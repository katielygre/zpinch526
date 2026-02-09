import numpy as np
import matplotlib.pyplot as plt


def plot_raw(data, ax, discharge_V=12.0, diag="Rogowski", trange: tuple = ()):
    dv = discharge_V
    time = data[dv][diag]["Time"]  # µs
    V = data[dv][diag]["Voltage"]  # Volts
    tmin, tmax = trange if trange else (time[0], time[-1])

    ax.plot(time, V, label=rf"{diag} coil for {discharge_V:2g} kV discharge")
    ax.set_xlim(tmin, tmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Voltage (V)", fontsize=12)


def plot_STFT(
    data, ax, discharge_V=12.0, diag="Rogowski", Trange: tuple = (), Frange: tuple = ()
):
    dv = discharge_V
    Vhat = data[dv][diag]["Vhat"]
    T = data[dv][diag]["T"]
    F = data[dv][diag]["F"]
    L = data[dv][diag]["L"]

    Tmin, Tmax = Trange if Trange else (T[0], T[-1])
    Fmin, Fmax = Frange if Frange else (1 / L, F[-1])
    Flims = (F >= Fmin) & (F <= Fmax)

    Vhat_sq = np.abs(Vhat) ** 2
    Vhat_sq = Vhat_sq.T
    levels = 100
    cf = ax.contourf(T, F[Flims], Vhat_sq[Flims, :], levels=levels, cmap="inferno")

    ax.set_xlim(Tmin, Tmax)
    ax.set_ylim(F[0], Fmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Frequency (MHz)", fontsize=12)

    return cf


def plot_raw1(
    data, ax, elec_gap=15.5, discharge_V=12.0, diag="Rogowski", trange: tuple = ()
):
    eg = elec_gap
    dv = discharge_V
    time = data[eg][dv][diag]["Time"]  # µs
    V = data[eg][dv][diag]["Voltage"]  # Volts
    tmin, tmax = trange if trange else (time[0], time[-1])

    ax.plot(time, V, label=rf"{diag}, {dv:.1f}kV, {eg:.1f}cm")
    ax.set_xlim(tmin, tmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Voltage (V)", fontsize=12)


def plot_STFT1(
    data,
    ax,
    elec_gap=15.5,
    discharge_V=12.0,
    diag="Rogowski",
    Trange: tuple = (),
    Frange: tuple = (),
):
    eg = elec_gap
    dv = discharge_V
    Vhat = data[eg][dv][diag]["Vhat"]
    F = data[eg][dv][diag]["F"]
    T = data[eg][dv][diag]["T"]
    L = data[eg][dv][diag]["L"]

    Tmin, Tmax = Trange if Trange else (T[0], T[-1])
    Fmin, Fmax = Frange if Frange else (1 / L, F[-1])
    Flims = (F >= Fmin) & (F <= Fmax)

    Vhat_sq = np.abs(Vhat) ** 2
    Vhat_sq = Vhat_sq.T
    levels = 100
    cf = ax.contourf(T, F[Flims], Vhat_sq[Flims, :], levels=levels, cmap="inferno")

    ax.set_xlim(Tmin, Tmax)
    ax.set_ylim(F[0], Fmax)
    ax.set_xlabel(rf"Time ($\mu$s)", fontsize=12)
    ax.set_ylabel(rf"Frequency (MHz)", fontsize=12)

    return cf


def plot_voltage(
    data, ax, elec_gap=15.5, discharge_V=12.0, diag="Rogowski", trange: tuple = ()
):
    eg = elec_gap
    dv = discharge_V

    time = data[eg][dv][diag]["Time"]  # seconds (I assume)
    voltage = data[eg][dv][diag]["Voltage"]

    # convert to microseconds for display (like your other plots)
    time_us = time * 1e6

    tmin, tmax = trange if trange else (time_us[0], time_us[-1])

    ax.plot(time_us, voltage, label=rf"{diag}, {dv:.1f}kV, {eg:.1f}cm")
    ax.set_xlim(tmin, tmax)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Voltage (V)")


def plot_current(
    data, ax, elec_gap=15.5, discharge_V=12.0, diag="Rogowski", trange: tuple = ()
):
    """
    Integrate Rogowski voltage to get plasma current.
    Output in kA.
    """
    eg = elec_gap
    dv = discharge_V

    time = data[eg][dv][diag]["Time"]  # seconds
    voltage = data[eg][dv][diag]["Voltage"]

    # ---- Rogowski constants ----
    mu0 = 4 * np.pi * 1e-7
    N = 60
    rogowski_major_radius = 0.09  # m
    rogowski_minor_radius = 0.002  # m

    n = N / (2 * np.pi * rogowski_major_radius)
    A = np.pi * rogowski_minor_radius**2
    c = 10 / 1  # voltage divider

    # ---- integration ----
    dt = time[1] - time[0]  # assumes uniform spacing
    current_unscaled = np.cumsum(voltage) * dt
    current = current_unscaled / (mu0 * n * A * c) / 1000  # kA

    # convert time to µs for plotting
    time_us = time * 1e6

    tmin, tmax = trange if trange else (time_us[0], time_us[-1])

    ax.plot(time_us, current, label=rf"{dv:.1f}kV, {eg:.1f}cm")
    ax.set_xlim(tmin, tmax)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Current (kA)")
