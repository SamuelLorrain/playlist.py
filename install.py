#!/usr/bin/python3

from pathlib import Path
import sys


if __name__ == "__main__":
    configString = """config = {
        "db":"%s",
        "log":"%s",
        "player":"%s"
    }
    """

    configFileCheck = Path('config.py')
    if configFileCheck.exists():
        raise ValueError("config file already exists")

    if '-n' not in sys.argv:
        db = input("what is the path to the db ? ")
        log = input("what is the path to the log file ? ")
        player = input("what program do you want to use to play music ?")

    with open('config.py','w') as configFile:
        configFile.write(configString % (db,log,player))

    if configFileCheck.exists():
        print("File generated!")
    else:
        print("error try to manually install file")
