#!/usr/bin/env python3
import argparse
import csv
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from urllib.request import Request, urlopen

API_URL = "http://localhost:8081"
API_REQUEST_TIMEOUT = 30.0
API_POLL_TIMEOUT = 600.0

POLL_INITIAL = 0.2
POLL_AFTER_5S = 0.5
POLL_AFTER_20S = 1.0

DEFAULTS = {
    "tx_height": 3.0,
    "tx_power": 27.0,
    "tx_gain": 5.0,
    "tx_loss": 0,
    "rx_gain": 6.5,
    "rx_loss": 0,
    "rx_height": 15.0,
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


def resolve_csv_path(folder: Path) -> Path:
    if not folder.exists():
        raise FileNotFoundError(f"Input path not found: {folder}")
    if folder.is_file():
        return folder
    csv_files = sorted(
        p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".csv"
    )
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder}")
    if len(csv_files) > 1:
        raise ValueError(f"Multiple CSV files found in folder: {folder}")
    return csv_files[0]


def parse_float(value):
    if value is None:
        return None
    s = str(value).strip().strip('"').strip("'")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in name)


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


def poll_task(api_url: str, task_id: str) -> Dict[str, Any]:
    start = time.monotonic()
    deadline = start + API_POLL_TIMEOUT
    while time.monotonic() < deadline:
        status = http_json(f"{api_url}/task/{task_id}", None, API_REQUEST_TIMEOUT)
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


def run_los_request(api_url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    submit = http_json(f"{api_url}/los", payload, API_REQUEST_TIMEOUT)
    task_id = submit["task_id"]
    status = poll_task(api_url, task_id)
    if "data" not in status or not status["data"]:
        return {"ok": True, "pred": None, "path_loss_rssi": None}
    data = json.loads(status["data"])
    return {
        "ok": True,
        "pred": data.get("rx_signal_power"),
        "path_loss_rssi": data.get("path_loss_rssi"),
    }


def build_payload(
    args: argparse.Namespace, situation: float, time_fraction: float
) -> Dict[str, Any]:
    payload = dict(DEFAULTS)
    payload.update(
        {
            "tx_lat": args.tx_lat,
            "tx_lon": args.tx_lon,
            "rx_lat": args.rx_lat,
            "rx_lon": args.rx_lon,
            "rx_height": args.rx_height,
            "rx_gain": args.rx_gain,
            "rx_loss": args.rx_loss,
            "tx_height": args.tx_height,
            "tx_power": args.tx_power,
            "tx_gain": args.tx_gain,
            "tx_loss": args.tx_loss,
            "frequency_mhz": args.frequency_mhz,
            "situation_fraction": situation,
            "time_fraction": time_fraction,
        }
    )
    return payload


def plot_distribution(values, title, out_path: Path):
    if not values:
        return False

    fig = plt.figure()
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])
    ax = fig.add_subplot(gs[0, 0])
    ax_box = fig.add_subplot(gs[1, 0], sharex=ax)

    counts, edges, _ = ax.hist(values, bins=30, color="#2f4b7c", alpha=0.25)
    centers = [(edges[i] + edges[i + 1]) / 2.0 for i in range(len(edges) - 1)]
    ax.plot(centers, counts, color="#2f4b7c", linewidth=2)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Count", fontsize=9)
    ax.tick_params(axis="both", labelsize=8)

    ax_box.boxplot(
        values,
        vert=False,
        widths=0.6,
        patch_artist=True,
        boxprops={"facecolor": "#2f4b7c", "alpha": 0.2},
    )
    ax_box.set_xlabel("Value", fontsize=9)
    ax_box.set_yticks([])
    ax_box.set_ylim(0.7, 1.3)
    ax_box.xaxis.set_major_locator(MultipleLocator(5))
    ax_box.tick_params(axis="x", labelsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return True


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate per-column distribution plots for CSV columns starting with '!'."
    )
    p.add_argument(
        "folder", help="Folder containing a single CSV (or output folder with -m)"
    )
    p.add_argument(
        "-m",
        "--model",
        action="store_true",
        help="Call API over situation/time grid and plot distribution",
    )
    p.add_argument(
        "-n",
        "--no-api",
        action="store_true",
        help="Read saved sweep CSV and only render plots",
    )
    p.add_argument("--api-url", default=API_URL, help="API base URL")
    p.add_argument(
        "--tx-lat",
        type=float,
        default=45.85473269336,
        help="TX latitude (required with -m)",
    )
    p.add_argument(
        "--tx-lon",
        type=float,
        default=13.72616645611,
        help="TX longitude (required with -m)",
    )
    p.add_argument(
        "--rx-lat",
        type=float,
        default=45.843544567,
        help="RX latitude (required with -m)",
    )
    p.add_argument(
        "--rx-lon",
        type=float,
        default=13.7343341751,
        help="RX longitude (required with -m)",
    )
    p.add_argument("--tx-height", type=float, default=DEFAULTS["tx_height"])
    p.add_argument("--tx-power", type=float, default=DEFAULTS["tx_power"])
    p.add_argument("--tx-gain", type=float, default=DEFAULTS["tx_gain"])
    p.add_argument("--tx-loss", type=float, default=DEFAULTS["tx_loss"])
    p.add_argument("--rx-height", type=float, default=15.0)
    p.add_argument("--rx-gain", type=float, default=6.5)
    p.add_argument("--rx-loss", type=float, default=0.0)
    p.add_argument("--frequency-mhz", type=float, default=DEFAULTS["frequency_mhz"])
    p.add_argument(
        "--parallel",
        "-p",
        type=int,
        default=6,
        help="Number of parallel LOS requests (0 = sequential)",
    )
    p.add_argument(
        "--queue-mult",
        type=int,
        default=4,
        help="Max in-flight = parallel * queue_mult",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.model and args.no_api:
        raise ValueError("Use either -m or -n, not both.")

    if args.no_api:
        output_dir = Path(args.folder)
        if output_dir.is_file():
            output_dir = output_dir.parent
        sweep_csv = output_dir / "model_sweep.csv"
        if not sweep_csv.exists():
            raise FileNotFoundError(f"Missing sweep CSV: {sweep_csv}")

        values_pred = []
        values_path = []
        tx_lat = tx_lon = rx_lat = rx_lon = None

        with open(sweep_csv, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames:
                raise ValueError("Sweep CSV has no header.")
            for row in reader:
                if tx_lat is None:
                    tx_lat = parse_float(row.get("tx_lat"))
                    tx_lon = parse_float(row.get("tx_lon"))
                    rx_lat = parse_float(row.get("rx_lat"))
                    rx_lon = parse_float(row.get("rx_lon"))
                pred = parse_float(row.get("predicted_rssi"))
                path = parse_float(row.get("path_loss_rssi"))
                if pred is not None:
                    values_pred.append(pred)
                if path is not None:
                    values_path.append(path)

        coord_note = ""
        if None not in (tx_lat, tx_lon, rx_lat, rx_lon):
            coord_note = f"\nTX({tx_lat:.5f},{tx_lon:.5f}) RX({rx_lat:.5f},{rx_lon:.5f})"

        if values_pred:
            plot_distribution(
                values_pred,
                f"Distribution: predicted RSSI (situation/time sweep){coord_note}",
                output_dir / "model_pred_distribution.png",
            )
        if values_path:
            plot_distribution(
                values_path,
                f"Distribution: path loss RSSI (situation/time sweep){coord_note}",
                output_dir / "fpls_pred_distribution.png",
            )
        return 0

    if args.model:
        output_dir = Path(args.folder)
        if output_dir.is_file():
            output_dir = output_dir.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        for field in ("tx_lat", "tx_lon", "rx_lat", "rx_lon"):
            if getattr(args, field) is None:
                raise ValueError(
                    f"Missing required argument for -m: --{field.replace('_', '-')}"
                )

        values_pred = []
        values_path = []
        total = 101 * 101
        completed = 0
        start = time.monotonic()
        sweep_rows = []

        def maybe_print_progress():
            nonlocal completed
            if completed % 250 == 0:
                elapsed = time.monotonic() - start
                avg = elapsed / max(1, completed)
                remaining = max(0, (total - completed)) * avg
                print(f"Progress: {completed}/{total} ETA ~{int(remaining)}s")

        def task_iter():
            for s in range(0, 101):
                for t in range(0, 101):
                    yield (float(s), float(t))

        tasks = task_iter()

        if args.parallel and args.parallel > 0:
            max_in_flight = args.parallel * max(1, args.queue_mult)
            in_flight: Dict[Any, Tuple[float, float]] = {}
            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                while len(in_flight) < max_in_flight:
                    try:
                        s, t = next(tasks)
                    except StopIteration:
                        break
                    payload = build_payload(args, s, t)
                    fut = executor.submit(run_los_request, args.api_url, payload)
                    in_flight[fut] = (s, t)

                while in_flight:
                    done, _ = wait(in_flight.keys(), return_when=FIRST_COMPLETED)
                    for fut in done:
                        in_flight.pop(fut)
                        try:
                            res = fut.result()
                            if res.get("ok"):
                                pred = res.get("pred")
                                path = res.get("path_loss_rssi")
                                if pred is not None:
                                    values_pred.append(float(pred))
                                if path is not None:
                                    values_path.append(float(path))
                                sweep_rows.append((s, t, pred, path))
                        except Exception:
                            pass
                        completed += 1
                        maybe_print_progress()

                        while len(in_flight) < max_in_flight:
                            try:
                                s, t = next(tasks)
                            except StopIteration:
                                break
                            payload = build_payload(args, s, t)
                            fut = executor.submit(
                                run_los_request, args.api_url, payload
                            )
                            in_flight[fut] = (s, t)
        else:
            for s, t in tasks:
                payload = build_payload(args, s, t)
                try:
                    res = run_los_request(args.api_url, payload)
                    if res.get("ok"):
                        pred = res.get("pred")
                        path = res.get("path_loss_rssi")
                        if pred is not None:
                            values_pred.append(float(pred))
                        if path is not None:
                            values_path.append(float(path))
                        sweep_rows.append((s, t, pred, path))
                except Exception:
                    pass
                completed += 1
                maybe_print_progress()

        if not values_pred and not values_path:
            raise ValueError("No prediction values received from API.")

        coord_note = f"TX({args.tx_lat:.5f},{args.tx_lon:.5f}) RX({args.rx_lat:.5f},{args.rx_lon:.5f})"

        sweep_csv = output_dir / "model_sweep.csv"
        with open(sweep_csv, "w", newline="", encoding="utf-8") as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(
                [
                    "situation_fraction",
                    "time_fraction",
                    "predicted_rssi",
                    "path_loss_rssi",
                    "tx_lat",
                    "tx_lon",
                    "rx_lat",
                    "rx_lon",
                ]
            )
            for s, t, pred, path in sweep_rows:
                writer.writerow([s, t, pred, path, args.tx_lat, args.tx_lon, args.rx_lat, args.rx_lon])

        if values_pred:
            plot_distribution(
                values_pred,
                f"Distribution: predicted RSSI (situation/time sweep)\n{coord_note}",
                output_dir / "model_pred_distribution.png",
            )
        if values_path:
            plot_distribution(
                values_path,
                f"Distribution: path loss RSSI (situation/time sweep)\n{coord_note}",
                output_dir / "fpls_pred_distribution.png",
            )
        return 0

    csv_path = resolve_csv_path(Path(args.folder))
    output_dir = csv_path.parent

    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("Input file has no header row.")

        target_fields = [f for f in reader.fieldnames if f.startswith("!")]
        if not target_fields:
            raise ValueError("No columns starting with '!' found.")

        values = {f: [] for f in target_fields}
        for row in reader:
            for f in target_fields:
                v = parse_float(row.get(f))
                if v is None or math.isnan(v) or math.isinf(v):
                    continue
                values[f].append(v)

    for f in target_fields:
        out_name = f"{safe_name(f)}_dist.png"
        out_path = output_dir / out_name
        plot_distribution(values[f], f"Distribution: {f}", out_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
