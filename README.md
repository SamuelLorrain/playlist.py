#playlist.py

A little program used to launch music randomly choosen in
a directory.

The main purpose is to play music in a DB without using any DB system
such as *Itunes* or *Clementine*. But, the only thing you can do is to play
an album randomly. I also wanted to keep track of albums
that I had already played, so I can listen to something different
everytime.

##Prerequisites

1. Only work with python3
2. Ensure that your music folder is in the form
   `folder/artists/albums/music.xxx`

##Install

1. launch `./install.py`, the install script will ask you to
   choose the path to your music, a folder to keep the log file
   and the name of the program used to play music.
   Note that the program have only been tested on Linux, with
   *gnome-mpv* and *vlc*. It may not work with terminal
   music players such as *ncmpcpp* because *playlist.py* use 
   subprocess to launch the player, which let *playlist.py*
   be the main command on the terminal (it may be fixed later).
   an example of config file:
   ```
   config = {
    "bdd":"/home/samuel/Documents/Music",
    "log":"/home/samuel/.config/playlist/playlist.log",
    "player":"gnome-mpv"
   }
   ```
2. launch `./playlist.py` with or without options.
3. Enjoy!

##Usage

- *-n*, dont keep track of albums already played
- *-l*, loop through albums without confirm

##Todo

- Caching system
- Check filetypes to only play music
- Add terminal player support

