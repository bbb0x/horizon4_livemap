import socket
import _thread
import struct
from settings import Settings

class UdpRecorder(object):

    FH4BufSize = 324
    POSXPOS = 244
    POSYPOS = 248
    POSZPOS = 252
    YAW = 56

    def listen(self):
         self.sock.settimeout(3) # 3 seconds until timeout triggers. Experience shows that even 1 sec should be safe, but this program is not very time critical.
         while True:
          try:
            data, addr = self.sock.recvfrom(UdpRecorder.FH4BufSize)

            raceOn = data[0] == 1
         
            posX = struct.unpack('f',data[UdpRecorder.POSXPOS:UdpRecorder.POSXPOS+4])[0]
            posY = struct.unpack('f',data[UdpRecorder.POSYPOS:UdpRecorder.POSYPOS+4])[0]
            posZ = struct.unpack('f',data[UdpRecorder.POSZPOS:UdpRecorder.POSZPOS+4])[0]
            yaw = struct.unpack('f',data[UdpRecorder.YAW:UdpRecorder.YAW+4])[0]
        
            #print("X: "+(str)(posX)+" Y: "+(str)(posY)+" Z: "+(str)(posZ))
            #print(yaw)
            self.dataCallback(raceOn, posX,posY,posZ,yaw)
          except socket.timeout:
               self.timeoutCallback()

    def __init__(self, dataCallback, timeoutCallback):
      UDP_IP = Settings.getLocalIp()
      UDP_PORT = Settings.getPort()

      self.dataCallback = dataCallback
      self.timeoutCallback = timeoutCallback
    
      self.sock = socket.socket(socket.AF_INET, # Internet
      socket.SOCK_DGRAM) # UDP
      self.sock.bind((UDP_IP, UDP_PORT))
     
      _thread.start_new_thread(self.listen, () ) # recvform blocks thread until we get data - so freezes window. We might not want that I guess ;)
   
      
    
           