#!/usr/bin/env python3

from dbhandler import handler

def main():
    db = handler.DBHandler()
    #db.insert('test', [1.11, 222.4, 3, 44], feature_type="DIFF")
    f = db.query(song_name="test", feature_type="PITCH")
    print(f)

if __name__ == "__main__":
    main()

