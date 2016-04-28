#!/usr/bin/env python3

from processor import normalize, dtw, euc
from pextraction import track_pitch
from visualizer import timeseries
from recorder import Recorder
import database

def process(hum):
    hum_normalized = normalize(hum)
    data = database.load()
    l = {}
    for alias in data:
        original = data[alias]['pitches']
        normalized = normalize(original)
        dtwdist, dtwpath = dtw(hum_normalized, normalized, euc, 14)
        l[alias] = (dtwdist, dtwpath)

    for alias in l:
        print(alias, l[alias][0])

def main():
    # start recording -> 5 sec default
    recorder = Recorder()
    frames = recorder.start(5)
    recorder.write_wav(frames, "input.wav")

    # load the hum and process
    hum = track_pitch("input.wav")
    timeseries(hum)
    process(hum)

    """
    print("hum vs original")
    x = normalize(x)
    dtwdist, dtwpath = dtw(x, z, euc, 14)
    print(dtwdist)

    y = normalize(track_pitch("notNearOriginal.wav"))
    print("hum vs non-original")
    dtwdist, dtwpath = dtw(x, y, euc, 14)
    print(dtwdist)
    """

if __name__ == "__main__":
    main()

