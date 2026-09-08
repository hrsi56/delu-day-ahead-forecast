# CP-1 spectral artifacts

These three figures use only price rows eligible for development EDA: delivery
2019-01-01 through Fold 5's end, 2026-04-07. The final-calibration slice,
Embargo B, and the 90-day holdout are excluded by the committed
`data/partitions.json` contract.

- `fig_welch_periodogram.png`: detrended price Welch PSD, Hann window, 50%
  overlap, `nperseg=512`, with 24h/168h/12h labels.
- `fig_per_regime_periodogram.png`: the same estimate for pre-crisis, crisis,
  and normalization regimes.
- `fig_acf_24_168.png`: detrended price autocorrelation with 24h and 168h
  reference lines.
- `spectral_peak_bins.csv`: exact FFT bins used for the labels.

Reproduce with `make spectral`. The labels are checked by the ordinary
repository test `tests/test_07_spectral_labels.py`.
