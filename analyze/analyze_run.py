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
    {"name": "HQ", "lat": 45.8435599, "lon": 13.73427, "rssi_field": "!75f19024", "rx_height": 15.0, "rx_gain": 6.5, "rx_loss": 0.0},
    {"name": "SV. Katarina", "lat": 45.85474, "lon": 13.72615, "rssi_field": "!7369fb6a", "rx_height": 3.0, "rx_gain": 5.0, "rx_loss": 0.0},
    {"name": "Mobil", "lat": 45.8463800779, "lon": 13.7232441999, "rssi_field": "!da5ad56c", "rx_height": 2.0, "rx_gain": 6.5, "rx_loss": 0.0},
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


def http_json(url: str, payload: Optional[Dict[str, Any]], timeout: float) -> Dict[str, Any]:
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
    return p.parse_args()


def save_series_plot(x, y, title, xlabel, ylabel, out_png, stderr=sys.stderr):
    if not x:
        return
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_two_series_plot(x, y1, y2, label1, label2, title, xlabel, ylabel, out_png, stderr=sys.stderr):
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

    with open(csv_path, newline="", encoding="utf-8") as fh, open(
        output_csv_path, "w", newline="", encoding="utf-8"
    ) as out_csv:
        reader = csv.DictReader(fh)
        writer = csv.writer(out_csv)
        if not reader.fieldnames:
            print("Input file has no header row.", file=sys.stderr)
            return 1

        if LAT_FIELD not in reader.fieldnames or LON_FIELD not in reader.fieldnames:
            print(f"Missing required columns. Found: {reader.fieldnames}", file=sys.stderr)
            return 1

        detected_sites = [s for s in RX_SITES if s["rssi_field"] in reader.fieldnames]

        # Output CSV header (only detected RX sites)
        header = ["row", "lat", "lon"]
        for s in detected_sites:
            f = s["rssi_field"]
            header += [f"{f}_mesaured_rssi", f"{f}_predicted_rssi", f"{f}_rssi_diff"]
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
            }

        total_requests = 0
        if not args.geojson_only:
            with open(csv_path, newline="", encoding="utf-8") as count_fh:
                count_reader = csv.DictReader(count_fh)
                for row in count_reader:
                    lat_val = (row.get(LAT_FIELD) or "").strip().strip('"').strip("'")
                    lon_val = (row.get(LON_FIELD) or "").strip().strip('"').strip("'")
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

                if args.geojson_only:
                    out_row += [rssi, None, None]
                    continue

                if rssi is None:
                    per_site[f]["skipped_no_rssi"] += 1
                    out_row += [None, None, None]
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
                    submit = http_json(f"{api.base_url}/los", payload, api.request_timeout)
                    task_id = submit["task_id"]
                    status = poll_task(api, task_id)
                    per_site[f]["completed"] += 1

                    if "data" in status and status["data"]:
                        data = json.loads(status["data"])
                        pred = data.get("rx_signal_power")

                    if pred is not None:
                        pred_f = abs(float(pred)) * -1
                        rssi_f = float(rssi)
                        diff = pred_f - rssi_f

                        per_site[f]["diff_values"].append(diff)
                        per_site[f]["x"].append(idx)
                        per_site[f]["rssi"].append(rssi_f)
                        per_site[f]["pred"].append(pred_f)
                        per_site[f]["diff"].append(diff)

                except Exception as exc:
                    per_site[f]["failed"] += 1
                    print(f"Row {idx} site {f}: LOS request failed: {exc}", file=sys.stderr)

                out_row += [rssi, pred, diff]
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
                    rmse = math.sqrt(sum(v * v for v in st["diff_values"]) / len(st["diff_values"]))
                    print(f"RSSI stats ({f}):", file=out_txt)
                    print(f"count={len(st['diff_values'])}", file=out_txt)
                    print(f"mean_abs_error={mean_abs:.3f}", file=out_txt)
                    print(f"mean_error={mean_err:.3f}", file=out_txt)
                    print(f"max_abs_error={max_abs:.3f}", file=out_txt)
                    print(f"rmse={rmse:.3f}", file=out_txt)
                    print("", file=out_txt)
                print(
                    f"Rows ({f}): completed={st['completed']} failed={st['failed']} skipped_no_rssi={st['skipped_no_rssi']}",
                    file=out_txt,
                )

                # !xxxx_diff.png
                save_series_plot(
                    st["x"],
                    st["diff"],
                    title=f"{f} GW, diff (pred - measured) RSSI",
                    xlabel="ID",
                    ylabel="RSSI diff (dB)",
                    out_png=str(output_dir / f"{f}_diff.png"),
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
                        {"x": per_site[f]["x"], "y": per_site[f]["diff"], "label": f"{f} diff"}
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
                    rssi_series.append({"x": per_site[f]["x"], "y": per_site[f]["rssi"], "label": f"{f} csv"})
                    rssi_series.append({"x": per_site[f]["x"], "y": per_site[f]["pred"], "label": f"{f} pred"})
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
