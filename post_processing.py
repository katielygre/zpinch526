import pandas as pd
import re
from pathlib import Path
import pdb
import sys
from read_scope import read_oscilloscope_data, parse_filename
from analysis import get_STFT
from plotting import plot_raw, plot_STFT
import matplotlib.pyplot as plt
from collections import defaultdict


# filepath = sys.argv[1]

# dv, oi, probe = parse_filename(filepath)

# data_dict = read_oscilloscope_data(filepath, discharge_V=dv, Osc_id=oi, diag=probe)

# fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)
# for diag in data_dict[10.5]:

#     V = data_dict[10.5][diag]["Voltage"]
#     T = data_dict[10.5][diag]["Time"]
#     ax.plot(T, V, label=rf"{diag}")

# ax.set_xlabel(rf"Time ($\mu$s)")
# ax.set_ylabel(rf"Voltage (V)")
# ax.grid()
# ax.legend()
# plt.savefig("10.5volatge.jpg")
# plt.show()

folders = ["0_5_cm", "3_5_cm", "6_5_cm", "9_5_cm", "12_5_cm", "15_5_cm"]

all_data = {}

valid_diags = ["mirnov", "rogowski"]

for folder in folders:
    folder_path = Path(folder)
    filepaths = sorted(folder_path.glob("*.csv"))

    data_dict = {}

    for filepath in filepaths:
        try:
            dv, oi, diag = parse_filename(filepath)
        except ValueError:
            print(f"Skipping {filepath.name} (bad filename)")
            continue

        if diag not in valid_diags:
            print(f"Skipping {filepath.name}")
            continue

        read_oscilloscope_data(filepath, data_dict, dv, oi, diag)

    all_data[folder] = data_dict

print(all_data.keys())

# Output: dict_keys(['0_5_cm', '3_5_cm', '6_5_cm', '9_5_cm', '12_5_cm', '15_5_cm'])

data_dict = {}

# # filepaths = [
# #     "12_5_cm/10_5_kV_O2_Mir.csv",
# #     "12_5_cm/10_5_kV_O1_Mir.csv",
# #     "12_5_cm/10_5_kV_O1_Rog.csv",
# # ]

# filepaths = sys.argv[1:]
# fpaths = [Path(filepath) for filepath in filepaths if filepath.endswith('csv')]

# for fpath in fpaths:
#     dv, oi, diag = parse_filename(fpath)
#     file_dict = read_oscilloscope_data(fpath, data_dict, discharge_V=dv, osc_id=oi, diag=diag)


# L = 0.1
# W = 1000
# new_dict = get_STFT(file_dict, L=L, W=W)

# fig, axs = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
# ax = axs.flatten()
# plot_raw(file_dict, ax[0], discharge_V=10.5, diag="M1")
# plot_raw(file_dict, ax[0], discharge_V=10.5, diag="M5")
# plot_raw(file_dict, ax[1], discharge_V=10.5, diag="M4")
# plot_raw(file_dict, ax[1], discharge_V=10.5, diag="M7")
# ax[0].grid()
# ax[0].legend()
# ax[1].grid()
# ax[1].legend()
# fig.suptitle(rf"Mirnov Coil Raw Data", fontsize=15)

# diag_of_interest = "M1"
# Frange = (50, 500)

# fig1, ax1 = plt.subplots(figsize=(10, 7), constrained_layout=True)
# cf = plot_STFT(new_dict, ax1, discharge_V=10.5, diag=diag_of_interest, Frange=Frange)
# cb = plt.colorbar(cf, ax=ax1, location="right", shrink=0.8)
# cb.set_label(rf"Spectral Power ($V^2$)")
# ax1.grid()
# fig1.suptitle(rf"STFT on Mirnov Coil {diag_of_interest} Data", fontsize=15)


# plt.show()
