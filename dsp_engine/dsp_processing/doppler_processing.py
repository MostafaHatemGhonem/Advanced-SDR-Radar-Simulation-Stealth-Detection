import numpy as np
import config


def compute_doppler_fft(range_bin_matrix):
    doppler_fft = np.fft.fftshift(
        np.fft.fft(range_bin_matrix, axis=0)
    )

    doppler_spectrum = np.abs(doppler_fft)

    num_chirps = range_bin_matrix.shape[0]

    doppler_freq = np.fft.fftshift(
        np.fft.fftfreq(num_chirps, d=config.TC)
    )

    velocities = (doppler_freq * config.LAMBDA) / 2

    return doppler_spectrum, velocities
