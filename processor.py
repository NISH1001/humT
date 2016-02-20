#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plot
import time


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


def main():
    #x = np.array([1, 0, 2, 3, 4, 5])
    #y = np.array([0, 1, 0, 0, 4, 5, 0, 0])
    #y1 = np.array([2, 3, 4, 0, 6])

    # random samples
    count = 1000
    x = np.random.randint(0, count, count)
    y = np.random.randint(0, count, count+500)
    y1 = np.random.randint(0, count, count+1000)
    
    # some benchmarkings and samples

    # compare x and y using numpy distance matrix
    start = time.time()
    distances = euclidean(x, y, numpy_use=True)
    path, cost = fdtw(x, y, distances)
    print(time.time() - start)
    print(cost)

    # compare x and y using own distance matrix
    start = time.time()
    path, cost = fdtw(x, y, euclidean(x, y, numpy_use=False))
    print(time.time() - start)
    print(cost)

    # compare x and y1 using numpy distance matrix
    start = time.time()
    distances = euclidean(x, y1, numpy_use=True)
    path, cost = fdtw(x, y1, distances)
    print(time.time() - start)
    print(cost)

    # compare x and y1 using own distance matrix
    start = time.time()
    path, cost = fdtw(x, y1, euclidean(x, y1, numpy_use=False))
    print(time.time()-start)
    print(cost)

if __name__ == "__main__":
    main()
