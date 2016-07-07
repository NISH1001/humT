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
    hum = normalize(hum)
    
    data = database.load()
    l = {}
    
    for alias in data:
        #setting input waveform
        original = data[alias]['pitches']
        #convert org to time series
        org = pitchToTimeseries(original)
        #noramlize the time series value
        org = normalize(org)
        #plotting the hum and original track
        timeseries(org,hum)
        
        
        '''iterations for sampling down the track
        set it by dividing the original by hum i.e divide original
        into hum sizes
        '''
        divideFactor = 0.95 * len(org)/len(hum)
        
        #chunk size to divide the iterations into
        chunkSize = int(len(org)/divideFactor)
        
        #atleast 2 iterations 
        iterations = int(divideFactor+0.5)
        if iterations < 2:
            iterations = 2
        
        
        #list of distances
        distances = []
        for i in range(0,iterations):
            chunkStart = int(len(org)/divideFactor*(i))
            chunkEnd = chunkStart + chunkSize 
            #sampling the org into chunks from chunkStart to chunkEnd
            org_temp = org[chunkStart:chunkEnd]
            #FastDTW used from the module
            distance,path = fastdtw(hum,org_temp,dist = euc)
            
            #plot similarities between the org_temp and hummed tune
            similarityPlot(hum,org_temp,path)
            #create a list of distances to compare later
            distances += [distance]
        #the min distances of all the distances is taken as the distance 
        l[alias] = min(distances)
        
    for alias in l:
        print(alias, l[alias])

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

