#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import time
from pextraction import track_pitch 
from visualizer import timeseries

from recorder import Recorder

def euclidean(x,y, numpy_use = True):
    """
    returns euclidean distance matrix
    """
    distances = []
    if numpy_use:
        m, n = np.meshgrid(x, y)
        distances = (m-n) ** 2
    else:
        # find euclidean distance matrix
        lx = len(x) # along x axis
        ly = len(y) # along y axis
        distances = np.zeros((ly, lx))
        for i in range(ly):
            for j in range(lx):
                distances[i,j] = (x[j] - y[i])**2
    return distances

def fdtw(x, y, dist_metric):
    """
    returns the cost along with the warping path
    """
    lx = len(x)
    ly = len(y)

    # hold the accumulated cost
    accumulated_cost = np.zeros((ly, lx))

    # bottom-left point in the grid -> (0,0) graphically :D
    accumulated_cost[0, 0] = dist_metric[0, 0]

    # accumulate first row starting from (0,1) -> along x-axis
    for i in range(1, lx):
        accumulated_cost[0,i] = dist_metric[0,i] + accumulated_cost[0, i-1]    

    # accumulate first column starting from (1,0) -> along y-axis
    for i in range(1, ly):
        accumulated_cost[i,0] = dist_metric[i,0] + accumulated_cost[i-1,0]

    """ for other elements in the grid
        Accumulated_Cost (D(i,j)) = 
        min{ D(i−1,j−1), D(i−1,j), D(i,j−1) } + dist_metric(i,j)
    """
    for i in range(1, ly):
        for j in range(1,lx):
            accumulated_cost[i, j] = min(
                    accumulated_cost[i-1, j-1],
                    accumulated_cost[i-1, j],
                    accumulated_cost[i, j-1],
                    ) + dist_metric[i, j]

    # now backtrack and find optimial warp path -> non-optimized -_-
    path = [ [lx-1, ly-1] ]
    i = ly - 1
    j = lx - 1
    cost = dist_metric[i, j]
    while i>0 and j>0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            if accumulated_cost[i-1, j] == min(
                        accumulated_cost[i-1, j-1], 
                        accumulated_cost[i-1, j], 
                        accumulated_cost[i, j-1]
                    ):
                i -= 1
            elif accumulated_cost[i, j-1] == min(
                        accumulated_cost[i-1, j-1], 
                        accumulated_cost[i-1, j], 
                        accumulated_cost[i, j-1]
                    ):
                j -= 1
            else:
                i -= 1
                j -= 1
        cost += dist_metric[i, j]
        path.append([j, i])
    path.append([0, 0])
    cost += dist_metric[0,0]

    # find cost
    # cost = sum([ dist_metric[x, y] for[y, x] in path ])
    return path, cost

def myclip(x, _min, _max):
    return min(max(x, _min), _max)

def euc(x, y):
    return (x-y) ** 2

# copy pasted from Neeraj and crew
# cuz mine was shit and this has even
# got localization
def dtw(a, b, distmetric, localize=None):
    D = [[10E16]*(len(b)+1)]*(len(a)+1)
    for i in range(len(a)):
        D[i+1][0] = 10E16
    for i in range(len(b)):
        D[0][i+1] = 10E16
    D[0][0]=0
    # Don't let the window size be less than the size difference
    if localize!=None:
        localize = max(abs(localize),abs(len(a)-len(b)))
    for i in range(len(a)):
        if localize==None:
            left,right = 0,len(b)-1
        else:
            left = myclip(i-localize,0,len(b)-1)
            right = myclip(i+localize,0,len(b)-1)
        for j in range(left,right+1):
            cost = distmetric(a[i],b[j])
            D[i+1][j+1] = cost+min((D[i][j+1],D[i+1][j],D[i][j]))
    i,j = len(a),len(b)
    path = [(i-1,j-1)]
    while True:
        prev = [D[i-1][j-1],D[i-1][j],D[i][j-1]]
        m = prev.index(min(prev))
        if m==0:
            path = [(i-2,j-2)]+path
            i,j=i-1,j-1
        elif m==1:
            path = [(i-2,j-1)]+path
            i=i-1
        else:
            path = [(i-1,j-2)]+path
            j=j-1
        if i==1 and j==1:
            break
        elif i==1:
            path = [(0,x) for x in range(j-1)]+path
            break
        elif j==1:
            path = [(x,0) for x in range(i-1)]+path
            break
    return D[len(a)][len(b)],path

# normalize the time series data by mean
def normalize(vec):
    vals = vec[0::2]
    mx, mn = max(vals), min(vals)
    mean, totf = 0, 0
    for i in range(0, len(vec), 2):
        totf += vec[i+1]
        val = vec[i] * vec[i+1]
        mean += val
    mean /= totf
    l = [   (vec[i] - mean)/(mx - mn)  \
            for i in range(0, len(vec), 2) 
        ]
    return l

def main():
    print("testing")

    recorder = Recorder()
    frames = recorder.start(5)
    recorder.write_wav(frames, "input.wav")

    z =track_pitch("original.wav")
    z = normalize(z)

    y = normalize(track_pitch("notNearOriginal.wav"))

    print("hum vs original")
    x = track_pitch("input.wav")
    timeseries(x)
    x = normalize(x)
    dtwdist, dtwpath = dtw(x, z, euc, 14)
    print(dtwdist)

    print("hum vs non-original")
    dtwdist, dtwpath = dtw(x, y, euc, 14)
    print(dtwdist)

if __name__ == "__main__":
    main()
