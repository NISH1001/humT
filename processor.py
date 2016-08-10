#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#sources import
import numpy as np
from visualizer import timeseries, pitchToTimeseries, similarityPlot
from recorder import Recorder
from database import Database, DatabaseQL
from dbhandler import handler

#inbuilt imports
from fastdtw import fastdtw
import matplotlib.pyplot as plt

class PathDistancePairs:
    #define path distance pair dictionary
    def __init__ (self):
        self._pdp = {}
        self._shortest_distance = None
        self._shortest_path = None
        self._matched_org = None
        self._matched_hum = None
    
    def assign(self,distance,path,org,hum):
        self._pdp[distance] = path,org,hum
        
    def pathDistanceCalc(self):
        self._shortest_distance = min(d for d,value in self._pdp.items())
         
        path_chunk_pairs= self._pdp[self._shortest_distance]
        #shortest path corresponding to minimum distance
        self._shortest_path = path_chunk_pairs[0]
    
        #best chunk org
        self._matched_org = path_chunk_pairs[1]
        self._matched_hum = path_chunk_pairs[2]
        #return self._shortest_distance,self._shortest_path,self._matched_chunk
    

    #if there is no path distance pair, returns false for is valid
    def isValid(self):
        if self._pdp == {}:
            return False
        else:
            return True

    #shows the shortest distance
    def getDistance(self):
        return self._shortest_distance 

    def getPath(self):
        return self._shortest_path
    
    def getMatch(self):
        return self._matched_org
    
    def getHum(self):
        return self._matched_hum

def compare(hum, org, segmentation = True):
    '''iterations for sampling down the track
    set it by dividing the original by hum i.e divide original
    into hum sizes divided by divide factor
    '''

    if (len(hum) > len(org)):
        hum, org = org, hum
         
    #class for path ,distances pair
    pdp = PathDistancePairs()
    
    if segmentation:
        divide_factor = 1.2* len(org)/len(hum)
        #chunk size to divide the iterations into
        chunk_size = int(len(org)/divide_factor)
        #atleast 2 iterations
        iterations = int(divide_factor+0.5)
        if iterations < 1:
            iterations = 1
    
        chunk_start = 0
        chunk_end = chunk_start + chunk_size
        while chunk_end < len(org):
            #sampling the org into chunks from chunk_start to chunk_end
            org_temp = org[chunk_start:chunk_end]
            #FastDTW used from the module
            distance, path = fastdtw(org_temp, hum, dist=euc)
            chunk_start += 50
            chunk_end += 50
            
            #assign the distances, path and matched chunk
            pdp.assign(distance, path, org_temp,hum)
    else:
        distance,path = fastdtw(org,hum,dist=euc)
        pdp.assign(distance,path,org,hum)

    #the min distances of all the distances is taken as the distance
    if not pdp.isValid:
        print("NULL pathDistancePair")
        print("Error !!! ")
             
    return pdp


prevDistance = 0
def process(hum,diff_hum):
    #setting input waveform
    hum = pitchToTimeseries(hum) 
    global prevDistance

    """
    Data = Database()
    data = Data.load()
    """
    
    l = {}

    hum_org = hum
    diff_hum_org = diff_hum

    dbh = handler.DBHandler()
    data = dbh.query_song_all()
    
    for alias in data:
        #setting input waveform

        #original = data[alias]['pitch']
        #diff_org = data[alias]['difference']


        original = np.array(dbh.query(alias, 'PITCH'))
        diff_org = np.array(dbh.query(alias, 'DIFFERENCE'))

        #convert org to time series
        org = pitchToTimeseries(original)
       
        #reassign the hum and hum diff each time beacuse the fucntions inside change
        #this value
        hum = hum_org
        diff_hum = diff_hum_org

        timeseries(normalize(org),normalize(hum))
 
        #class of pdp contains the path distance and closest matched chunk
        #for pitch values
        pdp = PathDistancePairs()  
        #for pitchdifference values
        pdp_diff = PathDistancePairs()
        
        pdp = compare(normalize(hum),normalize(org),True) 
        pdp_diff = compare(diff_hum,diff_org,False)
        
        pdp.pathDistanceCalc()
        pdp_diff.pathDistanceCalc()
        
        #the dictionary now contains the path distance pair and the pitchdifference path distance pair
        l[alias] = pdp,pdp_diff
        print(alias, pdp.getDistance(), pdp_diff.getDistance(), ' finished comparing ...')
        #print('distance ',alias,pdp.getDistance())
        #print('pitchdifference distance ' , alias, pdp_diff.getDistance())

    #showing results
    return results(l)
    
def results(l):
    #shortest Distance among the many distances
    #0 index in alias is the path difference pair
    #1 index in the alias in the difference of pitch path difference pair
    #we take the product of these two numbers as the distance
    shortest_distance = [(0.01*l[alias][0].getDistance()+ 0.99*l[alias][1].getDistance(), alias) for alias in l]
    shortest_distance.sort()
    alias = shortest_distance[0][1]
    
    print
    print(shortest_distance)
    print(alias)
    print('pitch distance ', l[alias][0].getDistance())
    print(' pitch difference distance ', l[alias][1].getDistance())
    print('Shortest Distance ',shortest_distance[0][0])
    
    #ploting similarity plot 
    #timeseries(hum,matched_chunk)
    similarityPlot(l[alias][0].getHum(),l[alias][0].getMatch(),l[alias][0].getPath(),50)
    similarityPlot(l[alias][1].getHum(),l[alias][1].getMatch(),l[alias][1].getPath(),1) 
    return alias

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
    l = [float(vec[i] - mean)/std for i in range(0, len(vec))]
    return l

if __name__ == "__main__":
    main()
