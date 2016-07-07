#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import collections as matcollect
import numpy as np
import itertools

#convert the pitch data to timeseries data
def pitchToTimeseries(l):
    pitchdata = []
    
    #convert (p1,t1,p2,t2....) into (p1,p1,....t1 p1s, p2 ,p2,p2..... t2 p2s...)
    for p in range(0,len(l)-1,2):
       pitchdata += [l[p]] * int(l[p+1])
    return pitchdata


#use like timeseries(a,b,c,d,.....)
def timeseries(*arg):
    for data in arg:
        plt.plot(data)
    plt.show()

#shows the similarity plot between hum and original
def similarityPlot(hum,org,path):
    #plotting the similarity
    plt.plot(hum,'b',label='Hummed Tune')
    plt.plot(org,'g',label='Original Tune')
    i = 1   
    for [map_x,map_y] in path:
        #for every 50 paths show only 1
        if i % 50 == 0:
            plt.plot([map_x,map_y],[hum[map_x],org[map_y]],'r')
            i = 1
        else:
            i = i+1
    plt.show()


def main():
    pass

if __name__ == "__main__":
    main()

