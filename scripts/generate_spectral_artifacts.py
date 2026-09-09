#!/usr/bin/env python3
"""Generate the three bounded CP-1 spectral figures from EDA-eligible rows."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from delu_forecast.partitions import pin_partition_spec
from delu_forecast.spectral import annotate_peaks, autocorrelation, welch_periodogram

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, default=ROOT / "data" / "snapshot.parquet")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = pd.read_parquet(args.snapshot)
    frame["timestamp_utc"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    cutoff = max(frame["delivery_date"])
    if not isinstance(cutoff, date):
        cutoff = pd.Timestamp(cutoff).date()
    spec = pin_partition_spec(cutoff)
    eda = frame.loc[frame["delivery_date"] <= spec["eda_cutoff"]].copy()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    frequencies, power = welch_periodogram(eda["price_eur_mwh"], nperseg=512)
    peaks = annotate_peaks(frequencies, power)
    peaks.to_csv(args.output_dir / "spectral_peak_bins.csv", index=False)
    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.semilogy(frequencies[1:], power[1:], color="#235789", linewidth=1.1)
    for row in peaks.itertuples():
        axis.axvline(row.bin_frequency_hz_per_hour, color="#d95f02", alpha=0.65, linestyle="--")
        axis.annotate(row.label, (row.bin_frequency_hz_per_hour, row.power), xytext=(5, 8), textcoords="offset points")
    axis.set(xlabel="Frequency (cycles/hour)", ylabel="Welch PSD", title="DE-LU day-ahead price: Welch periodogram")
    axis.set_xlim(0, 0.11)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(args.output_dir / "fig_welch_periodogram.png", dpi=160)
    plt.close(figure)

    delivery = pd.to_datetime(eda["delivery_date"])
    regimes = {
        "Pre-crisis": delivery < pd.Timestamp("2021-09-01"),
        "Crisis": (delivery >= pd.Timestamp("2021-09-01")) & (delivery <= pd.Timestamp("2022-12-31")),
        "Normalization": delivery >= pd.Timestamp("2023-01-01"),
    }
    figure, axis = plt.subplots(figsize=(10, 5.5))
    for label, mask in regimes.items():
        regime_f, regime_p = welch_periodogram(eda.loc[mask, "price_eur_mwh"], nperseg=512)
        axis.semilogy(regime_f[1:], regime_p[1:], linewidth=1.1, label=label)
    for period in (24, 168, 12):
        axis.axvline(1 / period, color="black", alpha=0.18, linestyle="--")
    axis.set(xlabel="Frequency (cycles/hour)", ylabel="Welch PSD", title="Price spectrum by market regime")
    axis.set_xlim(0, 0.11)
    axis.legend()
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(args.output_dir / "fig_per_regime_periodogram.png", dpi=160)
    plt.close(figure)

    acf = autocorrelation(eda["price_eur_mwh"], max_lag=336)
    figure, axis = plt.subplots(figsize=(10, 5.5))
    axis.plot(np.arange(len(acf)), acf, color="#235789", linewidth=1.0)
    for lag in (24, 168):
        axis.axvline(lag, color="#d95f02", linestyle="--", alpha=0.75, label=f"{lag}h")
    axis.set(xlabel="Lag (hours)", ylabel="Autocorrelation", title="Detrended price ACF with daily and weekly references")
    axis.legend()
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(args.output_dir / "fig_acf_24_168.png", dpi=160)
    plt.close(figure)
    print(f"Generated spectral artifacts from {len(eda):,} EDA-eligible hourly rows through {spec['eda_cutoff']}")


if __name__ == "__main__":
    main()
