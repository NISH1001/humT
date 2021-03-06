#!/usr/bin/python
from scipy.signal import firwin,medfilt
from scipy.fftpack import rfft, irfft

import matplotlib.pyplot as plt
import numpy as np
import sys,wave,re

SAMP_F=44100

# read audio samples
class AudioError(Exception):
    def __init__(self,args):
        self.args=args
    def Display(self):
        print("Audio Synthetis error:"+''.join(self.args))


#class WaveIO(object):
#    def __init__(self):
#        self.self=signal

def readwav(filename):

    """
    Read a WAV files
    Can't read compressed WAV files (library limitation).

    """

    try:
        spf=wave.open(filename)
        signal = np.fromstring(spf.readframes(SAMP_F),dtype=np.int16)
        return signal
    except Exception as e :
        raise AudioError("Cant read audio")
        return None

def writewav24(filename, rate, data):
    """
    it is not working.
    it is a shit piece of code.

    """
    a32 = np.asarray(data, dtype=np.int32)
    if a32.ndim == 1:
        # Convert to a 2D array with a single column.
        a32.shape = a32.shape + (1,)
    # By shifting first 0 bits, then 8, then 16, the resulting output
    # is 24 bit little-endian.
    a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
    wavdata = a8.astype(np.uint8).tostring()

    w = wave.open(filename, 'wb')
    w.setnchannels(a32.shape[1])
    w.setsampwidth(3)
    w.setframerate(rate)
    w.writeframes(wavdata)
    w.close()

#normalize
def normalize(a):
    a=a/abs(a).max()
    return a

def denormalize(a):
    return a*100000


def band_pass(signal):
    """
    remove lower and higher freqiescies
    pass between 25 Hz to 10 kHz

    """
    lowpass=50
    highpass=8000
    a=np.fft.rfft(signal)
    a[:lowpass]=0
    a[highpass:]=0
    return np.fft.irfft(a)

def afilter(signal):
    """
    filter uses bandpass and medfilter(median filter) from module signal
    output numpy array same size as input
    """
    #signal=wiener(signal,mysize=50,noise=0.25)
    #input: signal array, window size, noise to reduce in dB

    f1=30
    f2=10000

    signal=firwin(signal,[f1,f2],nyq=SAMP_F,pass_zero=False)

    signal=medfilt(signal,kernel_size=9)
    #kernel_size : median filter window, always odd
    return signal

def main():
    signal=readwav("../audio/input.wav")

    plt.figure(1)
    a=plt.subplot(2,1,1)
    r=2**16/2
    a.set_ylim([-r,r])
    a.set_xlabel('time[s]')
    a.set_ylabel('sample value[-]')
    plt.title("unfiltered")
    plt.plot(signal)

    #signal=band_pass(signal)
    signal=afilter(signal)

    left,right=signal[0::2],signal[1::2]
    lf,rf=np.fft.rfft(left),np.fft.rfft(right)

    plt.figure(2)
    a=plt.subplot(2,1,1)
    r=2**16/2
    a.set_ylim([-r,r])
    a.set_xlabel('time[s]')
    a.set_ylabel('sample value[-]')
    plt.title("Filtered")
    plt.plot(right)

    b=plt.subplot(2,1,2)
    b.set_xscale('log')
    b.set_xlabel('frequency[Hz]')
    b.set_ylabel('|amplitude|')
    plt.plot(abs(lf))

    plt.show()


if __name__=='__main__':
    main()
