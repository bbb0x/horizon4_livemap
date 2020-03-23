import socket
import math
class Settings(object):
    port = 1642
    localIp = ""

# Coordinates used to calculate current position
    TR_GAMEX = 3151.970458984375
    TR_GAMEZ = 3340.1171875

    BL_GAMEX = -5523.37548828125
    BL_GAMEZ = -5096.015625

    TR_PICX = 1142
    TR_PICZ = 124

    BL_PICX = 30
    BL_PICZ = 1206


    def getLocalIpIntern():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            Settings.localIp = s.getsockname()[0]
            s.close()
        
    @staticmethod
    def getPort():
            return Settings.port

    @staticmethod
    def getLocalIp():
            Settings.getLocalIpIntern()
            return Settings.localIp

    @staticmethod 
    def getPixelPos(x,z):
            xT = (x-Settings.BL_GAMEX)/(Settings.TR_GAMEX-Settings.BL_GAMEX)
            yT = (z-Settings.BL_GAMEZ)/(Settings.TR_GAMEZ-Settings.BL_GAMEZ)

            xP = ((Settings.TR_PICX-Settings.BL_PICX)*xT)+Settings.BL_PICX
            yP = ((Settings.TR_PICZ-Settings.BL_PICZ)*yT)+Settings.BL_PICZ

            return xP,yP


