#!/usr/bin/python

import scipy
from scipy.signal import hann, wiener
from scipy.fftpack import rfft,irfft




"""
calculates short time fourer transform (stft)
also has a lowpass filter of 20Hz (as it is for audio signal)
input:
    x: original signal as numpy array
    fs: sampling frequency
    framesz: fream size / double of window size
    hop: hop size
output:
    stft of x with index
"""


def stft(x, fs, framesz, hop):
    framesamp = int(framesz*fs)
    hopsamp = int(hop*fs)
    w = scipy.hanning(framesamp)
    X = scipy.array([scipy.fft(w*x[i:i+framesamp])
                     for i in range(0, len(x)-framesamp, hopsamp)])
    # lowpass flter 25Hz
    X[scipy.absolute(X)<20]=0

    return X



"""
calculates inverse short time fourer transform (istft)
input:
    x: STFT as numpy array
    fs: sampling frequency
    T: lenght of output signal
        depend on original signal
        T>= T of original signal
        obtained by len(original signal) / fs
    hop: hop size
output:
    original signal of length given by T

"""

def istft(X, fs, T, hop):
    x = scipy.zeros(T*fs)
    framesamp = X.shape[1]
    hopsamp = int(hop*fs)
    for n,i in enumerate(range(0, len(x)-framesamp, hopsamp)):
        x[i:i+framesamp] += scipy.real(scipy.ifft(X[n]))
    return x




"""
calculates average noise-power of a signal
takes quite(only noise) part of signal containing only noise (ie. no useful signal)
specificly for our case we take first 10 frames as quite part
input:
    x: input signal with quite part(only noise)
output:
    average noise-power of the signal

"""
def avg_npower(x,fs, framesz,hop):
    val_sft=stft(x,fs,framesz,hop)
    print len(val_sft[0])
    nsum=sum([abs(val_sft[i])**2 for i in range(0,10)])
    d=sum(nsum)/10
    return int(d)



"""
it is main filter part
with avg noise-power use winer filter
output: filtered signal
"""
def w_filter(signal,fs,framesz,hop,mysize=400):
    noise=avg_npower(signal,fs,framesz,hop)
    return wiener(signal,mysize,noise)
