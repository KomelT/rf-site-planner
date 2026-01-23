#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import time
import math
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple
from urllib.request import Request, urlopen

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# RX sites (fixed endpoints) + RSSI fields in CSV
# ---------------------------------------------------------------------------

RX_SITES = [
    {
        "name": "HQ",
        "lat": 45.8435599,
        "lon": 13.73427,
        "rssi_field": "!75f19024",
        "rx_height": 15.0,
        "rx_gain": 6.5,
        "rx_loss": 0.0,
    },
    {
        "name": "SV. Katarina",
        "lat": 45.85474,
        "lon": 13.72615,
        "rssi_field": "!7369fb6a",
        "rx_height": 3.0,
        "rx_gain": 5.0,
        "rx_loss": 0.0,
    },
    {
        "name": "Mobil",
        "lat": 45.8463800779,
        "lon": 13.7232441999,
        "rssi_field": "!da5ad56c",
        "rx_height": 2.0,
        "rx_gain": 6.5,
        "rx_loss": 0.0,
    },
]

# ---------------------------------------------------------------------------
# API + CSV fields
# ---------------------------------------------------------------------------

API_URL = "http://localhost:8081"
LAT_FIELD = "latitudeI"
LON_FIELD = "longitudeI"
COORD_SCALE = 1e7

API_REQUEST_TIMEOUT = 30.0
API_POLL_TIMEOUT = 600.0

POLL_INITIAL = 0.2
POLL_AFTER_5S = 0.5
POLL_AFTER_20S = 1.0

DEFAULTS = {
    "tx_height": 3.0,
    "tx_power": 27.0,
    "tx_gain": 5.0,
    "tx_loss": 10,
    "frequency_mhz": 869.525,
    "clutter_height": 2.0,
    "ground_dielectric": 15.0,
    "ground_conductivity": 0.005,
    "atmosphere_bending": 301.0,
    "radio_climate": "continental_temperate",
    "polarization": "vertical",
    "situation_fraction": 99,
    "time_fraction": 99,
    "high_resolution": True,
    "itm_mode": True,
}

DISTANCE_BIN_KM_DEFAULT = 1.0

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def http_json(url: str, payload: Optional[Dict[str, Any]], timeout: float) -> Dict[str, Any]:
    if payload is None:
        req = Request(url)
    else:
        data = json.dumps(payload).encode("utf-8")
        req = Request(url, data=data, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def poll_task(task_id: str) -> Dict[str, Any]:
    start = time.monotonic()
    deadline = start + API_POLL_TIMEOUT
    while time.monotonic() < deadline:
        status = http_json(f"{API_URL}/task/{task_id}", None, API_REQUEST_TIMEOUT)
        st = status.get("status")
        if st == "completed":
            return status
        if st == "failed":
            raise RuntimeError(status.get("error", "Task failed"))

        elapsed = time.monotonic() - start
        if elapsed < 5.0:
            time.sleep(POLL_INITIAL)
        elif elapsed < 20.0:
            time.sleep(POLL_AFTER_5S)
        else:
            time.sleep(POLL_AFTER_20S)

    raise TimeoutError(f"Task {task_id} timed out after {API_POLL_TIMEOUT}s")


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_optional_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip().strip('"').strip("'")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def normalize_bool(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return None


def resolve_csv_path(input_path: str) -> Path:
    path = Path(input_path)
    if path.is_dir():
        csv_files = sorted(
            p
            for p in path.iterdir()
            if p.is_file() and p.suffix.lower() == ".csv" and p.name.lower() != "analyze.csv"
        )
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in folder: {path}")
        if len(csv_files) > 1:
            raise ValueError(f"Multiple CSV files found in folder: {path}")
        return csv_files[0]
    if path.is_file():
        return path
    raise FileNotFoundError(f"Input path not found: {path}")


def detect_sites(fieldnames: List[str]) -> List[Dict[str, Any]]:
    return [s for s in RX_SITES if s["rssi_field"] in fieldnames]


def site_columns(f: str) -> List[str]:
    return [
        f"{f}_mesaured_rssi",
        f"{f}_predicted_rssi",
        f"{f}_path_loss_rssi",
        f"{f}_los_obstructed",
        f"{f}_fresnel_60_obstructed",
        f"{f}_first_fresnel_obstructed",
    ]


# ---------------------------------------------------------------------------
# Stats helpers (single combined table per site)
# ---------------------------------------------------------------------------


def new_site_stats() -> Dict[str, Any]:
    return {
        "completed": 0,
        "failed": 0,
        "skipped_no_rssi": 0,
        "x": [],
        "rssi": [],
        "pred": [],
        "diff": [],
        "diff_values": [],
        "dist_km": [],
        "los_fresnel_clear_x": [],
        "los_fresnel_clear_diff": [],
        "los_obstructed_x": [],
        "los_obstructed_diff": [],
        "los_obstructed_dist": [],
        "fresnel_60_obstructed_x": [],
        "fresnel_60_obstructed_diff": [],
        "first_fresnel_obstructed_x": [],
        "first_fresnel_obstructed_diff": [],
    }


def normalize_pred(pred: Any) -> Optional[float]:
    if pred is None:
        return None
    try:
        p = float(pred)
    except Exception:
        return None
    if p > 0:
        p = -abs(p)
    return p


def apply_result_to_stats(
    per_site: Dict[str, Dict[str, Any]],
    site_field: str,
    idx: int,
    dist_km: float,
    rssi: float,
    pred: Any,
    los_obstructed: Optional[bool],
    fresnel_60_obstructed: Optional[bool],
    first_fresnel_obstructed: Optional[bool],
) -> None:
    st = per_site[site_field]
    pred_f = normalize_pred(pred)
    if pred_f is None:
        return

    diff = pred_f - rssi

    st["diff_values"].append(diff)
    st["x"].append(idx)
    st["rssi"].append(rssi)
    st["pred"].append(pred_f)
    st["diff"].append(diff)
    st["dist_km"].append(dist_km)

    if los_obstructed is True:
        st["los_obstructed_x"].append(idx)
        st["los_obstructed_diff"].append(diff)
        st["los_obstructed_dist"].append(dist_km)
    elif fresnel_60_obstructed is True:
        st["fresnel_60_obstructed_x"].append(idx)
        st["fresnel_60_obstructed_diff"].append(diff)
    elif first_fresnel_obstructed is True:
        st["first_fresnel_obstructed_x"].append(idx)
        st["first_fresnel_obstructed_diff"].append(diff)
    else:
        st["los_fresnel_clear_x"].append(idx)
        st["los_fresnel_clear_diff"].append(diff)


def _percentile(sorted_vals: List[float], q: float) -> Optional[float]:
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1:
        return float(sorted_vals[0])
    pos = (n - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(sorted_vals[lo])
    w = pos - lo
    return float(sorted_vals[lo] * (1.0 - w) + sorted_vals[hi] * w)


def _pearson_corr(xs: List[float], ys: List[float]) -> Optional[float]:
    if not xs or not ys or len(xs) != len(ys) or len(xs) < 2:
        return None
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = 0.0
    dx2 = 0.0
    dy2 = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        dy = y - my
        num += dx * dy
        dx2 += dx * dx
        dy2 += dy * dy
    den = math.sqrt(dx2 * dy2)
    if den == 0.0:
        return None
    return num / den


def _calc_stats(values: List[float]) -> Optional[Dict[str, float]]:
    if not values:
        return None

    n = len(values)
    mean_err = sum(values) / n
    abs_vals = [abs(v) for v in values]
    mae = sum(abs_vals) / n
    rmse = math.sqrt(sum(v * v for v in values) / n)

    if n > 1:
        var = sum((v - mean_err) ** 2 for v in values) / (n - 1)
        std = math.sqrt(var)
    else:
        std = 0.0

    sorted_vals = sorted(values)
    median_err = _percentile(sorted_vals, 0.5)

    abs_sorted = sorted(abs_vals)
    p90_abs = _percentile(abs_sorted, 0.90)
    p95_abs = _percentile(abs_sorted, 0.95)

    if median_err is None:
        mad = None
    else:
        dev = [abs(v - median_err) for v in values]
        mad = _percentile(sorted(dev), 0.5)

    within_3 = sum(1 for a in abs_vals if a <= 3.0) / n
    within_6 = sum(1 for a in abs_vals if a <= 6.0) / n
    within_10 = sum(1 for a in abs_vals if a <= 10.0) / n

    return {
        "count": float(n),
        "mean_error": mean_err,
        "std": std,
        "mae": mae,
        "rmse": rmse,
        "median_error": float(median_err) if median_err is not None else float("nan"),
        "mad": float(mad) if mad is not None else float("nan"),
        "p90_abs": float(p90_abs) if p90_abs is not None else float("nan"),
        "p95_abs": float(p95_abs) if p95_abs is not None else float("nan"),
        "min": float(sorted_vals[0]),
        "max": float(sorted_vals[-1]),
        "within_3": within_3,
        "within_6": within_6,
        "within_10": within_10,
    }


def _fmt_f(x: Optional[float], nd: int = 3) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return ""
    return f"{x:.{nd}f}"


def _fmt_pct(x: Optional[float], nd: int = 1) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return ""
    return f"{x * 100:.{nd}f}%"


def _fmt_km_val(x: float) -> str:
    if abs(x - round(x)) < 1e-6:
        return str(int(round(x)))
    return f"{x:.1f}"


def _distance_bin_label(bin_idx: int, bin_km: float) -> str:
    start = bin_idx * bin_km
    end = start + bin_km
    return f"{_fmt_km_val(start)}-{_fmt_km_val(end)} km"


def _distance_bin_tag(bin_km: float) -> str:
    return f"{_fmt_km_val(bin_km)}km"


def _md_table_row(cols: List[str]) -> str:
    safe = [c.replace("|", "\\|") for c in cols]
    return "| " + " | ".join(safe) + " |"


def _write_stats_comparison_table(
    out_md,
    title: str,
    stats_by_category: Dict[str, Optional[Dict[str, float]]],
    pred_label: str,
) -> None:
    """
    ONE table: rows=metrics, cols=categories
    """
    print(f"### {title}", file=out_md)
    print("", file=out_md)

    categories = list(stats_by_category.keys())

    def get(cat: str, key: str) -> Optional[float]:
        st = stats_by_category.get(cat)
        if not st:
            return None
        return st.get(key)

    metrics = [
        ("Number of samples (N)", "count", "int"),
        (f"Average error / bias (mean of {pred_label} − measured) [dB]", "mean_error", "f3"),
        ("Standard deviation of error [dB]", "std", "f3"),
        ("Mean absolute error [dB]", "mae", "f3"),
        ("Root mean square error [dB]", "rmse", "f3"),
        ("Median error [dB]", "median_error", "f3"),
        ("Median absolute deviation (robust spread) [dB]", "mad", "f3"),
        ("90th percentile of absolute error [dB]", "p90_abs", "f3"),
        ("95th percentile of absolute error [dB]", "p95_abs", "f3"),
        ("Minimum error [dB]", "min", "f3"),
        ("Maximum error [dB]", "max", "f3"),
        ("Share within ±3 dB", "within_3", "pct"),
        ("Share within ±6 dB", "within_6", "pct"),
        ("Share within ±10 dB", "within_10", "pct"),
    ]

    header = ["Metric"] + categories
    print(_md_table_row(header), file=out_md)
    print(_md_table_row(["---"] * len(header)), file=out_md)

    for label, key, fmt in metrics:
        row = [label]
        for cat in categories:
            val = get(cat, key)
            if val is None:
                row.append("")
            elif fmt == "int":
                row.append(str(int(val)))
            elif fmt == "pct":
                row.append(_fmt_pct(val))
            else:
                row.append(_fmt_f(val))
        print(_md_table_row(row), file=out_md)

    print("", file=out_md)


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------


def _scatter_if(ax, xs, ys, **kwargs):
    if xs and ys and len(xs) == len(ys):
        ax.scatter(xs, ys, **kwargs)


def save_series_plot(
    x,
    y,
    title,
    xlabel,
    ylabel,
    out_png,
    green_x=None,
    green_y=None,
    red_x=None,
    red_y=None,
    orange_x=None,
    orange_y=None,
    yellow_x=None,
    yellow_y=None,
    stderr=sys.stderr,
):
    if not x:
        return
    fig, ax = plt.subplots()
    ax.plot(x, y)

    _scatter_if(ax, green_x or [], green_y or [], color="green", s=16, zorder=3, label="No obstructions")
    _scatter_if(ax, red_x or [], red_y or [], color="red", s=16, zorder=3, label="LOS obstructed")
    _scatter_if(ax, orange_x or [], orange_y or [], color="orange", s=16, zorder=3, label="Fresnel 60 obstructed")
    _scatter_if(ax, yellow_x or [], yellow_y or [], color="yellow", s=16, zorder=3, label="First Fresnel obstructed")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if any([(green_x and green_y), (red_x and red_y), (orange_x and orange_y), (yellow_x and yellow_y)]):
        ax.legend()

    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_two_series_plot(x, y1, y2, label1, label2, title, xlabel, ylabel, out_png, stderr=sys.stderr):
    if not x:
        return
    fig, ax = plt.subplots()
    ax.plot(x, y1, label=label1)
    ax.plot(x, y2, label=label2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_multi_series_plot(series, title, xlabel, ylabel, out_png, stderr=sys.stderr):
    if not any(s.get("x") for s in series):
        return
    fig, ax = plt.subplots()
    for s in series:
        if s.get("x"):
            ax.plot(s["x"], s["y"], label=s["label"])
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def _linreg(xs: List[float], ys: List[float]) -> Optional[Tuple[float, float, float]]:
    n = len(xs)
    if n < 2 or n != len(ys):
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    ss_xx = 0.0
    ss_xy = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        ss_xx += dx * dx
        ss_xy += dx * (y - my)
    if ss_xx == 0.0:
        return None
    m = ss_xy / ss_xx
    b = my - m * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    return m, b, r2


def save_scatter_with_linreg(
    xs: List[float],
    ys: List[float],
    title: str,
    xlabel: str,
    ylabel: str,
    out_png: str,
    stderr=sys.stderr,
):
    if not xs or not ys or len(xs) != len(ys):
        return
    fig, ax = plt.subplots()
    ax.scatter(xs, ys, s=16, alpha=0.7)
    reg = _linreg(xs, ys)
    if reg:
        m, b, r2 = reg
        x_min = min(xs)
        x_max = max(xs)
        xs_line = [x_min, x_max]
        ys_line = [m * x_min + b, m * x_max + b]
        ax.plot(xs_line, ys_line, color="red", linewidth=1.5)
        ax.text(
            0.02,
            0.98,
            f"y = {m:.3f}x + {b:.3f}\nR² = {r2:.3f}",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=9,
            bbox={"facecolor": "white", "alpha": 0.6, "edgecolor": "none"},
        )
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_diff_category_boxplot(
    categories: List[Tuple[str, List[float]]],
    title: str,
    ylabel: str,
    out_png: str,
    title_size: Optional[int] = None,
    label_size: Optional[int] = None,
    tick_size: Optional[int] = None,
    stderr=sys.stderr,
):
    if not any(vals for _, vals in categories):
        return
    fig, ax = plt.subplots()
    labels = [label for label, _ in categories]
    data = [vals for _, vals in categories]
    ax.boxplot(data, tick_labels=labels, showfliers=True)
    if title_size is None:
        ax.set_title(title)
    else:
        ax.set_title(title, fontsize=title_size)
    if label_size is None:
        ax.set_ylabel(ylabel)
    else:
        ax.set_ylabel(ylabel, fontsize=label_size)
    if tick_size is not None:
        ax.tick_params(axis="both", labelsize=tick_size)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_distance_boxplot(
    dist_km: List[float],
    diffs: List[float],
    bin_km: float,
    title: str,
    ylabel: str,
    out_png: str,
    stderr=sys.stderr,
):
    if not dist_km or not diffs:
        return
    if bin_km <= 0:
        return

    bins: Dict[int, List[float]] = {}
    for d, diff in zip(dist_km, diffs):
        if d is None:
            continue
        bin_idx = int(math.floor(d / bin_km))
        bins.setdefault(bin_idx, []).append(diff)

    categories = [(_distance_bin_label(idx, bin_km), bins[idx]) for idx in sorted(bins.keys())]
    save_diff_category_boxplot(
        categories,
        title,
        ylabel,
        out_png,
        title_size=10,
        label_size=9,
        tick_size=8,
        stderr=stderr,
    )


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * r * math.asin(math.sqrt(a))


def format_duration(seconds: float) -> str:
    seconds = max(0.0, seconds)
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{sec:02d}s"
    if minutes:
        return f"{minutes}m{sec:02d}s"
    return f"{sec}s"


def write_stats_and_plots(
    output_dir: Path,
    detected_sites: List[Dict[str, Any]],
    per_site: Dict[str, Dict[str, Any]],
    pred_label: str,
    report_name: str = "analyze.md",
) -> None:
    output_md_path = output_dir / report_name
    print(f"Wrote report: {output_md_path}", file=sys.stderr)

    with open(output_md_path, "w", encoding="utf-8") as out_md:
        print("# RF Site Planner – RSSI analysis", file=out_md)
        print("", file=out_md)
        print(f"- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}", file=out_md)
        print("", file=out_md)

        # Summary table
        print("## Summary per gateway", file=out_md)
        print("", file=out_md)

        summary_header = [
            "Gateway (site id)",
            "Completed requests",
            "Failed requests",
            "Skipped rows (missing RSSI)",
            "Number of samples (N)",
            "Mean absolute error [dB]",
            "Standard deviation of error [dB]",
            "Root mean square error [dB]",
            "Average error / bias [dB]",
            "90th percentile of absolute error [dB]",
            "Share within ±6 dB",
            f"Pearson correlation ({pred_label} vs measured)",
        ]
        print(_md_table_row(summary_header), file=out_md)
        print(_md_table_row(["---"] * len(summary_header)), file=out_md)

        for s in detected_sites:
            f = s["rssi_field"]
            st = per_site[f]
            stats_all = _calc_stats(st["diff_values"])
            corr = _pearson_corr(st["pred"], st["rssi"])

            n = int(stats_all["count"]) if stats_all else 0
            mae = _fmt_f(stats_all["mae"]) if stats_all else ""
            std = _fmt_f(stats_all["std"]) if stats_all else ""
            rmse = _fmt_f(stats_all["rmse"]) if stats_all else ""
            bias = _fmt_f(stats_all["mean_error"]) if stats_all else ""
            p90 = _fmt_f(stats_all["p90_abs"]) if stats_all else ""
            w6 = _fmt_pct(stats_all["within_6"]) if stats_all else ""
            corr_s = _fmt_f(corr, 3) if corr is not None else ""

            row = [
                f,
                str(st["completed"]),
                str(st["failed"]),
                str(st["skipped_no_rssi"]),
                str(n),
                mae,
                std,
                rmse,
                bias,
                p90,
                w6,
                corr_s,
            ]
            print(_md_table_row(row), file=out_md)

        print("", file=out_md)

        # Per-site details (ONE combined table per site, no "Metric | Value" tables)
        for s in detected_sites:
            f = s["rssi_field"]
            st = per_site[f]

            stats_all = _calc_stats(st["diff_values"])
            stats_clear = _calc_stats(st["los_fresnel_clear_diff"])
            stats_los = _calc_stats(st["los_obstructed_diff"])
            stats_f60 = _calc_stats(st["fresnel_60_obstructed_diff"])
            stats_ff = _calc_stats(st["first_fresnel_obstructed_diff"])
            corr = _pearson_corr(st["pred"], st["rssi"])

            total = len(st["diff_values"])
            total_safe = total if total > 0 else 1

            share_clear = len(st["los_fresnel_clear_diff"]) / total_safe
            share_los = len(st["los_obstructed_diff"]) / total_safe
            share_f60 = len(st["fresnel_60_obstructed_diff"]) / total_safe
            share_ff = len(st["first_fresnel_obstructed_diff"]) / total_safe

            print(f"## Gateway: `{f}`", file=out_md)
            print("", file=out_md)
            print(f"- Completed requests: **{st['completed']}**", file=out_md)
            print(f"- Failed requests: **{st['failed']}**", file=out_md)
            print(f"- Skipped rows (missing RSSI): **{st['skipped_no_rssi']}**", file=out_md)
            print(f"- Number of samples (N): **{total}**", file=out_md)
            print(
                f"- Pearson correlation ({pred_label} vs measured): **{_fmt_f(corr, 3) if corr is not None else ''}**",
                file=out_md,
            )
            print("", file=out_md)

            print("### Distribution by visibility category", file=out_md)
            print("", file=out_md)
            cov_header = ["Category", "N", "Share"]
            print(_md_table_row(cov_header), file=out_md)
            print(_md_table_row(["---"] * len(cov_header)), file=out_md)
            print(_md_table_row(["Line of sight clear (no obstructions)", str(len(st["los_fresnel_clear_diff"])), _fmt_pct(share_clear)]), file=out_md)
            print(_md_table_row(["Line of sight obstructed", str(len(st["los_obstructed_diff"])), _fmt_pct(share_los)]), file=out_md)
            print(_md_table_row(["60% of first Fresnel zone obstructed", str(len(st["fresnel_60_obstructed_diff"])), _fmt_pct(share_f60)]), file=out_md)
            print(_md_table_row(["First Fresnel zone obstructed", str(len(st["first_fresnel_obstructed_diff"])), _fmt_pct(share_ff)]), file=out_md)
            print("", file=out_md)

            stats_by_category = {
                "All samples": stats_all,
                "Line of sight clear": stats_clear,
                "Line of sight obstructed": stats_los,
                "Fresnel 60% obstructed": stats_f60,
                "First Fresnel obstructed": stats_ff,
            }
            _write_stats_comparison_table(
                out_md,
                f"Error statistics by category (error = {pred_label} − measured)",
                stats_by_category,
                pred_label,
            )

            # Plots
            save_series_plot(
                st["x"],
                st["diff"],
                title=f"{f} gateway: error ({pred_label} - measured) RSSI",
                xlabel="Row ID",
                ylabel="RSSI error (dB)",
                out_png=str(output_dir / f"{f}_diff.png"),
                green_x=st["los_fresnel_clear_x"],
                green_y=st["los_fresnel_clear_diff"],
                orange_x=st["fresnel_60_obstructed_x"],
                orange_y=st["fresnel_60_obstructed_diff"],
                yellow_x=st["first_fresnel_obstructed_x"],
                yellow_y=st["first_fresnel_obstructed_diff"],
                red_x=st["los_obstructed_x"],
                red_y=st["los_obstructed_diff"],
            )

            save_two_series_plot(
                st["x"],
                st["rssi"],
                st["pred"],
                label1="measured",
                label2=pred_label,
                title=f"{f} gateway: measured vs {pred_label} RSSI",
                xlabel="Row ID",
                ylabel="RSSI (dBm)",
                out_png=str(output_dir / f"{f}_val.png"),
            )

            save_diff_category_boxplot(
                categories=[
                    ("All", st["diff_values"]),
                    ("Clear", st["los_fresnel_clear_diff"]),
                    ("LOS", st["los_obstructed_diff"]),
                    ("F60", st["fresnel_60_obstructed_diff"]),
                    ("FF", st["first_fresnel_obstructed_diff"]),
                ],
                title=f"{f} gateway: error by category",
                ylabel="RSSI error (dB)",
                out_png=str(output_dir / f"{f}_diff_box.png"),
            )

        # Multi-site plots
        if len(detected_sites) > 1:
            diff_series = []
            for s in detected_sites:
                f = s["rssi_field"]
                diff_series.append({"x": per_site[f]["x"], "y": per_site[f]["diff"], "label": f"{f} {pred_label} error"})
            save_multi_series_plot(
                diff_series,
                title=f"All gateways: RSSI error ({pred_label} - measured)",
                xlabel="Row ID",
                ylabel="RSSI error (dB)",
                out_png=str(output_dir / "all_sites_diff.png"),
            )

            rssi_series = []
            for s in detected_sites:
                f = s["rssi_field"]
                rssi_series.append({"x": per_site[f]["x"], "y": per_site[f]["rssi"], "label": f"{f} measured"})
                rssi_series.append({"x": per_site[f]["x"], "y": per_site[f]["pred"], "label": f"{f} {pred_label}"})
            save_multi_series_plot(
                rssi_series,
                title=f"All gateways: measured + {pred_label} RSSI",
                xlabel="Row ID",
                ylabel="RSSI (dBm)",
                out_png=str(output_dir / "all_sites_rssi.png"),
            )


def write_distance_boxplots(
    output_dir: Path,
    detected_sites: List[Dict[str, Any]],
    per_site: Dict[str, Dict[str, Any]],
    pred_label: str,
    bin_km: float,
) -> None:
    if bin_km <= 0:
        return
    output_dir.mkdir(exist_ok=True)
    bin_tag = _distance_bin_tag(bin_km)
    for s in detected_sites:
        f = s["rssi_field"]
        st = per_site[f]
        out_png = output_dir / f"{f}_diff_box_by_{bin_tag}.png"
        save_distance_boxplot(
            st["dist_km"],
            st["diff_values"],
            bin_km,
            title=f"{f} gateway: {pred_label} error by distance ({bin_tag} bins)",
            ylabel="RSSI error (dB)",
            out_png=str(out_png),
        )


def write_non_los_length_scatter(
    output_dir: Path,
    detected_sites: List[Dict[str, Any]],
    per_site: Dict[str, Dict[str, Any]],
    pred_label: str,
) -> None:
    output_dir.mkdir(exist_ok=True)
    summary_rows = []
    for s in detected_sites:
        f = s["rssi_field"]
        st = per_site[f]
        reg = _linreg(st["los_obstructed_dist"], st["los_obstructed_diff"])
        if reg:
            m, b, r2 = reg
        else:
            m = b = r2 = None
        out_png = output_dir / f"{f}_diff_vs_length_non_los.png"
        save_scatter_with_linreg(
            st["los_obstructed_dist"],
            st["los_obstructed_diff"],
            title=f"{f} gateway: {pred_label} error vs link length (non-LOS)",
            xlabel="Link length (km)",
            ylabel="RSSI error (dB)",
            out_png=str(out_png),
        )
        summary_rows.append(
            {
                "site": f,
                "count": len(st["los_obstructed_diff"]),
                "slope_db_per_km": m,
                "intercept_db": b,
                "r2": r2,
            }
        )

    summary_path = output_dir / "summary.md"
    with open(summary_path, "w", encoding="utf-8") as out_md:
        print(f"# Non-LOS error vs link length ({pred_label})", file=out_md)
        print("", file=out_md)
        header = ["Gateway (site id)", "N", "Slope [dB/km]", "Intercept [dB]", "R²"]
        print(_md_table_row(header), file=out_md)
        print(_md_table_row(["---"] * len(header)), file=out_md)
        for row in summary_rows:
            print(
                _md_table_row(
                    [
                        row["site"],
                        str(int(row["count"])),
                        _fmt_f(row["slope_db_per_km"], 4) if row["slope_db_per_km"] is not None else "",
                        _fmt_f(row["intercept_db"], 3) if row["intercept_db"] is not None else "",
                        _fmt_f(row["r2"], 3) if row["r2"] is not None else "",
                    ]
                ),
                file=out_md,
            )


# ---------------------------------------------------------------------------
# LOS request
# ---------------------------------------------------------------------------


def build_payload(tx_lat: float, tx_lon: float, site: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(DEFAULTS)
    payload.update(
        {
            "tx_lat": tx_lat,
            "tx_lon": tx_lon,
            "rx_lat": float(site["lat"]),
            "rx_lon": float(site["lon"]),
            "rx_height": float(site["rx_height"]),
            "rx_gain": float(site["rx_gain"]),
            "rx_loss": float(site["rx_loss"]),
        }
    )
    return payload


def run_los_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    submit = http_json(f"{API_URL}/los", payload, API_REQUEST_TIMEOUT)
    task_id = submit["task_id"]
    status = poll_task(task_id)

    if "data" not in status or not status["data"]:
        return {
            "ok": True,
            "pred": None,
            "path_loss_rssi": None,
            "los_obstructed": None,
            "fresnel_60_obstructed": None,
            "first_fresnel_obstructed": None,
        }

    data = json.loads(status["data"])
    return {
        "ok": True,
        "pred": data.get("rx_signal_power"),
        "path_loss_rssi": data.get("path_loss_rssi"),
        "los_obstructed": normalize_bool(data.get("path", {}).get("obstructed")),
        "first_fresnel_obstructed": normalize_bool(data.get("first_fresnel", {}).get("obstructed")),
        "fresnel_60_obstructed": normalize_bool(
            data.get("freshnel_60", data.get("fresnel_60", {})).get("obstructed")
        ),
    }


# ---------------------------------------------------------------------------
# GeoJSON
# ---------------------------------------------------------------------------


def write_geojson(csv_path: Path, out_path: Path) -> int:
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("Input file has no header row.")
        if LAT_FIELD not in reader.fieldnames or LON_FIELD not in reader.fieldnames:
            raise ValueError(f"Missing required columns. Found: {reader.fieldnames}")

        features = []
        for idx, row in enumerate(reader, start=1):
            raw_lat = parse_optional_float(row.get(LAT_FIELD))
            raw_lon = parse_optional_float(row.get(LON_FIELD))
            if raw_lat is None or raw_lon is None:
                continue

            lat = raw_lat / COORD_SCALE
            lon = raw_lon / COORD_SCALE

            props = dict(row)
            props["row"] = idx
            props["lat"] = lat
            props["lon"] = lon

            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "properties": props,
                }
            )

    out = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as out_fh:
        json.dump(out, out_fh, ensure_ascii=True)
    return len(features)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run LOS requests for each CSV row against the RF site planner API or output GeoJSON only."
    )
    p.add_argument("input_path", help="Folder containing a single CSV (or a CSV path)")
    p.add_argument("--geojson-only", "-g", action="store_true", help="Only generate GeoJSON and skip LOS requests")
    p.add_argument("--no-prediction", "-n", action="store_true", help="Skip API calls and rebuild stats/plots from analyze.csv")
    p.add_argument("--parallel", "-p", type=int, default=20, help="Number of parallel LOS requests (0 = sequential)")
    p.add_argument("--queue-mult", type=int, default=4, help="Max in-flight = parallel * queue_mult")
    p.add_argument(
        "--distance-bin-km",
        type=float,
        default=DISTANCE_BIN_KM_DEFAULT,
        help="Distance bin size in km for diff boxplots (default: 1.0)",
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    args = parse_args()
    if args.distance_bin_km <= 0:
        print("--distance-bin-km must be > 0", file=sys.stderr)
        return 1

    csv_path = resolve_csv_path(args.input_path)
    output_dir = csv_path.parent
    output_csv_path = output_dir / "analyze.csv"
    output_geojson_path = output_dir / "analyze.geojson"

    # GeoJSON-only
    if args.geojson_only:
        try:
            count = write_geojson(csv_path, output_geojson_path)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Wrote GeoJSON: {output_geojson_path} ({count} points)", file=sys.stderr)
        return 0

    # No-prediction: rebuild from analyze.csv (keeps combined tables)
    if args.no_prediction:
        if not output_csv_path.exists():
            print(f"Missing analyze.csv at {output_csv_path}", file=sys.stderr)
            return 1

        with open(output_csv_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                print("Input analyze.csv has no header row.", file=sys.stderr)
                return 1
            header = list(reader.fieldnames)
            rows = list(reader)

        detected_sites = [s for s in RX_SITES if f"{s['rssi_field']}_mesaured_rssi" in header]
        per_site_model = {s["rssi_field"]: new_site_stats() for s in detected_sites}
        per_site_fpls = {s["rssi_field"]: new_site_stats() for s in detected_sites}

        # ensure prediction + obstruction columns exist
        for s in detected_sites:
            f = s["rssi_field"]
            for col in site_columns(f):
                if col not in header:
                    header.append(col)

        # remove legacy diff columns (if present)
        header = [col for col in header if not col.endswith("_rssi_diff")]

        with open(output_csv_path, "w", newline="", encoding="utf-8") as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(header)

            for idx, row in enumerate(rows, start=1):
                lat = parse_optional_float(row.get("lat"))
                lon = parse_optional_float(row.get("lon"))
                if lat is None or lon is None:
                    continue

                row_id = parse_optional_float(row.get("row"))
                x_val = int(row_id) if row_id is not None else idx

                for s in detected_sites:
                    f = s["rssi_field"]
                    st_model = per_site_model[f]
                    st_fpls = per_site_fpls[f]
                    dist_km = haversine_km(lat, lon, float(s["lat"]), float(s["lon"]))

                    rssi = parse_optional_float(row.get(f"{f}_mesaured_rssi"))
                    pred = parse_optional_float(row.get(f"{f}_predicted_rssi"))
                    path_loss = parse_optional_float(row.get(f"{f}_path_loss_rssi"))
                    if rssi is None:
                        st_model["skipped_no_rssi"] += 1
                        st_fpls["skipped_no_rssi"] += 1
                        continue

                    los = normalize_bool(row.get(f"{f}_los_obstructed"))
                    f60 = normalize_bool(row.get(f"{f}_fresnel_60_obstructed"))
                    ff = normalize_bool(row.get(f"{f}_first_fresnel_obstructed"))

                    if pred is not None:
                        st_model["completed"] += 1
                        apply_result_to_stats(per_site_model, f, x_val, dist_km, float(rssi), pred, los, f60, ff)
                    if path_loss is not None:
                        st_fpls["completed"] += 1
                        apply_result_to_stats(per_site_fpls, f, x_val, dist_km, float(rssi), path_loss, los, f60, ff)

                writer.writerow([row.get(col) for col in header])

        model_dir = output_dir / "model_pred"
        fpls_dir = output_dir / "fpls_pred"
        model_dir.mkdir(exist_ok=True)
        fpls_dir.mkdir(exist_ok=True)

        write_stats_and_plots(model_dir, detected_sites, per_site_model, pred_label="predicted")
        write_stats_and_plots(fpls_dir, detected_sites, per_site_fpls, pred_label="path loss")

        model_len_dir = output_dir / "model_pred_length"
        write_distance_boxplots(
            model_len_dir,
            detected_sites,
            per_site_model,
            pred_label="predicted",
            bin_km=args.distance_bin_km,
        )

        model_nlos_len_dir = output_dir / "model_pred_length_non_los"
        write_non_los_length_scatter(
            model_nlos_len_dir,
            detected_sites,
            per_site_model,
            pred_label="predicted",
        )
        return 0

    # Prediction mode: load rows first to count requests and keep order
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            print("Input file has no header row.", file=sys.stderr)
            return 1
        if LAT_FIELD not in reader.fieldnames or LON_FIELD not in reader.fieldnames:
            print(f"Missing required columns. Found: {reader.fieldnames}", file=sys.stderr)
            return 1

        detected_sites = detect_sites(list(reader.fieldnames))
        per_site_model = {s["rssi_field"]: new_site_stats() for s in detected_sites}
        per_site_fpls = {s["rssi_field"]: new_site_stats() for s in detected_sites}

        header = ["row", "lat", "lon"]
        for s in detected_sites:
            header += site_columns(s["rssi_field"])

        rows: List[Tuple[int, float, float, Dict[str, Any]]] = []
        total_requests = 0

        for idx, row in enumerate(reader, start=1):
            raw_lat = parse_optional_float(row.get(LAT_FIELD))
            raw_lon = parse_optional_float(row.get(LON_FIELD))
            if raw_lat is None or raw_lon is None:
                continue

            lat = raw_lat / COORD_SCALE
            lon = raw_lon / COORD_SCALE

            for s in detected_sites:
                f = s["rssi_field"]
                if parse_optional_float(row.get(f)) is not None:
                    total_requests += 1
                else:
                    per_site_model[f]["skipped_no_rssi"] += 1
                    per_site_fpls[f]["skipped_no_rssi"] += 1

            rows.append((idx, lat, lon, row))

    completed_requests = 0
    start_time = time.monotonic()
    last_progress_t = start_time

    def maybe_print_progress():
        nonlocal last_progress_t
        if total_requests <= 0:
            return
        now = time.monotonic()
        if now - last_progress_t >= 1.0 or completed_requests % 25 == 0:
            elapsed = now - start_time
            avg = elapsed / max(1, completed_requests)
            remaining = max(0, (total_requests - completed_requests)) * avg
            percent = (completed_requests / total_requests) * 100
            print(
                f"Progress: {percent:.1f}% ({completed_requests}/{total_requests}) ETA {format_duration(remaining)}",
                file=sys.stderr,
            )
            last_progress_t = now

    with open(output_csv_path, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(header)

        # Parallel
        if args.parallel and args.parallel > 0:
            max_in_flight = args.parallel * max(1, args.queue_mult)
            results: Dict[int, Dict[str, Tuple[Any, Any, Optional[bool], Optional[bool], Optional[bool]]]] = {}

            def submit_one(executor, tx_lat: float, tx_lon: float, site: Dict[str, Any]):
                payload = build_payload(tx_lat, tx_lon, site)
                return executor.submit(run_los_request, payload)

            def task_iter():
                for (row_idx, lat, lon, row) in rows:
                    for site in detected_sites:
                        f = site["rssi_field"]
                        rssi = parse_optional_float(row.get(f))
                        if rssi is None:
                            continue
                        yield (row_idx, lat, lon, row, site, float(rssi))

            tasks = task_iter()
            in_flight: Dict[Any, Tuple[int, float, float, Dict[str, Any], Dict[str, Any], float]] = {}

            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                while len(in_flight) < max_in_flight:
                    try:
                        row_idx, lat, lon, row, site, rssi = next(tasks)
                    except StopIteration:
                        break
                    fut = submit_one(executor, lat, lon, site)
                    in_flight[fut] = (row_idx, lat, lon, row, site, rssi)

                while in_flight:
                    done, _ = wait(in_flight.keys(), return_when=FIRST_COMPLETED)
                    for fut in done:
                        row_idx, lat, lon, row, site, rssi = in_flight.pop(fut)
                        f = site["rssi_field"]
                        dist_km = haversine_km(lat, lon, float(site["lat"]), float(site["lon"]))

                        pred = None
                        path_loss = None
                        los = None
                        f60 = None
                        ff = None

                        try:
                            res = fut.result()
                            if res.get("ok"):
                                pred = res.get("pred")
                                path_loss = res.get("path_loss_rssi")
                                los = res.get("los_obstructed")
                                f60 = res.get("fresnel_60_obstructed")
                                ff = res.get("first_fresnel_obstructed")
                            else:
                                per_site_model[f]["failed"] += 1
                                per_site_fpls[f]["failed"] += 1
                                print(f"Row {row_idx} site {f}: LOS failed: {res.get('error','')}", file=sys.stderr)
                        except Exception as exc:
                            per_site_model[f]["failed"] += 1
                            per_site_fpls[f]["failed"] += 1
                            print(f"Row {row_idx} site {f}: LOS failed: {exc}", file=sys.stderr)

                        if pred is not None:
                            per_site_model[f]["completed"] += 1
                            apply_result_to_stats(per_site_model, f, row_idx, dist_km, rssi, pred, los, f60, ff)
                        if path_loss is not None:
                            per_site_fpls[f]["completed"] += 1
                            apply_result_to_stats(per_site_fpls, f, row_idx, dist_km, rssi, path_loss, los, f60, ff)
                        results.setdefault(row_idx, {})[f] = (pred, path_loss, los, f60, ff)

                        completed_requests += 1
                        maybe_print_progress()

                        while len(in_flight) < max_in_flight:
                            try:
                                n_row_idx, n_lat, n_lon, n_row, n_site, n_rssi = next(tasks)
                            except StopIteration:
                                break
                            n_fut = submit_one(executor, n_lat, n_lon, n_site)
                            in_flight[n_fut] = (n_row_idx, n_lat, n_lon, n_row, n_site, n_rssi)

            for (row_idx, lat, lon, row) in rows:
                out_row = [row_idx, lat, lon]
                for site in detected_sites:
                    f = site["rssi_field"]
                    rssi = parse_optional_float(row.get(f))
                    pred, path_loss, los, f60, ff = results.get(row_idx, {}).get(f, (None, None, None, None, None))
                    out_row += [rssi, pred, path_loss, los, f60, ff]
                writer.writerow(out_row)

        # Sequential
        else:
            for (row_idx, lat, lon, row) in rows:
                out_row = [row_idx, lat, lon]
                for site in detected_sites:
                    f = site["rssi_field"]
                    rssi = parse_optional_float(row.get(f))
                    if rssi is None:
                        out_row += [None, None, None, None, None, None]
                        continue
                    dist_km = haversine_km(lat, lon, float(site["lat"]), float(site["lon"]))

                    pred = None
                    path_loss = None
                    los = None
                    f60 = None
                    ff = None

                    try:
                        res = run_los_request(build_payload(lat, lon, site))
                        if res.get("ok"):
                            pred = res.get("pred")
                            path_loss = res.get("path_loss_rssi")
                            los = res.get("los_obstructed")
                            f60 = res.get("fresnel_60_obstructed")
                            ff = res.get("first_fresnel_obstructed")
                        else:
                            per_site_model[f]["failed"] += 1
                            per_site_fpls[f]["failed"] += 1
                            print(f"Row {row_idx} site {f}: LOS failed: {res.get('error','')}", file=sys.stderr)
                    except Exception as exc:
                        per_site_model[f]["failed"] += 1
                        per_site_fpls[f]["failed"] += 1
                        print(f"Row {row_idx} site {f}: LOS failed: {exc}", file=sys.stderr)

                    if pred is not None:
                        per_site_model[f]["completed"] += 1
                        apply_result_to_stats(per_site_model, f, row_idx, dist_km, float(rssi), pred, los, f60, ff)
                    if path_loss is not None:
                        per_site_fpls[f]["completed"] += 1
                        apply_result_to_stats(per_site_fpls, f, row_idx, dist_km, float(rssi), path_loss, los, f60, ff)
                    out_row += [rssi, pred, path_loss, los, f60, ff]

                    completed_requests += 1
                    maybe_print_progress()

                writer.writerow(out_row)

    model_dir = output_dir / "model_pred"
    fpls_dir = output_dir / "fpls_pred"
    model_dir.mkdir(exist_ok=True)
    fpls_dir.mkdir(exist_ok=True)

    write_stats_and_plots(model_dir, detected_sites, per_site_model, pred_label="predicted")
    write_stats_and_plots(fpls_dir, detected_sites, per_site_fpls, pred_label="path loss")

    model_len_dir = output_dir / "model_pred_length"
    write_distance_boxplots(
        model_len_dir,
        detected_sites,
        per_site_model,
        pred_label="predicted",
        bin_km=args.distance_bin_km,
    )

    model_nlos_len_dir = output_dir / "model_pred_length_non_los"
    write_non_los_length_scatter(
        model_nlos_len_dir,
        detected_sites,
        per_site_model,
        pred_label="predicted",
    )
    print(f"Rows: total_with_coords={len(rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
