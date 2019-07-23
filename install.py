#!/usr/bin/python3

from pathlib import Path
import sys


if __name__ == "__main__":
    configString = """config = {
        "bdd":"%s",
        "log":"%s"
        "player":"%s"
    }
    """

    configFileCheck = Path('config.py')
    if configFileCheck.exists():
        raise ValueError("config file already exists")

    if '-n' not in sys.argv:
        bdd = input("what is the path to the bdd ? ")
        log = input("what is the path to the log file ? ")
        player = input("what program do you want to use to play music ?")

    with open('config.py','w') as configFile:
        configFile.write(configString % (bdd,log,player))

    if configFileCheck.exists():
        print("File generated!")
    else:
        print("error try to manually install file")
