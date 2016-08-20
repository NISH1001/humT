from scipy import *
import numpy as np
from wfilter import *
import wavio
import wave
import matplotlib.pyplot as plt

if __name__ == '__main__':

    fs = 8000        # sampled at 8 kHz
    framesz = 0.050  # with a frame size of 50 milliseconds
    hop = 0.025      # and hop size of 25 milliseconds.


    spf=wave.open("audio/input.wav")
    sz=44100
    signal = np.fromstring(spf.readframes(sz),dtype=np.int16)
    x=signal
    # Create test signal and STFT.
    X = stft(x, fs, framesz, hop)

    filt=w_filter(signal,fs,framesz,hop)

    plt.figure(0)
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.title("Original")
    plt.plot(x)

    #plot

    plt.figure(1)
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.title("STFT")
    plt.plot(scipy.absolute(X))


    # Compute the ISTFT.
    T=shape(signal)[0]/fs
    xsignal = istft(X, fs, T, hop)

    plt.figure(2)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.title("Inverse stft")
    plt.plot(xsignal)

    plt.figure(3)
    plt.xlabel("time")
    plt.ylabel("amplitude")
    plt.title("filtered signal")
    plt.plot(filt)
    plt.show()

