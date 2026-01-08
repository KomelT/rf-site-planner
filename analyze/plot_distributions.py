#!/usr/bin/env python3
import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def resolve_csv_path(folder: Path) -> Path:
    if not folder.exists():
        raise FileNotFoundError(f"Input path not found: {folder}")
    if folder.is_file():
        return folder
    csv_files = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".csv")
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
    ax_box.xaxis.set_major_locator(MultipleLocator(1))
    ax_box.tick_params(axis="x", labelsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return True


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate per-column distribution plots for CSV columns starting with '!'."
    )
    p.add_argument("folder", help="Folder containing a single CSV (or a CSV path)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
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
