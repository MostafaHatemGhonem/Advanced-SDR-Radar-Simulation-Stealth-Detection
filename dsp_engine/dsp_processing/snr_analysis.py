import numpy as np
from .noise import add_white_noise
from .windowing import apply_hamming
from .range_processing import compute_range_fft, estimate_range


def run_snr_analysis(beat_signal, true_range, snr_values):

    results = []

    for snr in snr_values:

        noisy = add_white_noise(beat_signal, snr)
        windowed = apply_hamming(noisy)

        spectrum, ranges = compute_range_fft(windowed)
        estimated_range = estimate_range(spectrum, ranges)

        error = abs(estimated_range - true_range)

        detection_ok = error <= 1.0  # within 1 meter resolution

        results.append({
            "snr_db": snr,
            "estimated_range": float(estimated_range),
            "error": float(error),
            "detected": bool(detection_ok)
        })

    return results
