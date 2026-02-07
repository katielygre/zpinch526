import numpy as np
import matplotlib.pyplot as plt


def plot_raw(data, ax, discharge_voltage = 12., diag="Rogowski"):
    dv = discharge_voltage
    time = data[dv][diag]['Time'] # µs
    V = data[dv][diag]['Voltage'] # Volts
    ax.plot(time, V, label=rf"{diag} coil for {discharge_voltage:2g} kV discharge")
    ax.set_xlabel(rf"Time ($\mu$s)")
    ax.set_ylabel(rf"Voltage (V)")

def plot_STFT(data, ax, discharge_voltage = 12., diag="Rogowski"):
    dv = discharge_voltage
    Vhat = data[dv][diag]['Vhat']
    T = data[dv][diag]['T']
    F = data[dv][diag]['F']

    Vhat_sq = np.abs(Vhat)**2
    Vhat_sq = Vhat_sq.T
    levels=100
    cf = ax.contourf(T, F, Vhat_sq, levels=levels, cmap='inferno')

    ax.set_xlabel(rf"Time ($\mu$s)")
    ax.set_ylabel(rf"Frequency (MHz)")
