from pathlib import Path
import os
import sys
import random
import subprocess

class Playlist:
    def __init__(self,bdd,log):
        self.PATH_TO_BDD = Path(bdd)
        self.PATH_TO_LOG = Path(log)
        self.CURRENT_ARTIST = ""
        self.CURRENT_ALBUM = ""
        self.PATH_TO_PLAYLIST = ""
        self.playlist = []

    def append_log(self):
        with open(os.fspath(self.PATH_TO_LOG),'a') as log:
            log.write(''.join((os.fspath(self.PATH_TO_PLAYLIST),'\n')))

    def create_playlist(self):
        artists = os.listdir(os.fspath(self.PATH_TO_BDD))
        self.CURRENT_ARTIST = random.choice(artists)

        pathToArtist = self.PATH_TO_BDD/self.CURRENT_ARTIST

        albums = os.listdir(os.fspath(pathToArtist))
        self.CURRENT_ALBUM = random.choice(albums)

        self.PATH_TO_PLAYLIST = self.PATH_TO_BDD / self.CURRENT_ARTIST / self.CURRENT_ALBUM

        #check if playlist have already been played
        checkList = []
        with open(os.fspath(self.PATH_TO_LOG),'r') as log:
            for i in log.readlines():
                checkList.append(i[0:-1])

        if self.PATH_TO_PLAYLIST in checkList:
            print("album already playlist")
            self.create_playlist()

        tmp = list(self.PATH_TO_PLAYLIST.glob('*'))
        self.playlist = [os.fspath(i) for i in tmp]
        print(self.PATH_TO_PLAYLIST)

    def launch_playlist(self):
        if self.PATH_TO_PLAYLIST == "":
            raise ValueError("create_playlist() must be called first")
        self.append_log()
        self.playlist.insert(0,'gnome-mpv')
        subprocess.Popen(self.playlist)

play = Playlist('/media/samuel/HITASHI/Musique','playlist.log')
play.create_playlist()
play.launch_playlist()
