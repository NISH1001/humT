#!/usr/bin/env python3

import json
import sys

from pextraction import track_pitch

def load():
    data = {}
    try:
        datastr = open("storage.json").read()
        data = json.loads(datastr)
    except FileNotFoundError:
        open("storage.json", "w").write('')
        return {}
    return data

def store(wavefile, alias):
    print("extracting pitches...")
    data = load()
    data[alias] = {}
    if data[alias]:
        return

    d = {}
    d['wavefile'] = wavefile
    d['pitches'] = track_pitch(wavefile)
    data[alias] = d
    datastr = json.dumps(data, indent=4)
    open("storage.json", "w").write(datastr)

def main():
    argv = sys.argv[1:]
    store(argv[0], argv[1])

if __name__ == "__main__":
    main()

