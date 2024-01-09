# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 11:59:17 2024

@author: hcans
"""
import numpy as np
import matplotlib.pyplot as plt

def read_ecg_data(header_file, data_file, leads=['I', 'II', 'III']):
    # Read the header file to determine the format of the ECG data
    with open(header_file, 'r') as file:
        header_data = file.readlines()

    # Extract the number of leads and the number of samples
    num_leads = int(header_data[0].split()[1])
    num_samples = int(header_data[0].split()[3])

    # Read the data file
    raw_data = np.fromfile(data_file, dtype=np.int16)
    raw_data = raw_data.reshape((num_samples, num_leads))

    # Extract the specified leads
    lead_indices = [header_data.index(next(line for line in header_data if lead in line)) - 1 for lead in leads]
    lead_data = raw_data[:, lead_indices]

    return lead_data

def plot_ecg_leads(ecg_data, qrs_index, sample_rate=500, duration_sec=10):
    # Calculate the start and end indices for the 10-second interval around the QRS index
    start_index = max(0, qrs_index - sample_rate * duration_sec // 2)
    end_index = start_index + sample_rate * duration_sec

    # Adjust the indices to fit within the data array
    start_index = max(start_index, 0)
    end_index = min(end_index, ecg_data.shape[0])

    # Create a time axis for the ECG data
    time_axis = np.linspace(-duration_sec/2, duration_sec/2, end_index - start_index)

    # Plot each lead
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    for i in range(3):
        axs[i].plot(time_axis, ecg_data[start_index:end_index, i])
        axs[i].set_title(f'Lead {i+1}')
        axs[i].set_ylabel('Amplitude')
    axs[2].set_xlabel('Time (s)')
    plt.tight_layout()
    plt.show()

    return time_axis, start_index, end_index

def calculate_and_plot_error_signal(ecg_data, qrs_index, sample_rate=500, duration_sec=3):
    # Calculate the start and end indices for the 3-second interval around the QRS index
    start_index = max(0, qrs_index - sample_rate * duration_sec // 2)
    end_index = start_index + sample_rate * duration_sec

    # Adjust the indices to fit within the data array
    start_index = max(start_index, 0)
    end_index = min(end_index, ecg_data.shape[0])

    # Create a time axis for the error signal data
    time_axis = np.linspace(-duration_sec/2, duration_sec/2, end_index - start_index)

    # Calculate the error signal
    error_signal = ecg_data[start_index:end_index, 0] + ecg_data[start_index:end_index, 2] - ecg_data[start_index:end_index, 1]

    # Plot the error signal
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, error_signal, label='Error Signal E[n]')
    plt.title('Error Signal E[n] = V[I] + V[III] - V[II]')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.tight_layout()
    plt.show()


header_file = 'D:/biyomed_final/03000_lr.hea'  
data_file = 'D:/biyomed_final/03000_lr.dat'     

# Read the ECG data
ecg_data = read_ecg_data(header_file, data_file)

# Index of the QRS complex (replace with the actual index of the QRS complex)
qrs_index = 10   # Assuming the QRS complex is at 10 seconds

# Plot the ECG leads for 10 seconds around the QRS complex
_, start_index_10s, end_index_10s = plot_ecg_leads(ecg_data, qrs_index, duration_sec=10)

# Calculate and plot the error signal for 3 seconds around the QRS complex
calculate_and_plot_error_signal(ecg_data, qrs_index, duration_sec=3)