#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import time
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    "itm_mode": True,
}


@dataclass
class ApiConfig:
    base_url: str
    poll_interval: float = 1
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
        st = status.get("status")
        if st == "completed":
            return status
        if st == "failed":
            raise RuntimeError(status.get("error", "Task failed"))
        time.sleep(api.poll_interval)
    raise TimeoutError(f"Task {task_id} timed out after {api.poll_timeout}s")


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


def new_site_stats() -> Dict[str, Any]:
    return {
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


def run_los_request(
    api: ApiConfig, payload: Dict[str, Any]
) -> Dict[str, Optional[Any]]:
    try:
        submit = http_json(f"{api.base_url}/los", payload, api.request_timeout)
        task_id = submit["task_id"]
        status = poll_task(api, task_id)
        if "data" in status and status["data"]:
            data = json.loads(status["data"])
            return {
                "ok": True,
                "pred": data.get("rx_signal_power"),
                "path_obstructed": normalize_bool(
                    data.get("path", {}).get("obstructed")
                ),
                "fresnel_obstructed": normalize_bool(
                    data.get("first_fresnel", {}).get("obstructed")
                ),
                "fresnel_60_obstructed": normalize_bool(
                    data.get("freshnel_60", data.get("fresnel_60", {})).get(
                        "obstructed"
                    )
                ),
            }
        return {"ok": True, "pred": None}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


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
    p.add_argument(
        "--parallel",
        "-p",
        type=int,
        default=6,
        help="Number of parallel LOS requests (0 = sequential)",
    )
    return p.parse_args()


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

    _scatter_if(
        ax,
        green_x or [],
        green_y or [],
        color="green",
        s=16,
        zorder=3,
        label="No obstructions",
    )
    _scatter_if(
        ax,
        red_x or [],
        red_y or [],
        color="red",
        s=16,
        zorder=3,
        label="LOS obstructed",
    )
    _scatter_if(
        ax,
        orange_x or [],
        orange_y or [],
        color="orange",
        s=16,
        zorder=3,
        label="Fresnel 60 obstructed",
    )
    _scatter_if(
        ax,
        yellow_x or [],
        yellow_y or [],
        color="yellow",
        s=16,
        zorder=3,
        label="First Fresnel obstructed",
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if any(
        [
            (green_x and green_y),
            (red_x and red_y),
            (orange_x and orange_y),
            (yellow_x and yellow_y),
        ]
    ):
        ax.legend()

    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    plt.close(fig)
    print(f"Wrote plot: {out_png}", file=stderr)


def save_two_series_plot(
    x, y1, y2, label1, label2, title, xlabel, ylabel, out_png, stderr=sys.stderr
):
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


def write_geojson(csv_path: Path, out_path: Path) -> int:
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("Input file has no header row.")
        if LAT_FIELD not in reader.fieldnames or LON_FIELD not in reader.fieldnames:
            raise ValueError(f"Missing required columns. Found: {reader.fieldnames}")

        features = []
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

            props = dict(row)
            props["row"] = idx
            props["lat"] = csv_lat
            props["lon"] = csv_lon

            features.append(
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [csv_lon, csv_lat]},
                    "properties": props,
                }
            )

    out = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as out_fh:
        json.dump(out, out_fh, ensure_ascii=True)
    return len(features)


def main() -> int:
    args = parse_args()
    api = ApiConfig(base_url=API_URL.rstrip("/"))

    rows_with_coords = 0
    detected_sites = []
    per_site: Dict[str, Dict[str, Any]] = {}

    csv_path = resolve_csv_path(args.input_path)
    output_dir = csv_path.parent

    output_csv_path = output_dir / "analyze.csv"
    output_txt_path = output_dir / "analyze.txt"
    output_geojson_path = output_dir / "analyze.geojson"

    if args.geojson_only:
        try:
            count = write_geojson(csv_path, output_geojson_path)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Wrote GeoJSON: {output_geojson_path} ({count} points)", file=sys.stderr)
        return 0

    # -----------------------------------------------------------------------
    # no-prediction: rebuild plots/stats from analyze.csv
    # -----------------------------------------------------------------------
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

        detected_sites = [
            s for s in RX_SITES if f"{s['rssi_field']}_mesaured_rssi" in header
        ]

        # ensure obstruction columns exist
        for s in detected_sites:
            f = s["rssi_field"]
            for col in (
                f"{f}_los_obstructed",
                f"{f}_first_fresnel_obstructed",
                f"{f}_fresnel_60_obstructed",
            ):
                if col not in header:
                    header.append(col)

        # remove legacy diff columns if present
        header = [col for col in header if not col.endswith("_rssi_diff")]

        for s in detected_sites:
            per_site[s["rssi_field"]] = new_site_stats()

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
                    st = per_site[f]

                    rssi = parse_optional_float(row.get(f"{f}_mesaured_rssi"))
                    pred = parse_optional_float(row.get(f"{f}_predicted_rssi"))

                    if rssi is None:
                        st["skipped_no_rssi"] += 1
                        continue

                    if pred is None:
                        continue

                    diff = pred - rssi

                    st["completed"] += 1
                    st["diff_values"].append(diff)
                    st["x"].append(x_val)
                    st["rssi"].append(rssi)
                    st["pred"].append(pred)
                    st["diff"].append(diff)

                    los_obstructed = normalize_bool(row.get(f"{f}_los_obstructed"))
                    first_fresnel_obstructed = normalize_bool(
                        row.get(f"{f}_first_fresnel_obstructed")
                    )
                    fresnel_60_obstructed = normalize_bool(
                        row.get(f"{f}_fresnel_60_obstructed")
                    )

                    if los_obstructed is True:
                        st["los_obstructed_x"].append(x_val)
                        st["los_obstructed_diff"].append(diff)
                    elif fresnel_60_obstructed is True:
                        st["fresnel_60_obstructed_x"].append(x_val)
                        st["fresnel_60_obstructed_diff"].append(diff)
                    elif first_fresnel_obstructed is True:
                        st["first_fresnel_obstructed_x"].append(x_val)
                        st["first_fresnel_obstructed_diff"].append(diff)
                    elif (
                        los_obstructed is False
                        and first_fresnel_obstructed is False
                        and fresnel_60_obstructed is False
                    ):
                        st["los_fresnel_clear_x"].append(x_val)
                        st["los_fresnel_clear_diff"].append(diff)

                writer.writerow([row.get(col) for col in header])

    # -----------------------------------------------------------------------
    # prediction mode: read raw csv and call API (unless geojson-only)
    # -----------------------------------------------------------------------
    else:
        existing_rows = {}
        if args.geojson_only and output_csv_path.exists():
            with open(output_csv_path, newline="", encoding="utf-8") as existing_fh:
                existing_reader = csv.DictReader(existing_fh)
                for row in existing_reader:
                    row_id = (row.get("row") or "").strip()
                    if row_id:
                        existing_rows[row_id] = row

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

            header = ["row", "lat", "lon"]
            for s in detected_sites:
                f = s["rssi_field"]
                header += [
                    f"{f}_mesaured_rssi",
                    f"{f}_predicted_rssi",
                    f"{f}_los_obstructed",
                    f"{f}_fresnel_60_obstructed",
                    f"{f}_first_fresnel_obstructed",
                ]
            writer.writerow(header)

            for s in detected_sites:
                per_site[s["rssi_field"]] = new_site_stats()

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
            last_progress_t = start_time
    
            if args.parallel and args.parallel > 0 and not args.geojson_only:
                rows = []
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
    
                    rssi_by_site = {}
                    for s in detected_sites:
                        f = s["rssi_field"]
                        rssi = parse_optional_float(row.get(f))
                        rssi_by_site[f] = rssi
                        if rssi is None:
                            st = per_site[f]
                            st["skipped_no_rssi"] += 1
    
                    rows.append({
                        "idx": idx,
                        "csv_lat": csv_lat,
                        "csv_lon": csv_lon,
                        "rssi_by_site": rssi_by_site,
                        "results": {},
                    })
    
                futures = {}
                with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                    for row in rows:
                        for s in detected_sites:
                            f = s["rssi_field"]
                            rssi = row["rssi_by_site"].get(f)
                            if rssi is None:
                                continue
                            payload = build_payload(
                                tx_lat=row["csv_lat"],
                                tx_lon=row["csv_lon"],
                                rx_lat=float(s["lat"]),
                                rx_lon=float(s["lon"]),
                                rx_height=float(s["rx_height"]),
                                rx_gain=float(s["rx_gain"]),
                                rx_loss=float(s["rx_loss"]),
                            )
                            future = executor.submit(run_los_request, api, payload)
                            futures[future] = (row, s, rssi)
    
                    for future in as_completed(futures):
                        row, s, rssi = futures[future]
                        f = s["rssi_field"]
                        pred = None
                        diff = None
                        path_obstructed = None
                        fresnel_obstructed = None
                        fresnel_60_obstructed = None
                        try:
                            result = future.result()
                            if result.get("ok"):
                                pred = result.get("pred")
                                path_obstructed = result.get("path_obstructed")
                                fresnel_obstructed = result.get("fresnel_obstructed")
                                fresnel_60_obstructed = result.get("fresnel_60_obstructed")
                                st = per_site[f]
                                st["completed"] += 1
                            else:
                                per_site[f]["failed"] += 1
                                error = result.get("error", "LOS request failed")
                                print(
                                    f"Row {row['idx']} site {f}: LOS request failed: {error}",
                                    file=sys.stderr,
                                )
                        except Exception as exc:
                            per_site[f]["failed"] += 1
                            print(
                                f"Row {row['idx']} site {f}: LOS request failed: {exc}",
                                file=sys.stderr,
                            )
    
                        if pred is not None:
                            pred_f = abs(float(pred)) * -1
                            rssi_f = float(rssi)
                            diff = pred_f - rssi_f
    
                            st = per_site[f]
                            st["diff_values"].append(diff)
                            st["x"].append(row["idx"])
                            st["rssi"].append(rssi_f)
                            st["pred"].append(pred_f)
                            st["diff"].append(diff)
                            if path_obstructed is True:
                                st["los_obstructed_x"].append(row["idx"])
                                st["los_obstructed_diff"].append(diff)
                            elif fresnel_60_obstructed is True:
                                st["fresnel_60_obstructed_x"].append(row["idx"])
                                st["fresnel_60_obstructed_diff"].append(diff)
                            elif fresnel_obstructed is True:
                                st["first_fresnel_obstructed_x"].append(row["idx"])
                                st["first_fresnel_obstructed_diff"].append(diff)
                            else:
                                st["los_fresnel_clear_x"].append(row["idx"])
                                st["los_fresnel_clear_diff"].append(diff)
    
                        row["results"][f] = (
                            pred,
                            path_obstructed,
                            fresnel_obstructed,
                            fresnel_60_obstructed,
                        )
    
                        completed_requests += 1
                        now = time.monotonic()
                        if total_requests > 0 and (
                            now - last_progress_t >= 1.0 or completed_requests % 25 == 0
                        ):
                            elapsed = now - start_time
                            avg = elapsed / completed_requests
                            remaining = (total_requests - completed_requests) * avg
                            percent = (completed_requests / total_requests) * 100
                            print(
                                f"Progress: {percent:.1f}% ({completed_requests}/{total_requests}) "
                                f"ETA {format_duration(remaining)}",
                                file=sys.stderr,
                            )
                            last_progress_t = now
    
                for row in rows:
                    out_row = [row["idx"], row["csv_lat"], row["csv_lon"]]
                    for s in detected_sites:
                        f = s["rssi_field"]
                        rssi = row["rssi_by_site"].get(f)
                        pred, path_obstructed, fresnel_obstructed, fresnel_60_obstructed = (
                            row["results"].get(f, (None, None, None, None))
                        )
                        out_row += [
                            rssi,
                            pred,
                            path_obstructed,
                            fresnel_obstructed,
                            fresnel_60_obstructed,
                        ]
                    writer.writerow(out_row)
            else:
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
    
                    if args.geojson_only:
                        existing = existing_rows.get(str(idx)) or existing_rows.get(
                            str(int(idx))
                        )
                        pred_val = None
                        los_val = None
                        fresnel_60_val = None
                        first_fresnel_val = None
                        if existing:
                            pred_val = parse_optional_float(
                                existing.get(f"{f}_predicted_rssi")
                            )
                            los_val = normalize_bool(
                                existing.get(f"{f}_los_obstructed")
                            )
                            fresnel_60_val = normalize_bool(
                                existing.get(f"{f}_fresnel_60_obstructed")
                            )
                            first_fresnel_val = normalize_bool(
                                existing.get(f"{f}_first_fresnel_obstructed")
                            )
                        out_row += [
                            rssi,
                            pred_val,
                            los_val,
                            fresnel_60_val,
                            first_fresnel_val,
                        ]
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
                            st = per_site[f]
                            st["completed"] += 1
    
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
                                        "freshnel_60", data.get("fresnel_60", {})
                                    ).get("obstructed")
                                )
    
                            if pred is not None:
                                pred_f = abs(float(pred)) * -1
                                rssi_f = float(rssi)
                                diff = pred_f - rssi_f
    
                                st["diff_values"].append(diff)
                                st["x"].append(idx)
                                st["rssi"].append(rssi_f)
                                st["pred"].append(pred_f)
                                st["diff"].append(diff)
    
                                if path_obstructed is True:
                                    st["los_obstructed_x"].append(idx)
                                    st["los_obstructed_diff"].append(diff)
                                elif fresnel_60_obstructed is True:
                                    st["fresnel_60_obstructed_x"].append(idx)
                                    st["fresnel_60_obstructed_diff"].append(diff)
                                elif fresnel_obstructed is True:
                                    st["first_fresnel_obstructed_x"].append(idx)
                                    st["first_fresnel_obstructed_diff"].append(diff)
                                else:
                                    st["los_fresnel_clear_x"].append(idx)
                                    st["los_fresnel_clear_diff"].append(diff)
    
                        except Exception as exc:
                            per_site[f]["failed"] += 1
                            print(
                                f"Row {idx} site {f}: LOS request failed: {exc}",
                                file=sys.stderr,
                            )
    
                        out_row += [
                            rssi,
                            pred,
                            path_obstructed,
                            fresnel_obstructed,
                            fresnel_60_obstructed,
                        ]
    
                        completed_requests += 1
                        now = time.monotonic()
                        if total_requests > 0 and (
                            now - last_progress_t >= 1.0 or completed_requests % 25 == 0
                        ):
                            elapsed = now - start_time
                            avg = elapsed / completed_requests
                            remaining = (total_requests - completed_requests) * avg
                            percent = (completed_requests / total_requests) * 100
                            print(
                                f"Progress: {percent:.1f}% ({completed_requests}/{total_requests}) "
                                f"ETA {format_duration(remaining)}",
                                file=sys.stderr,
                            )
                            last_progress_t = now
    
                    writer.writerow(out_row)

    # -----------------------------------------------------------------------
    # stats + plots
    # -----------------------------------------------------------------------
    if not args.geojson_only:
        with open(output_txt_path, "w", encoding="utf-8") as out_txt:
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

                save_series_plot(
                    st["x"],
                    st["diff"],
                    title=f"{f} GW, diff (pred - measured) RSSI",
                    xlabel="ID",
                    ylabel="RSSI diff (dB)",
                    out_png=str(output_dir / f"{f}_diff.png"),
                    green_x=st["los_fresnel_clear_x"],
                    green_y=st["los_fresnel_clear_diff"],
                    yellow_x=st["fresnel_60_obstructed_x"],
                    yellow_y=st["fresnel_60_obstructed_diff"],
                    orange_x=st["first_fresnel_obstructed_x"],
                    orange_y=st["first_fresnel_obstructed_diff"],
                    red_x=st["los_obstructed_x"],
                    red_y=st["los_obstructed_diff"],
                )

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
