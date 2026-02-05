import pandas as pd
import re
import os

def parse_filename(filepath):

    filename = os.path.basename(filepath)

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



parse_filename(r"\12_5_cm\7_5_kV_O1_Mir.csv")