#!/usr/bin/env python3

#inbuilt imports
import json
import sys

#source imports
from pextraction import track_pitch

from dbhandler import handler

class DatabaseQL:

    def __init__(self):
        pass

    def store(self, wavefile, song_name):
        db = handler.DBHandler()
        pitch, difference = track_pitch(wavefile)
        db.insert(song_name, pitch, "PITCH")
        db.insert(song_name, difference, "DIFFERENCE")

    def load(self):
        db = handler.DBHandler()
        return db.query_song_all()

class Database:
    
    def __init__(self,filen = 'storage.json',wavefile = None,alias = None):
        self.__file_name = filen
        self.__wavefile = wavefile
        self.__alias = alias
    

    def load(self):
        data = {}
        try:
            #saving the files in storage.json file
            datastr = open(self.__file_name).read()
            data = json.loads(datastr)
        except FileNotFoundError:
            open(self.__file_name, "w").write('')
            return {}
        return data
    
    def store(self):
        print("extracting pitches...")
        data = self.load()
        data[self.__alias] = {}
        if data[self.__alias]:
            return
         
        d = {}
        d['wavefile'] = self.__wavefile
        pitch = []
        difference = []
        pitch,difference = track_pitch(self.__wavefile)
        d['pitch'] = pitch
        d['difference'] = difference
        data[self.__alias] = d
        datastr = json.dumps(data, indent=4)
        open(self.__file_name, "w").write(datastr)

def main():
    name = ""
    argv = sys.argv[1:]
    d = DatabaseQL()
    if str(argv[0]) == "show":
        data = d.load()
        for n in data:
            name += n +'\n'
        print (name)
    else:
        d.store(argv[0], argv[1])


if __name__ == "__main__":
    main()

