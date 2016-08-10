#!/usr/bin/env python3

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import numpy as np

#import settings
from . import settings
from .models import DeclarativeBase, Song, Feature

class DBHandler:
    def __init__(self):
        self.engine= self._connect()
        self.createdb()

    def _connect(self):
        """
            main connection
        """
        return create_engine(URL(**settings.DATABASE), echo=False)

    def createdb(self):
        DeclarativeBase.metadata.create_all(self.engine)

    def insert(self, song_name, feature, feature_type="PITCH"):
        """
            insert feature to a song
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        feature = ','.join([ str(x) for x in feature])

        f = Feature(values = feature, type=feature_type)
        s = Song(name=song_name)
        sn = session.query(Song).get(song_name)

        # check if song is already in db
        if sn:
            s = sn
        # now check if feature is already in the db
        for feat in s.features:
            if feat.type == feature_type:
                session.query(Feature).filter(Feature.type == feature_type).delete(synchronize_session=False)
        s.features.append(f)
        session.add(f)
        session.add(s)
        session.commit()
        session.close()

    def query(self, song_name, feature_type):
        """
            get feature for a song
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()
        song = session.query(Song).get(song_name)
        ret = None
        #self.display(song)
        for f in song.features:
            if f.type == feature_type:
                ret = f.values
        ret = ret.split(',')
        ret = [ int(x) for x in ret]
        return ret

    def query_song_all(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        songs = session.query(Song).all()
        for song in songs:
            yield song.name

    def display(self, song):
        print(song.name)
        for f in song.features:
            print(f.type)
            print(f.values)


def main():
    db = DBHandler()
    #db.insert('test', [1.11, 222.4, 3, 44], feature_type="DIFF")
    f = db.query('test', 'PITCH')
    print(f)

if __name__ == "__main__":
    main()

