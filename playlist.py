#!/usr/bin/python3

from pathlib import Path
import os
import sys
import random
import subprocess
from config import *

############################################################################
#
# TODO:
# - Checker plus de types de fichiers ?
# - Meilleure gestion de gnome-mpv (api mpv à la place ?)
# - Mise en cache
#
############################################################################

class Playlist:
    def __init__(self,db,log,check=True):
        self.check=check
        self.PATH_TO_DB = Path(db)
        if not self.PATH_TO_DB.exists():
            raise ValueError("the db does not exist, unable to create playlist!")
        self.PATH_TO_LOG = Path(log)
        self.CURRENT_ARTIST = ""
        self.CURRENT_ALBUM = ""
        self.PATH_TO_PLAYLIST = ""
        self.playlist = []
        #just open the file in append mode to create it
        #if it's needed
        with open(os.fspath(self.PATH_TO_LOG),'a') as log:
            pass

    def uncheck(self):
        """
        Used with -n, allow to play an album
        without get rid of it.
        """
        self.check=False

    def append_log(self):
        """
        Add the album played to the log,
        ensure that it will not be played anymore
        """
        with open(os.fspath(self.PATH_TO_LOG),'a') as log:
            log.write(''.join((os.fspath(self.PATH_TO_PLAYLIST),'\n')))

    def create_playlist(self):
        """
        Shuffle the next album to play in the DB:
        Create the playlist, use the DB to fill the the playlist.
        And, use the checklist and compare the two (if check is true).
        """
        checkList = []
        artists = os.listdir(os.fspath(self.PATH_TO_DB))

        #CHECK FOR LOG ERROR
        if self.check:
            with open(os.fspath(self.PATH_TO_LOG),'r') as log:
                for i in log.readlines():
                    checkList.append(i[0:-1])
            if len(artists) < len(checkList):
                raise ValueError("""every albums have been played. Can't create a
                        new playlist!""")

        self.CURRENT_ARTIST = random.choice(artists)

        pathToArtist = self.PATH_TO_DB/self.CURRENT_ARTIST

        albums = os.listdir(os.fspath(pathToArtist))

        #check if the album name is valid (will do if the album is not called
        #by those names)
        self.CURRENT_ALBUM = random.choice(albums)
        while self.CURRENT_ALBUM in ['desktop.ini','.DS_Store','']:
            self.CURRENT_ALBUM = random.choice(albums)

        self.PATH_TO_PLAYLIST = self.PATH_TO_DB / self.CURRENT_ARTIST / self.CURRENT_ALBUM

        #check if the album has already been played
        if self.check:
            if self.PATH_TO_PLAYLIST in checkList:
                self.create_playlist()

        tmp = list(self.PATH_TO_PLAYLIST.glob('*'))
        self.playlist = [os.fspath(i) for i in tmp]
        print(self.PATH_TO_PLAYLIST)

    def launch_playlist(self):
        """
        Launch the playlist with config["player"]
        """
        if self.PATH_TO_PLAYLIST == "":
            raise ValueError("The playlist is not reachable.\nMaybe create_playlist() must be called first.")
        if self.check:
            self.append_log()

        self.playlist.insert(0,config["player"])
        proc = subprocess.Popen(self.playlist, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        proc.wait()

play = Playlist(config["db"],config["log"])

def main():
    """
    -n play any album without checking if it has been already played,
       and dont add it to the check log.
    -l loop for another album when the first have been played without
       asking for it.
    """
    try:
        loop = False
        if '-n' in sys.argv:
            play.uncheck()
        loop = '-l' in sys.argv

        play.create_playlist()
        play.launch_playlist()

        if loop:
            while True:
                    play.create_playlist()
                    play.launch_playlist()
        else:
            while True:
                yesno = input("another ? [O/N]")
                if yesno.lower() in ['o','y','yes','oui']:
                    play.create_playlist()
                    play.launch_playlist()
                elif yesno.lower() in ['n','no','non']:
                    break
                else:
                    break
    except KeyboardInterrupt as e:
        print("\nOk then!")
    finally:
        print("Good Bye!")


if __name__ == '__main__':
    main()

