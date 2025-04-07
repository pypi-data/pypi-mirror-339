import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

class CaF_Analysis:
    def __init__(self,
                 run_folder,
                 buffer=1000,
                 decimation=32,
                 sampling_rate=125e6,
                 window_length=500,
                 polyorder=5,
                 peak_height=0.001,
                 peak_distance=80,
                 peak_prominence=0.015,
                 show_plot=True,
                 return_peaks=True):
        
        self.run_folder = run_folder
        self.buffer = buffer
        self.decimation = decimation
        self.sampling_rate = sampling_rate
        self.window_length = window_length
        self.polyorder = polyorder
        self.peak_height = peak_height
        self.peak_distance = peak_distance
        self.peak_prominence = peak_prominence
        self.show_plot = show_plot
        self.return_peaks = return_peaks

    def run(self):
        # Find first matching .npy file
        npy_files = [f for f in os.listdir(self.run_folder) if f.endswith(".npy") and "_run_PMT_" in f]
        if not npy_files:
            raise FileNotFoundError(f"No matching .npy files found in {self.run_folder}")

        data_path = os.path.join(self.run_folder, npy_files[0])
        data = np.load(data_path)

        # Time calibration
        buff_length = range(16384)
        rate = self.sampling_rate / self.decimation
        time = np.array([x / rate * 1e3 for x in buff_length])  # ms
        average_data = data[self.buffer:]
        time = time[self.buffer:]

        # Smoothing
        smoothed_data = savgol_filter(average_data, window_length=self.window_length, polyorder=self.polyorder)

        # Peak finding
        peaks, properties = find_peaks(
            smoothed_data,
            height=self.peak_height,
            distance=self.peak_distance,
            prominence=self.peak_prominence
        )

        tof_times = time[peaks]

        # Plotting
        if self.show_plot:
            plt.figure(figsize=(12, 6))
            plt.plot(time, smoothed_data, label="Smoothed Data", color='black')
            plt.plot(time[peaks], smoothed_data[peaks], "ro", label="Peaks")
            plt.scatter(time, average_data, marker='o', label="Raw Data", s=10, alpha=0.3)
            plt.xlabel("Time (ms)")
            plt.ylabel("Signal (a.u.)")
            plt.title("TOF Signal with Peaks")
            plt.legend()
            plt.tight_layout()
            plt.show()

        # Output
        if self.return_peaks:
            return np.round(tof_times, 3)
        else:
            print("TOF peak times (ms):", np.round(tof_times, 3))