#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def euc(x, y):
    return (x-y)**2

# normalize the time series data by mean
#  x = (x - mean)/ S.D
def normalize(vec):
    #mean of the data
    mean = sum(vec) / len(vec)

    #standard deviation of the data
    std = np.std(vec)

    #for each values compute the normalized values] 
    l = [  float(vec[i] - mean)/std for i in range(0, len(vec)) ]
    return l

if __name__ == "__main__":
    main()
