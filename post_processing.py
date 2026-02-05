import pandas as pd
import re
from pathlib import Path
import os
import pdb
import sys
from read_scope import read_oscilloscope_data
import matplotlib.pyplot as plt

def parse_filename(filepath):
    fname = Path(filepath)
    filename = fname.name

    match = re.search(r'(\d+)_(\d+)_kV_O(\d+)_(\w+)', filename)

    if not match:
        raise ValueError("Filename format not recognized")

    discharge_voltage = float(f"{match.group(1)}.{match.group(2)}")
    oscilliscope_index = int(match.group(3))
    probe = match.group(4)

    if probe == "Rog":
        probe = "rogowski"
    elif probe == "Mir":
        probe = "mirnov"

    return discharge_voltage, oscilliscope_index, probe

filepath = sys.argv[1]

dv, oi, probe = parse_filename(filepath)

data_dict = read_oscilloscope_data(filepath, discharge_V=dv, Osc_id=oi, diag=probe)

fig, ax = plt.subplots(figsize=(10,7), constrained_layout=True)
for diag in data_dict[10.5]:

    V = data_dict[10.5][diag]["Voltage"]
    T = data_dict[10.5][diag]["Time"]
    ax.plot(T, V, label=rf"{diag}")

ax.set_xlabel(rf"Time ($\mu$s)")
ax.set_ylabel(rf"Voltage (V)")
ax.grid()
ax.legend()
plt.show()
