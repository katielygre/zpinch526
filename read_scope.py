import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from pathlib import Path
import re

# data_dict = {
#     discharge_V: {
#         "Rogowski": {"Time": None, "Voltage": None},
#         "M1": {"Time": None, "Voltage": None},
#         "M2": {"Time": None, "Voltage": None},
#         "M4": {"Time": None, "Voltage": None},
#         "M5": {"Time": None, "Voltage": None},
#         "M7": {"Time": None, "Voltage": None}
#     }
# }


def read_oscilloscope_data(
    filename, data_dict=None, discharge_V=9.0, Osc_id=1, diag="rogowski"
):
    """
    Reads the specified channel data from the oscilloscope CSV file.
    channel_index should be 0 for the first channel, 1 for the second, etc.
    """
    # Calculate the column index for the Time and Voltage data
    # Each channel block has 5 columns, with a blank column in between each block

    if data_dict is None:
        data_dict = {}

    try:
        #     data_dict[discharge_V] = {
        #     "Rogowski": {"Time": None, "Voltage": None},
        #     "M1": {"Time": None, "Voltage": None},
        #     "M2": {"Time": None, "Voltage": None},
        #     "M4": {"Time": None, "Voltage": None},
        #     "M5": {"Time": None, "Voltage": None},
        #     "M7": {"Time": None, "Voltage": None}
        # }
        if discharge_V not in data_dict:
            data_dict[discharge_V] = {}
    except Exception as e:
        print(f"Please input a dictionary into the 'data_dict' argument: {e}")

    mapping = {
        1: {
            "rogowski": {"N_channels": 1, "diag_id": ["Rogowski"]},
            "mirnov": {"N_channels": 2, "diag_id": ["M1", "M5"]},
        },
        2: {"mirnov": {"N_channels": 2, "diag_id": ["M4", "M7"]}},
    }
    try:
        N_channels = mapping[Osc_id][diag]["N_channels"]
    except Exception as e:
        print(f"Invalid input for 'diag' or 'Osc_id': {e}")

    for channel_index in range(N_channels):
        scale = 6 * channel_index + 1
        base_column = 6 * channel_index + 3
        scale = pd.read_csv(filename, usecols=[scale], header=None, names=["scale"])
        vert_scale = float(scale["scale"][8])
        hor_scale = float(scale["scale"][11])
        yzero = float(scale["scale"][13])
        data = pd.read_csv(
            filename,
            skiprows=10,
            usecols=[base_column, base_column + 1],
            header=None,
            names=["Time", "Voltage"],
        )
        V_arr = data["Voltage"].to_numpy()
        T_arr = data["Time"].to_numpy()
        V = V_arr / vert_scale  # Volts
        T = T_arr / hor_scale * 1e6  # µs
        diag_id = mapping[Osc_id][diag]["diag_id"][channel_index]
        data_dict[discharge_V][diag_id] = {"Time": T, "Voltage": V}
        # data_dict[discharge_V][diag_id]["Time"] = T
        # data_dict[discharge_V][diag_id]["Voltage"] = V

    return data_dict


def parse_filename(filepath):
    fname = Path(filepath)
    filename = fname.name

    match = re.search(r"(\d+)_(\d+)_kV_O(\d+)_(\w+)", filename)

    if not match:
        raise ValueError("Filename format not recognized")

    discharge_voltage = float(f"{match.group(1)}.{match.group(2)}")
    oscilloscope_index = int(match.group(3))
    probe = match.group(4)

    if probe == "Rog":
        probe = "rogowski"
    elif probe == "Mir":
        probe = "mirnov"

    return discharge_voltage, oscilloscope_index, probe


# files = sys.argv[1:]
# filepaths = [Path(file) for file in files]
# data_dict = {}
# for fpath in filepaths:


# data_dict = read_oscilloscope_data(fpath, data_dict, discharge_V=discharge_voltage, Osc_id=osc_id, diag='Mirnov')
# if osc_id==1:
#     data_dict = read_oscilloscope_data(fpath, data_dict, discharge_V=discharge_voltage, Osc_id=osc_id, diag='Rogowski')


# discharge_voltages = [7.5, 9., 10.5, 12.]

# O1_dict = {
# 7.5: {
#     "M1": {
#         'Time': np.array([]),
#         'Voltage': np.array([])
#     },
#     'M4':{
#         'Time': np.array([]),
#         'Voltage': np.array([])
#     },
#     'M5':{
#         'Time': np.array([]),
#         'Voltage': np.array([])
#     },
#     'M7':{
#         'Time': np.array([]),
#         'Voltage': np.array([])
#     },
#     'Rogowski':{
#         'Time': np.array([]),
#         'Voltage': np.array([])
#     },
# },
# 9.0: {
#     'Discharge Voltage': 9.0, #kV
# }
# }
