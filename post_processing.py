import pandas as pd
import re
from pathlib import Path
import pdb
import sys
from read_scope import read_oscilloscope_data, parse_filename, parse_filepath, get_oscilloscope_data
from analysis import get_STFT, get_STFT2
from plotting import plot_raw, plot_STFT, plot_raw1, plot_STFT1
import matplotlib.pyplot as plt
from collections import defaultdict

# folders = ["0_5_cm", "3_5_cm", "6_5_cm", "9_5_cm", "12_5_cm", "15_5_cm"]

# all_data = {}

# valid_diags = ["mirnov", "rogowski"]

# for folder in folders:
#     folder_path = Path(folder)
#     filepaths = sorted(folder_path.glob("*.csv"))

#     data_dict = {}

#     for filepath in filepaths:
#         try:
#             dv, oi, diag = parse_filename(filepath)
#         except ValueError:
#             print(f"Skipping {filepath.name} (bad filename)")
#             continue

#         if diag not in valid_diags:
#             print(f"Skipping {filepath.name}")
#             continue

#         read_oscilloscope_data(filepath, data_dict, dv, oi, diag)

#     all_data[folder] = data_dict

# print(all_data.keys())

# # Output: dict_keys(['0_5_cm', '3_5_cm', '6_5_cm', '9_5_cm', '12_5_cm', '15_5_cm'])

data_dict = {}

filepaths = sys.argv[1:]
fpaths = [Path(filepath) for filepath in filepaths if filepath.endswith('csv')]

for fpath in fpaths:
    dv, oi, diag, eg = parse_filepath(fpath)
    file_dict = get_oscilloscope_data(fpath, data_dict, discharge_V=dv, osc_id=oi, diag=diag, elec_gap=eg)


L = 0.1
W = 1000
new_dict = get_STFT2(file_dict, L=L, W=W)

electrode_gap = 12.5 # cm
discharge_voltage = 10.5 # kV

fig, axs = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
ax = axs.flatten()
plot_raw1(file_dict, ax[0], elec_gap=electrode_gap, discharge_V=discharge_voltage, diag="M1")
plot_raw1(file_dict, ax[0], elec_gap=electrode_gap, discharge_V=discharge_voltage, diag="M5")
plot_raw1(file_dict, ax[1], elec_gap=electrode_gap, discharge_V=discharge_voltage, diag="M4")
plot_raw1(file_dict, ax[1], elec_gap=electrode_gap, discharge_V=discharge_voltage, diag="M7")
ax[0].grid()
ax[0].legend()
ax[1].grid()
ax[1].legend()
fig.suptitle(rf"Mirnov Coil Raw Data", fontsize=15)

diag_of_interest = "M1"
Frange = (50, 500)

fig1, ax1 = plt.subplots(figsize=(10, 7), constrained_layout=True)
cf = plot_STFT1(new_dict, ax1, elec_gap=electrode_gap, discharge_V=discharge_voltage, diag=diag_of_interest, Frange=Frange)
cb = plt.colorbar(cf, ax=ax1, location="right", shrink=0.8)
cb.set_label(rf"Spectral Power ($V^2$)")
ax1.grid()
fig1.suptitle(rf"STFT on Mirnov Coil {diag_of_interest} Data", fontsize=15)


plt.show()
