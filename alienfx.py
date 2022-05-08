#class of ColorZone
from classes.color_zone import ColorZones
#set Color function
from functions.color import setColorHex
#save config
from functions.fileStorage import updateConfig

z1 = str(input())
z2 = str(input())
z3 = str(input())
z4 = str(input())

color = ColorZones(z1, z2, z3, z4)
updateConfig(z1, z2, z3, z4)
setColorHex(color)