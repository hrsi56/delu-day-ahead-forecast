import numpy as np

from delu_forecast.spectral import annotate_peaks, welch_periodogram


def test_spectral_labels_land_within_one_fft_bin() -> None:
    hours = np.arange(4096)
    signal = np.sin(2 * np.pi * hours / 24) + 0.5 * np.sin(2 * np.pi * hours / 168)
    frequencies, power = welch_periodogram(signal, nperseg=512)
    labels = annotate_peaks(frequencies, power).set_index("period_hours")
    assert {24, 168}.issubset(labels.index)
    assert (labels.loc[[24, 168], "bin_error"] <= labels.loc[[24, 168], "fft_bin_width"]).all()
