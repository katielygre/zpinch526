import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.signal import windows, decimate, savgol_filter
from pathlib import Path
from copy import deepcopy
import pdb

def sci_notation(value, dp=2):
    exponent = int(np.floor(np.log10(abs(value))))
    coeff = value / 10**exponent
    return rf"${coeff:.{dp}f} \times 10^{{{exponent}}}$"

def STFT2(signal, time,
         W = 500, # number of windows
         L = 1 # Length of window in µs
        ):

    N = len(time)
    dt = time[1] - time[0] # step, µs
    fs = 1 / dt # sampling freq in MHz
    S = int(np.floor(L * fs)) # Samples per window

    # Set up time and spectral axes
    tax = np.arange(0,N,N//W) # t start indices for W windows
    cut = round(S/(N//W))+1 
    tax = tax[:-cut] # remove the last windows that over flow the time axis
    T = time[tax]
    F = rfftfreq(S,dt) # MHz

    # Batch Fourier Transform
    window = windows.hann(S, sym=False)
    # window = 1
    block = np.array([window * signal[t:t+S] for t in tax])
    G = rfft(block,axis=1, norm='forward') # complex valued (W-cut x M)
    return G, T, F


def get_STFT(data, L, W):
    data_copy = deepcopy(data)
    for diags in data_copy.values():
        for vals in diags.values():
            time = vals['Time']
            V = vals['Voltage']
            Vhat, T, F = STFT2(V, time, L=L, W=W)
            vals['Vhat'] = Vhat
            vals['T'] = T
            vals['F'] = F
            vals['L'] = L
            vals['W'] = W
    return data_copy

def get_STFT2(data, L, W):
    data_copy = deepcopy(data)
    for d in data_copy.values():
        for diags in d.values():
            for vals in diags.values():
                time = vals['Time']
                V = vals['Voltage']
                Vhat, T, F = STFT2(V, time, L=L, W=W)
                vals['Vhat'] = Vhat
                vals['T'] = T
                vals['F'] = F
                vals['L'] = L
                vals['W'] = W
    return data_copy