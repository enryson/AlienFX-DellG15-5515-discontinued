# responsable of create a config file
import os
import json
from pathlib import Path
from functions.color import (conCo, decCo)
from gi.repository import Gdk

path = os.environ['HOME'] + "/.local/share/AlienFx"
pathFile = os.path.join(path, "AlienFx.conf")

def encColor(zone):
    arrColor = [conCo(zone.red), conCo(zone.green), conCo(zone.blue)]
    return arrColor

def decColor(zone):
    arrColor = Gdk.RGBA(decCo(zone[0]), decCo(zone[1]), decCo(zone[2]), 1)
    return arrColor

def createConfig():
    colorConfig = {
        "z1": [87, 227, 137],
        "z2": [87, 227, 137],
        "z3": [87, 227, 137],
        "z4": [87, 227, 137]
    }
    # create folder on the local share folder
    if not os.path.exists(path):
        os.mkdir(path)
    # create file if not exists
    fle = Path(pathFile)
    fle.touch(exist_ok=True)
    # store base config file
    with open(pathFile, 'w') as f:
        json.dump(colorConfig, f)

def loadConfig():
    with open(pathFile, 'r') as f:
        return json.load(f)

def checkFileExists():
    try:
        fle = Path(pathFile)
        fle.touch(exist_ok=True)
        with open(pathFile, 'r') as f:
            return True
    except IOError:
        return False

def readConfig():
    fileExists = checkFileExists()
    if not fileExists:
        createConfig()
    config = loadConfig()
    z1 = decColor(config['z1'])
    z2 = decColor(config['z2'])
    z3 = decColor(config['z3'])
    z4 = decColor(config['z4'])
    return z1, z2, z3, z4

def updateConfig(zone1, zone2, zone3, zone4):
    z1 = encColor(zone1)
    z2 = encColor(zone2)
    z3 = encColor(zone3)
    z4 = encColor(zone4)
    try:
        loadConfig()
    except IOError:
        createConfig(z1, z2, z3, z4)
    finally:
        config = loadConfig()
        # edit the data
        config['z1'] = z1
        config['z2'] = z2
        config['z3'] = z3
        config['z4'] = z4
        # write it back to the file
        with open(pathFile, 'w') as f:
            json.dump(config, f)
