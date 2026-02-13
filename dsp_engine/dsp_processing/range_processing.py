import numpy as np
import config


def compute_range_fft(beat_signal):

    fft_result = np.fft.fft(beat_signal)
    spectrum = np.abs(fft_result)

    freqs = np.fft.fftfreq(len(beat_signal), d=1/config.FS)

    # FMCW range conversion
    ranges = (config.C * freqs) / (2 * config.SLOPE)

    return spectrum, ranges


def estimate_range(spectrum, ranges):
    peak_index = np.argmax(spectrum)
    return ranges[peak_index]
