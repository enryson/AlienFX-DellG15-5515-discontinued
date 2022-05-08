from functions.elc_ng import ELC, ColorCommand
from PIL import ImageColor


def conCo(color):
    newColor = int(color * 255)
    return newColor

def decCo(color):
    newColor = color / 255
    return newColor

def setColorHex(colorConfig):
    zone1 = ImageColor.getrgb(colorConfig.zone1)
    zone1 = ImageColor.getrgb(colorConfig.zone1)
    zone2 = ImageColor.getrgb(colorConfig.zone2)
    zone3 = ImageColor.getrgb(colorConfig.zone3)
    zone4 = ImageColor.getrgb(colorConfig.zone4)
    
    elc = ELC(0x187c, 0x0550)
    with elc:
        elc.execute(ColorCommand([8] , zone1[0],zone1[1],zone1[2]))
        elc.execute(ColorCommand([9] , zone2[0],zone2[1],zone2[2]))
        elc.execute(ColorCommand([10], zone3[0],zone3[1],zone3[2]))
        elc.execute(ColorCommand([11], zone4[0],zone4[1],zone4[2]))

def setColorRGB(zn1, zn2, zn3, zn4):
    elc = ELC(0x187c, 0x0550)
    with elc:
        elc.execute(ColorCommand([8] , conCo(zn1.red),conCo(zn1.green),conCo(zn1.blue)))
        elc.execute(ColorCommand([9] , conCo(zn2.red),conCo(zn2.green),conCo(zn2.blue)))
        elc.execute(ColorCommand([10], conCo(zn3.red),conCo(zn3.green),conCo(zn3.blue)))
        elc.execute(ColorCommand([11], conCo(zn4.red),conCo(zn4.green),conCo(zn4.blue)))
        
def setColorRGBOnly(zn1, zn2, zn3, zn4):
    elc = ELC(0x187c, 0x0550)
    with elc:
        elc.execute(ColorCommand([8] , zn1.r,zn1.g,zn1.b))
        elc.execute(ColorCommand([9] , zn2.r,zn2.g,zn2.b))
        elc.execute(ColorCommand([10], zn3.r,zn3.g,zn3.b))
        elc.execute(ColorCommand([11], zn4.r,zn4.g,zn4.b))