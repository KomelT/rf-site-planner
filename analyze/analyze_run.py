#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import time
import math
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, Optional
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
# API + CSV defaults
# ---------------------------------------------------------------------------

API_URL = "http://localhost:8081"
LAT_FIELD = "latitudeI"
LON_FIELD = "longitudeI"
COORD_SCALE = 1e7

DEFAULTS = {
    "tx_height": 3.0,
    "tx_power": 27.0,
    "tx_gain": 5.0,
    "tx_loss": 3.0,
    "frequency_mhz": 869.525,
    "clutter_height": 1.0,
    "ground_dielectric": 15.0,
    "ground_conductivity": 0.005,
    "atmosphere_bending": 301.0,
    "radio_climate": "continental_temperate",
    "polarization": "vertical",
    "situation_fraction": 50.0,
    "time_fraction": 90.0,
    "high_resolution": True,
    "itu_model": True,
}


@dataclass
class ApiConfig:
    base_url: str
    poll_interval: float = 0.1
    poll_timeout: float = 600.0
    request_timeout: float = 30.0


def http_json(
    url: str, payload: Optional[Dict[str, Any]], timeout: float
) -> Dict[str, Any]:
    if payload is None:
        req = Request(url)
    else:
        data = json.dumps(payload).encode("utf-8")
        req = Request(url, data=data, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def poll_task(api: ApiConfig, task_id: str) -> Dict[str, Any]:
    deadline = time.monotonic() + api.poll_timeout
    while time.monotonic() < deadline:
        status = http_json(f"{api.base_url}/task/{task_id}", None, api.request_timeout)
        if status.get("status") == "completed":
            return status
        if status.get("status") == "failed":
            raise RuntimeError(status.get("error", "Task failed"))
        time.sleep(api.poll_interval)
    raise TimeoutError(f"Task {task_id} timed out after {api.poll_timeout}s")


def parse_optional_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    stripped = value.strip().strip('"').strip("'")
    if stripped == "":
        return None
    try:
        return float(stripped)
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


def build_payload(
    tx_lat: float,
    tx_lon: float,
    rx_lat: float,
    rx_lon: float,
    rx_height: float,
    rx_gain: float,
    rx_loss: float,
) -> Dict[str, Any]:
    payload = dict(DEFAULTS)
    payload.update(
        {
            "tx_lat": tx_lat,
            "tx_lon": tx_lon,
            "rx_lat": rx_lat,
            "rx_lon": rx_lon,
            "rx_height": rx_height,
            "rx_gain": rx_gain,
            "rx_loss": rx_loss,
        }
    )
    return payload


def resolve_csv_path(input_path: str) -> Path:
    path = Path(input_path)
    if path.is_dir():
        csv_files = sorted(
            p
            for p in path.iterdir()
            if p.is_file()
            and p.suffix.lower() == ".csv"
            and p.name.lower() != "analyze.csv"
        )
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in folder: {path}")
        if len(csv_files) > 1:
            raise ValueError(f"Multiple CSV files found in folder: {path}")
        return csv_files[0]
    if path.is_file():
        return path
    raise FileNotFoundError(f"Input path not found: {path}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run LOS requests for each CSV row against the RF site planner API or output GeoJSON only."
    )
    p.add_argument("input_path", help="Folder containing a single CSV (or a CSV path)")
    p.add_argument(
        "--geojson-only",
        "-g",
        action="store_true",
        help="Only generate GeoJSON and skip LOS requests",
    )
    p.add_argument(
        "--no-prediction",
        "-n",
        action="store_true",
        help="Skip API calls and rebuild stats/plots from analyze.csv",
    )
    return p.parse_args()


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
    plt.figure()
    plt.plot(x, y)
    if green_x and green_y:
        plt.scatter(
            green_x, green_y, color="green", s=16, zorder=3, label="No obstructions"
        )
    if red_x and red_y:
        plt.scatter(
            red_x, red_y, color="red", s=16, zorder=3, label="Fresnel 60 obstructed"
        )
    if orange_x and orange_y:
        plt.scatter(
            orange_x,
            orange_y,
            color="orange",
            s=16,
            zorder=3,
            label="First Fresnel obstructed",
        )
    if yellow_x and yellow_y:
        plt.scatter(
            yellow_x,
            yellow_y,
            color="yellow",
            s=16,
            zorder=3,
            label="LOS obstructed",
        )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if (
        (green_x and green_y)
        or (red_x and red_y)
        or (orange_x and orange_y)
        or (yellow_x and yellow_y)
    ):
        plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_two_series_plot(
    x, y1, y2, label1, label2, title, xlabel, ylabel, out_png, stderr=sys.stderr
):
    if not x:
        return
    plt.figure()
    plt.plot(x, y1, label=label1)
    plt.plot(x, y2, label=label2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_multi_series_plot(series, title, xlabel, ylabel, out_png, stderr=sys.stderr):
    """
    series: list of dicts: {"x": [...], "y": [...], "label": "..."}
    """
    # Draw only if at least one series has data
    if not any(s.get("x") for s in series):
        return
    plt.figure()
    for s in series:
        if s.get("x"):
            plt.plot(s["x"], s["y"], label=s["label"])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Wrote plot: {out_png}", file=stderr)


def format_duration(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{sec:02d}s"
    if minutes:
        return f"{minutes}m{sec:02d}s"
    return f"{sec}s"


def main() -> int:
    args = parse_args()
    api = ApiConfig(base_url=API_URL.rstrip("/"))

    rows_with_coords = 0
    detected_sites = []
    per_site = {}

    csv_path = resolve_csv_path(args.input_path)
    output_dir = csv_path.parent

    output_csv_path = output_dir / "analyze.csv"
    output_txt_path = output_dir / "analyze.txt"

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
            detected_sites = [
                s for s in RX_SITES if f"{s['rssi_field']}_mesaured_rssi" in header
            ]
            rows = list(reader)

        for s in detected_sites:
            f = s["rssi_field"]
            for col in (
                f"{f}_los_obstructed",
                f"{f}_first_fresnel_obstructed",
                f"{f}_fresnel_60_obstructed",
            ):
                if col not in header:
                    header.append(col)

        header = [col for col in header if not col.endswith("_rssi_diff")]

        for s in detected_sites:
            f = s["rssi_field"]
            per_site[f] = {
                "completed": 0,
                "failed": 0,
                "skipped_no_rssi": 0,
                "diff_values": [],
                "x": [],
                "rssi": [],
                "pred": [],
                "diff": [],
                "los_fresnel_clear_x": [],
                "los_fresnel_clear_diff": [],
                "fresnel_60_obstructed_x": [],
                "fresnel_60_obstructed_diff": [],
                "first_fresnel_obstructed_x": [],
                "first_fresnel_obstructed_diff": [],
                "los_obstructed_x": [],
                "los_obstructed_diff": [],
            }

        with open(output_csv_path, "w", newline="", encoding="utf-8") as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(header)

            for idx, row in enumerate(rows, start=1):
                csv_lat = parse_optional_float(row.get("lat"))
                csv_lon = parse_optional_float(row.get("lon"))
                if csv_lat is None or csv_lon is None:
                    continue
                rows_with_coords += 1

                row_id = parse_optional_float(row.get("row"))
                x_val = int(row_id) if row_id is not None else idx

                for s in detected_sites:
                    f = s["rssi_field"]
                    rssi_field = f"{f}_mesaured_rssi"
                    pred_field = f"{f}_predicted_rssi"
                    los_field = f"{f}_los_obstructed"
                    first_fresnel_field = f"{f}_first_fresnel_obstructed"
                    fresnel_60_field = f"{f}_fresnel_60_obstructed"

                    rssi = parse_optional_float(row.get(rssi_field))
                    pred = parse_optional_float(row.get(pred_field))
                    diff = None

                    if rssi is None:
                        per_site[f]["skipped_no_rssi"] += 1
                    if pred is not None and rssi is not None:
                        diff = pred - rssi

                    if pred is not None and rssi is not None and diff is not None:
                        per_site[f]["completed"] += 1
                        per_site[f]["diff_values"].append(diff)
                        per_site[f]["x"].append(x_val)
                        per_site[f]["rssi"].append(rssi)
                        per_site[f]["pred"].append(pred)
                        per_site[f]["diff"].append(diff)

                        los_obstructed = normalize_bool(row.get(los_field))
                        first_fresnel_obstructed = normalize_bool(
                            row.get(first_fresnel_field)
                        )
                        fresnel_60_obstructed = normalize_bool(row.get(fresnel_60_field))

                        if fresnel_60_obstructed is True:
                            per_site[f]["fresnel_60_obstructed_x"].append(x_val)
                            per_site[f]["fresnel_60_obstructed_diff"].append(diff)
                        elif first_fresnel_obstructed is True:
                            per_site[f]["first_fresnel_obstructed_x"].append(x_val)
                            per_site[f]["first_fresnel_obstructed_diff"].append(diff)
                        elif los_obstructed is True:
                            per_site[f]["los_obstructed_x"].append(x_val)
                            per_site[f]["los_obstructed_diff"].append(diff)
                        elif (
                            los_obstructed is False
                            and first_fresnel_obstructed is False
                            and fresnel_60_obstructed is False
                        ):
                            per_site[f]["los_fresnel_clear_x"].append(x_val)
                            per_site[f]["los_fresnel_clear_diff"].append(diff)

                writer.writerow([row.get(col) for col in header])
    else:
        with (
            open(csv_path, newline="", encoding="utf-8") as fh,
            open(output_csv_path, "w", newline="", encoding="utf-8") as out_csv,
        ):
            reader = csv.DictReader(fh)
            writer = csv.writer(out_csv)
            if not reader.fieldnames:
                print("Input file has no header row.", file=sys.stderr)
                return 1

            if LAT_FIELD not in reader.fieldnames or LON_FIELD not in reader.fieldnames:
                print(
                    f"Missing required columns. Found: {reader.fieldnames}",
                    file=sys.stderr,
                )
                return 1

            detected_sites = [
                s for s in RX_SITES if s["rssi_field"] in reader.fieldnames
            ]

            # Output CSV header (only detected RX sites)
            header = ["row", "lat", "lon"]
            for s in detected_sites:
                f = s["rssi_field"]
                header += [
                    f"{f}_mesaured_rssi",
                    f"{f}_predicted_rssi",
                    f"{f}_los_obstructed",
                    f"{f}_first_fresnel_obstructed",
                    f"{f}_fresnel_60_obstructed",
                ]
            writer.writerow(header)

            # Per-site buffers
            for s in detected_sites:
                f = s["rssi_field"]
                per_site[f] = {
                    "completed": 0,
                    "failed": 0,
                    "skipped_no_rssi": 0,
                    "diff_values": [],
                    "x": [],
                    "rssi": [],
                    "pred": [],
                    "diff": [],
                    "los_fresnel_clear_x": [],
                    "los_fresnel_clear_diff": [],
                    "fresnel_60_obstructed_x": [],
                    "fresnel_60_obstructed_diff": [],
                    "first_fresnel_obstructed_x": [],
                    "first_fresnel_obstructed_diff": [],
                    "los_obstructed_x": [],
                    "los_obstructed_diff": [],
                }

            total_requests = 0
            if not args.geojson_only:
                with open(csv_path, newline="", encoding="utf-8") as count_fh:
                    count_reader = csv.DictReader(count_fh)
                    for row in count_reader:
                        lat_val = (
                            (row.get(LAT_FIELD) or "").strip().strip('"').strip("'")
                        )
                        lon_val = (
                            (row.get(LON_FIELD) or "").strip().strip('"').strip("'")
                        )
                        if not lat_val or not lon_val:
                            continue
                        if lat_val == LAT_FIELD or lon_val == LON_FIELD:
                            continue
                        try:
                            float(lat_val)
                            float(lon_val)
                        except ValueError:
                            continue
                        for s in detected_sites:
                            f = s["rssi_field"]
                            if parse_optional_float(row.get(f)) is not None:
                                total_requests += 1

            completed_requests = 0
            start_time = time.monotonic()

            for idx, row in enumerate(reader, start=1):
                lat_val = (row.get(LAT_FIELD) or "").strip().strip('"').strip("'")
                lon_val = (row.get(LON_FIELD) or "").strip().strip('"').strip("'")

                if not lat_val or not lon_val:
                    continue
                if lat_val == LAT_FIELD or lon_val == LON_FIELD:
                    continue

                try:
                    raw_lat = float(lat_val)
                    raw_lon = float(lon_val)
                except ValueError:
                    continue

                csv_lat = raw_lat / COORD_SCALE
                csv_lon = raw_lon / COORD_SCALE
                rows_with_coords += 1

                out_row = [idx, csv_lat, csv_lon]
                for s in detected_sites:
                    f = s["rssi_field"]
                    rssi = parse_optional_float(row.get(f))
                    pred = None
                    diff = None
                    path_obstructed = None
                    fresnel_obstructed = None
                    fresnel_60_obstructed = None
                    los_obstructed_val = None
                    first_fresnel_val = None
                    fresnel_60_val = None

                    if args.geojson_only:
                        out_row += [rssi, None, None, None, None]
                        continue

                    if rssi is None:
                        per_site[f]["skipped_no_rssi"] += 1
                        out_row += [None, None, None, None, None]
                        continue

                    payload = build_payload(
                        tx_lat=csv_lat,
                        tx_lon=csv_lon,
                        rx_lat=float(s["lat"]),
                        rx_lon=float(s["lon"]),
                        rx_height=float(s["rx_height"]),
                        rx_gain=float(s["rx_gain"]),
                        rx_loss=float(s["rx_loss"]),
                    )

                    try:
                        submit = http_json(
                            f"{api.base_url}/los", payload, api.request_timeout
                        )
                        task_id = submit["task_id"]
                        status = poll_task(api, task_id)
                        per_site[f]["completed"] += 1

                        if "data" in status and status["data"]:
                            data = json.loads(status["data"])
                            pred = data.get("rx_signal_power")
                            path_obstructed = normalize_bool(
                                data.get("path", {}).get("obstructed")
                            )
                            fresnel_obstructed = normalize_bool(
                                data.get("first_fresnel", {}).get("obstructed")
                            )
                            fresnel_60_obstructed = normalize_bool(
                                data.get(
                                    "fresnel_60", {}
                                ).get("obstructed")
                            )
                            los_obstructed_val = path_obstructed
                            first_fresnel_val = fresnel_obstructed
                            fresnel_60_val = fresnel_60_obstructed

                        if pred is not None:
                            pred_f = abs(float(pred)) * -1
                            rssi_f = float(rssi)
                            diff = pred_f - rssi_f

                            per_site[f]["diff_values"].append(diff)
                            per_site[f]["x"].append(idx)
                            per_site[f]["rssi"].append(rssi_f)
                            per_site[f]["pred"].append(pred_f)
                            per_site[f]["diff"].append(diff)
                            if fresnel_60_obstructed is True:
                                per_site[f]["fresnel_60_obstructed_x"].append(idx)
                                per_site[f]["fresnel_60_obstructed_diff"].append(diff)
                            elif fresnel_obstructed is True:
                                per_site[f]["first_fresnel_obstructed_x"].append(idx)
                                per_site[f]["first_fresnel_obstructed_diff"].append(
                                    diff
                                )
                            elif path_obstructed is True:
                                per_site[f]["los_obstructed_x"].append(idx)
                                per_site[f]["los_obstructed_diff"].append(diff)
                            else:
                                per_site[f]["los_fresnel_clear_x"].append(idx)
                                per_site[f]["los_fresnel_clear_diff"].append(diff)

                    except Exception as exc:
                        per_site[f]["failed"] += 1
                        print(
                            f"Row {idx} site {f}: LOS request failed: {exc}",
                            file=sys.stderr,
                        )

                    out_row += [
                        rssi,
                        pred,
                        los_obstructed_val,
                        first_fresnel_val,
                        fresnel_60_val,
                    ]
                    if not args.geojson_only:
                        completed_requests += 1
                        if total_requests > 0:
                            elapsed = time.monotonic() - start_time
                            avg = elapsed / completed_requests
                            remaining = (total_requests - completed_requests) * avg
                            percent = (completed_requests / total_requests) * 100
                            print(
                                f"Progress: {percent:.1f}% ({completed_requests}/{total_requests}) "
                                f"ETA {format_duration(remaining)}",
                                file=sys.stderr,
                            )

                writer.writerow(out_row)

    if not args.geojson_only:
        with open(output_txt_path, "w", encoding="utf-8") as out_txt:
            # Per-site stats + per-site plots
            for s in detected_sites:
                f = s["rssi_field"]
                st = per_site[f]

                if st["diff_values"]:
                    abs_vals = [abs(v) for v in st["diff_values"]]
                    mean_abs = sum(abs_vals) / len(abs_vals)
                    mean_err = sum(st["diff_values"]) / len(st["diff_values"])
                    max_abs = max(abs_vals)
                    rmse = math.sqrt(
                        sum(v * v for v in st["diff_values"]) / len(st["diff_values"])
                    )
                    print(f"RSSI stats ({f}):", file=out_txt)
                    print(f"count={len(st['diff_values'])}", file=out_txt)
                    print(f"mean_abs_error={mean_abs:.3f}", file=out_txt)
                    print(f"mean_error={mean_err:.3f}", file=out_txt)
                    print(f"max_abs_error={max_abs:.3f}", file=out_txt)
                    print(f"rmse={rmse:.3f}", file=out_txt)
                print(
                    f"Rows ({f}): completed={st['completed']} failed={st['failed']} skipped_no_rssi={st['skipped_no_rssi']}",
                    file=out_txt,
                )
                print("", file=out_txt)

                # !xxxx_diff.png
                save_series_plot(
                    st["x"],
                    st["diff"],
                    title=f"{f} GW, diff (pred - measured) RSSI",
                    xlabel="ID",
                    ylabel="RSSI diff (dB)",
                    out_png=str(output_dir / f"{f}_diff.png"),
                    green_x=st["los_fresnel_clear_x"],
                    green_y=st["los_fresnel_clear_diff"],
                    red_x=st["fresnel_60_obstructed_x"],
                    red_y=st["fresnel_60_obstructed_diff"],
                    orange_x=st["first_fresnel_obstructed_x"],
                    orange_y=st["first_fresnel_obstructed_diff"],
                    yellow_x=st["los_obstructed_x"],
                    yellow_y=st["los_obstructed_diff"],
                )

                # !xxxx_val.png  (CSV RSSI + predicted RSSI)
                save_two_series_plot(
                    st["x"],
                    st["rssi"],
                    st["pred"],
                    label1="measured",
                    label2="predicted",
                    title=f"{f} GW received values",
                    xlabel="ID",
                    ylabel="RSSI (dBm)",
                    out_png=str(output_dir / f"{f}_val.png"),
                )

            if len(detected_sites) > 1:
                # all_sites_diff.png  -> 3 lines (diff per site), X=row ID
                diff_series = []
                for s in detected_sites:
                    f = s["rssi_field"]
                    diff_series.append(
                        {
                            "x": per_site[f]["x"],
                            "y": per_site[f]["diff"],
                            "label": f"{f} diff",
                        }
                    )
                save_multi_series_plot(
                    diff_series,
                    title="All sites: diff (pred - measured) RSSI",
                    xlabel="ID",
                    ylabel="RSSI diff (dB)",
                    out_png=str(output_dir / "all_sites_diff.png"),
                )

                # all_sites_rssi.png -> 6 lines (csv + predicted for each site), X=row ID
                rssi_series = []
                for s in detected_sites:
                    f = s["rssi_field"]
                    rssi_series.append(
                        {
                            "x": per_site[f]["x"],
                            "y": per_site[f]["rssi"],
                            "label": f"{f} csv",
                        }
                    )
                    rssi_series.append(
                        {
                            "x": per_site[f]["x"],
                            "y": per_site[f]["pred"],
                            "label": f"{f} pred",
                        }
                    )
                save_multi_series_plot(
                    rssi_series,
                    title="ALL sites: RSSI (csv) + predicted",
                    xlabel="ID (row)",
                    ylabel="dBm",
                    out_png=str(output_dir / "all_sites_rssi.png"),
                )

    print(f"Rows: total_with_coords={rows_with_coords}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
