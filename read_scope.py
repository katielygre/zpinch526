import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def read_oscilloscope_data(filename, discharge_V=9., Osc_id=1, diag='Rogowski'):
    """
    Reads the specified channel data from the oscilloscope CSV file.
    channel_index should be 0 for the first channel, 1 for the second, etc.
    """
    # Calculate the column index for the Time and Voltage data
    # Each channel block has 5 columns, with a blank column in between each block

    data_dict = {
        discharge_V: {
            "Rogowski": {"Time": None, "Voltage": None},
            "M1": {"Time": None, "Voltage": None},
            "M2": {"Time": None, "Voltage": None},
            "M4": {"Time": None, "Voltage": None},
            "M5": {"Time": None, "Voltage": None},
            "M7": {"Time": None, "Voltage": None}
        }
    }

    mapping = {1: {
                'Rogowski': {"N_channels": 1, "diag_id": ["Rogowski"]}, 
                'Mirnov': {"N_channels": 2, "diag_id": ["M1", "M5"]}
                }, 
               2: {
                'Mirnov': {"N_channels": 2, "diag_id": ["M4", "M7"]}
                }
                }
    try:
        N_channels = mapping[Osc_id][diag]["N_channels"]
    except Exception as e:
        print(f"Invalid input for 'diag' or 'Osc_id': {e}")

    for channel_index in range(N_channels):
        scale = 6 * channel_index + 1
        base_column = 6 * channel_index + 3
        scale = pd.read_csv(filename, usecols=[scale], header=None, names=['scale'])
        vert_scale = float(scale['scale'][8])
        hor_scale = float(scale['scale'][11])
        yzero = float(scale['scale'][13])
        data = pd.read_csv(filename, skiprows=10, usecols=[base_column, base_column + 1], header=None, names=['Time', 'Voltage'])
        V = (data['Voltage'] - yzero) / vert_scale # Volts
        T = data['Time'] / hor_scale * 1e6 # µs
        diag_id = mapping[Osc_id][diag]["diag_id"][channel_index]

        data_dict[discharge_V][diag_id]["Time"] = T
        data_dict[discharge_V][diag_id]["Voltage"] = V

    return data_dict

discharge_voltages = [7.5, 9., 10.5, 12.]

for discharge_voltage in discharge_voltages:
    data_dict = read_oscilloscope_data()


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


