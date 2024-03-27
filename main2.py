import csv
from scipy.io.wavfile import write
import numpy as np
from scipy.signal import butter, sosfilt

# Specify the file name
file_name = "2022_04_22_hour_heartbeat_merged.csv"
sample_rate = 44100
duration_per_heartbeat = 0.2  # Duration in seconds


def butter_bandpass(lowcut, highcut, fs, order=5):
    sos = butter(order, [lowcut, highcut], btype="band", fs=fs, output="sos")
    return sos


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y


def frequency_range_from_heartbeat(heartbeat):
    # This function determines the frequency range for the bandpass filter
    # based on the heartbeat. You can adjust the formula to your liking.
    base_freq = 200 + (heartbeat - 60) * (600 / (115 - 60))
    return max(20, base_freq - 50), min(sample_rate / 2, base_freq + 50)


# Base white noise generation
base_noise_duration = int(sample_rate * duration_per_heartbeat)  # for each segment
base_noise = np.random.normal(0, 1, base_noise_duration)

all_filtered_noise_segments = []

with open(file_name, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        heartbeat = int(row[1])
        lowcut, highcut = frequency_range_from_heartbeat(heartbeat)
        filtered_noise = butter_bandpass_filter(
            base_noise, lowcut, highcut, sample_rate
        )
        all_filtered_noise_segments.append(filtered_noise)

# Concatenate all filtered noise segments and normalize
full_noise_wave = np.concatenate(all_filtered_noise_segments).astype(np.float32)
full_noise_wave *= 32767 / np.max(
    np.abs(full_noise_wave)
)  # Normalize to the range of int16
full_noise_wave = full_noise_wave.astype(np.int16)

# Write the resulting waveform to a WAV file
write("heartbeat_modulated_white_noise.wav", sample_rate, full_noise_wave)
