import numpy as np


def add_white_noise(signal, snr_db):

    signal_power = np.mean(np.abs(signal)**2)

    snr_linear = 10**(snr_db / 10)
    noise_power = signal_power / snr_linear

    noise_std = np.sqrt(noise_power / 2)

    noise = (
        np.random.normal(0, noise_std, signal.shape)
        + 1j*np.random.normal(0, noise_std, signal.shape)
    )

    return signal + noise
