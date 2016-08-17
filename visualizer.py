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
       pitchdata += [l[p]] * (int(l[p+1]/2))
    return pitchdata


#use like timeseries(a,"a legend" ,b,"b legend",.....)
def timeseries(*arg):
    legend_list = []
    for i in range(1,len(arg),2):
        plt.plot(arg[i-1])
        legend_list.append(arg[i])
    
    plt.legend(legend_list)
    plt.show()

#shows the similarity plot between hum and original
def similarityPlot(hum,org,path,jump):
    #plotting the similarity
    plt.plot(hum)
    plt.plot(org)
    
    i = 1   
    for [map_x,map_y] in path:
        #for every jump value of paths show only 1
        if map_x > len(org) or map_y > len(hum):
            break
        if i % jump == 0:
            plt.plot([map_x,map_y],[org[map_x],hum[map_y]],'r')
            i = 1
        else:
            i = i+1
    
    plt.legend(['Hummed tune','Original tune','Similarity'])
    plt.show()


def main():
    pass

if __name__ == "__main__":
    main()

