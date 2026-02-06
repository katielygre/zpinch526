import pandas as pd
import re
from pathlib import Path
import os
import pdb
import sys
from read_scope import read_oscilloscope_data, parse_filename
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


data_dict = {}

filepaths = [
    "12_5_cm/10_5_kV_O2_Mir.csv",
    "12_5_cm/10_5_kV_O1_Mir.csv",
    "12_5_cm/10_5_kV_O1_Rog.csv",
]
for filepath in filepaths:
    dv, oi, diag = parse_filename(filepath)
    file_dict = read_oscilloscope_data(filepath, data_dict, dv, oi, diag)

print(data_dict[10.5].keys())
