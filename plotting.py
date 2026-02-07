import numpy as np
import matplotlib.pyplot as plt


def plot_raw(data, ax, discharge_V = 12., diag="Rogowski", trange:tuple=()):
    dv = discharge_V
    time = data[dv][diag]['Time'] # µs
    V = data[dv][diag]['Voltage'] # Volts
    tmin, tmax = trange if trange else (time[0], time[-1])

    ax.plot(time, V, label=rf"{diag} coil for {discharge_V:2g} kV discharge")
    ax.set_xlim(tmin, tmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Voltage (V)", fontsize=12)

def plot_STFT(data, ax, discharge_V = 12., diag="Rogowski", Trange:tuple=(), Frange:tuple=()):
    dv = discharge_V
    Vhat = data[dv][diag]['Vhat']
    T = data[dv][diag]['T']
    F = data[dv][diag]['F']
    L = data[dv][diag]['L']

    Tmin, Tmax = Trange if Trange else (T[0], T[-1])
    Fmin, Fmax = Frange if Frange else (1/L, F[-1])
    Flims = (F>=Fmin) & (F<=Fmax)

    Vhat_sq = np.abs(Vhat)**2
    Vhat_sq = Vhat_sq.T
    levels=100
    cf = ax.contourf(T, F[Flims], Vhat_sq[Flims,:], levels=levels, cmap='inferno')
    
    ax.set_xlim(Tmin, Tmax)
    ax.set_ylim(F[0], Fmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Frequency (MHz)", fontsize=12)

    return cf
