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
# - Checker des types de fichiers (virer les desktop.ini, les Folder.jpg etc.)
# - Meilleure gestion de gnome-mpv (api mpv à la place ?)
# - mise en cache
#
############################################################################

class Playlist:
    def __init__(self,bdd,log,check=True):
        self.check=check
        self.PATH_TO_BDD = Path(bdd)
        if not self.PATH_TO_BDD.exists():
            raise ValueError("the bdd does not exist, unable to create playlist!")
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
        self.check=False

    def append_log(self):
        with open(os.fspath(self.PATH_TO_LOG),'a') as log:
            log.write(''.join((os.fspath(self.PATH_TO_PLAYLIST),'\n')))

    def create_playlist(self):
        checkList = []
        artists = os.listdir(os.fspath(self.PATH_TO_BDD))

        #CHECK FOR LOG ERROR
        if self.check:
            with open(os.fspath(self.PATH_TO_LOG),'r') as log:
                for i in log.readlines():
                    checkList.append(i[0:-1])
            if len(artists) < len(checkList):
                raise ValueError("""every albums have been played. Can't create a
                        new playlist!""")

        self.CURRENT_ARTIST = random.choice(artists)

        pathToArtist = self.PATH_TO_BDD/self.CURRENT_ARTIST

        albums = os.listdir(os.fspath(pathToArtist))
        self.CURRENT_ALBUM = random.choice(albums)

        self.PATH_TO_PLAYLIST = self.PATH_TO_BDD / self.CURRENT_ARTIST / self.CURRENT_ALBUM

        #check if the album has already been played
        if self.check:
            if self.PATH_TO_PLAYLIST in checkList:
                self.create_playlist()

        tmp = list(self.PATH_TO_PLAYLIST.glob('*'))
        self.playlist = [os.fspath(i) for i in tmp]
        print(self.PATH_TO_PLAYLIST)

    def launch_playlist(self):
        if self.PATH_TO_PLAYLIST == "":
            raise ValueError("create_playlist() must be called first")
        if self.check:
            self.append_log()

        #self.playlist.insert(0,'--no-audio-display')
        self.playlist.insert(0,'gnome-mpv')
        proc = subprocess.Popen(self.playlist, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
        proc.wait()

play = Playlist(config["bdd"],config["log"])

def main():
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

