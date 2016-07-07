#!/usr/bin/env python3

#sources import
from processor import normalize,euc
from pextraction import track_pitch
from visualizer import timeseries,pitchToTimeseries,similarityPlot
from recorder import Recorder
import database

#inbuilt imports
from fastdtw import fastdtw
import matplotlib.pyplot as plt
import sys

def process(hum):
    #setting input waveform
    hum = pitchToTimeseries(hum)
    
    data = database.load()
    l = {}
    
    for alias in data:
        #setting input waveform
        original = data[alias]['pitches']
        #convert org to time series
        org = pitchToTimeseries(original)
        
        if (len(hum) > len(org)):
            hum, org = org, hum
                
        '''iterations for sampling down the track
        set it by dividing the original by hum i.e divide original
        into hum sizes
        '''
        divideFactor = 1.0 * len(org)/len(hum)
        
        #chunk size to divide the iterations into
        chunkSize = int(len(org)/divideFactor)
        
        #atleast 2 iterations 
        iterations = int(divideFactor+0.5)
        if iterations < 2:
            iterations = 2
        
        #dictionary for path ,distances pair
        pathDistancePairs = {}

        chunkStart = 0
        chunkEnd = chunkStart + chunkSize 
        
            
        while chunkEnd < len(org):
            #sampling the org into chunks from chunkStart to chunkEnd
            org_temp =  normalize(org[chunkStart:chunkEnd])
            #FastDTW used from the module
            distance,path = fastdtw(normalize(hum),org_temp,dist = euc)
            
            chunkStart += 50
            chunkEnd = chunkStart + chunkSize 
            #create a dictionary of type {key = path, value = distance} 
            pathDistancePairs[distance] = path,org_temp

        #the min distances of all the distances is taken as the distance 
        if pathDistancePairs == {}:
            print("NULL pathDistancePair")
        shortestDistance = min(d for d,value in pathDistancePairs.iteritems())

        pathChunkPairs = pathDistancePairs[shortestDistance] 
        #shortest path corresponding to minimum distance
        shortestPath = pathChunkPairs[0]
        
        #best chunk match
        matchedChunk = pathChunkPairs[1]

        l[alias] = shortestDistance,matchedChunk,shortestPath
        print(alias,shortestDistance, " Finished comparing...")
    
    #showing results
    results(l,normalize(hum))   

def results(l,hum):
    #shortest Distance among the many distances
    shortestDistance = min(l[alias][0] for alias in l)
    for alias in l:
        if l[alias][0] == shortestDistance:
            print(alias,shortestDistance)
            break
    #key corresponding to the minimum distance
    #key = [k for k in l if l[k][0] == shortestDistance]
    for k in l:
        if l[k][0] == shortestDistance:
            matchedChunk = l[k][1]
            shortestPath = l[k][2]
    #ploting similarity plot 
    #timeseries(hum,matchedChunk)
    similarityPlot(hum,matchedChunk,shortestPath)


def main():
    #inputName for argv
    inputName = ""
    
    
    #if the input is record
    if sys.argv[1] == 'record':
        # start recording -> 5 sec default
        recorder = Recorder()
        frames = recorder.start(5)
        recorder.write_wav(frames, "input.wav")
        inputName = "input.wav"

    #else if it is a filename
    else:
        inputName = sys.argv[1]

    # load the hum and process
    hum = track_pitch(inputName)
    
    #process the hum and compare with the database
    process(hum)

if __name__ == "__main__":
    main()

