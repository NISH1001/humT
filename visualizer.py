#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import collections as matcollect
import numpy as np
import itertools

def timeseries(l):
    pitches = l
    pitchdata = []
    for p in range(0,len(pitches),2):
       pitchdata += [pitches[p]] * pitches[p+1]
    plt.plot(pitchdata)
    plt.show()

def main():
    pass

if __name__ == "__main__":
    main()

