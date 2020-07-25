def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def getIfromRGB(rgb):
    red = int(round(rgb[0]))
    green = int(round(rgb[1]))
    blue = int(round(rgb[2]))
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint