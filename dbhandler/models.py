from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()

class Song(DeclarativeBase):
    """
        a song contains many features
    """

    __tablename__ = "songs"

    name    = Column(String, primary_key=True)
    #features = relationship("Feature", back_populates="song")
    features = relationship("Feature", backref="songs")

class Feature(DeclarativeBase):
    """
        type is either PITCH or DIFF
    """

    __tablename__ = "features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    values  =    Column(String)
    song_name =   Column(String, ForeignKey('songs.name'))
    type    =   Column(String)



