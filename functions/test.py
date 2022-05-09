from elc_ng import ELC, ColorCommand

elc = ELC(0x187c, 0x0550)
with elc:
    elc.execute(ColorCommand([8] , 255,255,255))