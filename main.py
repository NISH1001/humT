#!/usr/bin/env python3

#sources import
from processor import process
from pextraction import track_pitch
from recorder import *
#inbuilt imports
import sys

def main():
    #input_name for argv
    input_name = "" 
    
    #if the input is record
    if sys.argv[1] == 'record':
        # start recording -> 5 sec default
        recorder = Recorder()
        frames = recorder.start(5)
        recorder.write_wav(frames, "input.wav")
        input_name = "input.wav"

    #else if it is a filename
    else:
        input_name = sys.argv[1]

    # load the hum and process
    hum,diff_hum = track_pitch(input_name)
    
    #process the hum and compare with the database
    process(hum,diff_hum)

if __name__ == "__main__":
    main()

