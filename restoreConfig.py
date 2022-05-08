
from functions.fileStorage import loadConfig
from functions.color import setColorRGBOnly
from classes.color_zone import ColorZones

class ColorZones:
    def __init__(self,data):
        self.r = data[0]
        self.g = data[1]
        self.b = data[2]
    pass

def decode(data):
    outpu = ColorZones(data[0],data[1],data[2])
    return outpu

config = loadConfig()
zn1 = ColorZones(config['z1'])
zn2 = ColorZones(config['z2'])
zn3 = ColorZones(config['z3'])
zn4 = ColorZones(config['z4'])

setColorRGBOnly(zn1, zn2, zn3, zn4)