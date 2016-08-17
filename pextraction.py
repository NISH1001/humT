import os
from math import sin,pi
import sys
from visualizer import timeseries,pitchToTimeseries

notePitches =   [61.74,65.41,69.30,73.42,77.78,82.41,87.31,92.50,98.00,103.83,110.00,116.54,123.47,130.81,138.59,146.83,155.56,164.81,174.61,185.00,196.00,207.65,220.00,233.08,246.94,261.63,277.18,293.66,311.13,329.63,349.23 ,369.99,392.00,415.30,440.00,466.16,493.88,523.25,554.37,587.33,622.25, 659.25,698.46,739.99 ,783.99,830.61,880.00 ]
    
def track_pitch(inputFilename): 
    #Load the Aubiopitch from command and save the data onto a file
    os.system("aubiopitch -i" + inputFilename+ " -r 44100 -l 0.8 > temp.txt")
    
    #Use the file to read the frequencies next
    file = open("temp.txt", "r")
    frequen = file.read().split()
    map(float, frequen)
    
    #delete the temp file beacuse it is not needed anymore
    os.system("rm temp.txt")
    #Pitch obtained in the form of [Time,Frequency]. Ignore time for now
    frequency = []
    analog_freq = []
    for i in range(0, len(frequen),2):
        if float(frequen[i+1]) < 60: 
            continue
        
        elif float(frequen[i+1]) >800:
            continue
        else:  
            #mapping the pitches in the frequency to the list given above (autotuning)
            val = float(frequen[i+1])
            temp1 = min(range(len(notePitches)),key = lambda i: abs(notePitches[i]- val))
            frequency.append(notePitches[temp1])
            analog_freq.append(frequen[i+1])
    
    
    #Pitches is the list of pitches after averaging
    pitches = []
    
    #prev_pitch is the centre of the clusture
    prev_pitch = frequency[0]
    cluster = [] 
    for pitch in frequency:
        
        #make a ratio variable
        ratio = max(pitch,prev_pitch)/ min(pitch,prev_pitch)
        
        #anamoly, pitches can not be more than 2.5 times apart
        if ratio > 2.5:
            continue 
        
        if abs(prev_pitch-pitch) < 5:
            cluster.append(pitch)
        else: 
            if len(cluster) < 15:
                cluster = []
                prev_pitch = pitch
                continue
            maxoccuredvalue = max(set(cluster),key=cluster.count)
            pitches += [notePitches.index(maxoccuredvalue),len(cluster)]
            cluster = []

        prev_pitch = pitch
    
    #now we shall see the pitches differences 
    pitchDirection = []
    initialPitch = pitches[0]

    for p in range(2,len(pitches),2):
        pitchDifference = pitches[p] - initialPitch
        pitchDirection.append(pitchDifference)
        
        initialPitch = pitches[p]

    return pitches,pitchDirection


def main():
    track_pitch(str(sys.argv[1]))


if __name__ == "__main__":
    main()
