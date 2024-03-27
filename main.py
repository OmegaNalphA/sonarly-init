import csv
from scipy.io.wavfile import write
import numpy as np

# Specify the file name
file_name = "2022_04_22_hour_heartbeat_merged.csv"
sample_rate = 44100
duration_per_heartbeat = 0.2  # Duration in seconds

def frequency_from_heartbeat(heartbeat):
    # Map the heartbeat value to a frequency range (e.g., 200 to 800 Hz)
    return 200 + (heartbeat - 60) * (600 / (115 - 60))

def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.sin(2 * np.pi * frequency * t)
    return wave

# List to hold all sine waves
all_waves = []

with open(file_name, "r") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        heartbeat = int(row[1])  # Ensure heartbeat is an integer
        frequency = frequency_from_heartbeat(heartbeat)
        wave = generate_sine_wave(frequency, duration_per_heartbeat, sample_rate)
        all_waves.append(wave)

# Concatenate all waves and normalize to int16
full_wave = np.concatenate(all_waves).astype(np.float32)
full_wave *= 32767 / np.max(np.abs(full_wave))  # Normalize to the range of int16
full_wave = full_wave.astype(np.int16)

# Write the resulting waveform to a WAV file
write("heartbeat_sound.wav", sample_rate, full_wave)
