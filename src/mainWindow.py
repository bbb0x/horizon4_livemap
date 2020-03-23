import wx
from settings import Settings
from udpRecorder import UdpRecorder
from fileHelper import FileHelper
import math

class MainWindow(wx.Frame):

    i = 50

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 300))
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0
        self.connected = False
        self.bm = wx.Bitmap(FileHelper.getPath("gfx/fh4map_main.jpg"))
        img = wx.Image(FileHelper.getPath("gfx/fh4map_main.jpg")) # need it as Image too very temporarely, just to fetch its initial size.
        self.rawImgW = img.Width
        self.rawImgH = img.Height
        img.Destroy()
        self.carBm = wx.Bitmap(FileHelper.getPath("gfx/car.png"))
        titleHeight = self.GetRect().height-self.GetClientRect().height
        self.SetSize(self.rawImgW/1.5,self.rawImgH/1.5 + (titleHeight/1.5)) # the last part is broken, (not a direct formula, but seems to work on windows at least). It seems to be hard to size the window exactly.
       
        self.InitUI()
        self.recorder = UdpRecorder(self.udpReceivedData, self.udpTimeout)

       

    def InitUI(self):
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize) 
        self.Bind(wx.EVT_IDLE, self.OnIdle)  
        self.Centre()
        self.Show(True)

    def InitBuffer(self):
        self.client_size = self.GetClientSize()
        self.buffer = wx.Bitmap(
        self.client_size.width, self.client_size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        gc.SetAntialiasMode(wx.ANTIALIAS_DEFAULT) 
        gc.SetInterpolationQuality(wx.INTERPOLATION_BEST)
        self.draw(gc)
        self.reInitBuffer = False

    def OnSize(self, event):
        self.reInitBuffer = True
        self.InitBuffer()
        self.Refresh(False)

    def OnIdle(self, event):
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)

    def draw(self, gc):
        size = self.client_size

        imgw = self.rawImgW
        imgh = self.rawImgH
        aspectRatio = imgw/imgh
        topMargin = 0
        # Resize it, but keep the aspect ratio. Add 'margins' to ensure.
        height = size.height
        width = min(size.width, round(height*aspectRatio))
        if width == size.width:
             height = round(width/aspectRatio)
             topMargin = round((size.height-height)/2)
       
        leftMargin = round((size.width)-width)/2
      
 
        gc.DrawBitmap(self.bm,leftMargin,topMargin, width, height)
        refWidth = 314
        refWidthContentSize = 10
        multiplicator = width/refWidth

        if not self.connected:
          # Darken background and tell user what to do to connect.
          brush = wx.Brush(wx.Colour(0,0,0,0xff*0.8),wx.BRUSHSTYLE_SOLID)
          gc.SetBrush(brush)
          gc.DrawRectangle(leftMargin,topMargin,width,height)       
     
          font =  gc.CreateFont(wx.Font(refWidthContentSize*multiplicator, wx.SWISS, wx.NORMAL, wx.BOLD),wx.Colour(255,255,255))
          gc.SetFont(font)

          text = "Not connected to Forza Horizon 4.\n\nPlease enter the following details at\nHome > Settings > Hud in the game:\n\nIP Address: "+ (str)(Settings.getLocalIp())+"\nPort: "+ (str)(Settings.getPort())
          textSize = gc.GetTextExtent(text)

          textX = leftMargin+(width/2)-(textSize[0]/2)
          textY = topMargin+(height/2)-(textSize[1]/2)
          gc.DrawText(text,textX,textY)
        else:
          xp,yp =  Settings.getPixelPos(self.x,self.z)

          # We know got the pixel location. But this is according to the source image, not to the current size which is displayed.
          # Calibration was very hard. This was supposed to be calculated against the image size, but I had to manually adjust them. Nothing to worry, just leave it like that.
          xp*=(width/1461)
          yp*=(height/1417)

          # Also consider the margin, if it has any. 
          xp+=leftMargin
          yp+=topMargin

          refcw = 10
          cw = refcw * multiplicator

          # draw a secondary circle that lights up the area, to make the users eye catch the position more early
          scs = cw*15
          brush =wx.Brush(wx.Colour(255,255,255,0xff*0.15))
          gc.SetBrush(brush)
          gc.DrawEllipse(xp-scs/2,yp-scs/2,scs,scs)

          # draw main position circle
          brush =wx.Brush(wx.Colour(0,0,100,0xff*0.4))
          gc.SetBrush(brush)
          pen = wx.Pen(wx.Colour(255,0,0),cw/12)
          gc.SetPen(pen)
          gc.DrawEllipse(xp-cw/2,yp-cw/2,cw,cw)

          gc.SetPen(wx.Pen())

          # inner dot

          ids = cw/10
          brush =wx.Brush(wx.Colour(255,255,0))
          gc.SetBrush(brush)
          gc.DrawEllipse(xp-ids/2,yp-ids/2,ids,ids)

          # draw a car inside of it, Note: Commented it out. Looks ugly because bitmaps are always placed by full pixel for some reason, only drawables are smooth.
          # carCs = cw/1.5
          # dc.DrawBitmap(self.carBm, xp- carCs/2,yp- carCs/2, carCs, carCs)

          # draw yaw angle graphic
          gc.SetBrush(wx.Brush())
          gc.SetPen(wx.Pen(wx.Colour(100,0,255,0xff*0.7),cw/8))
          path = gc.CreatePath()
          distance = math.pi/4
          yaw = self.yaw - math.pi/2 # default orientation is incorrect, so fixing it here.
          path.AddArc(xp,yp,(cw/2)+cw/6,yaw-distance,yaw+distance,True)
    
          gc.DrawPath(path)

  

    def OnPaint(self, e):
        wx.BufferedPaintDC(self, self.buffer)
       

    def scale_bitmap(self, img, width, height):
        image = img.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.Bitmap(image)
        return result

    def udpTimeout(self):
        was = self.connected
        self.connected = False

        if was:
           self.reInitBuffer = True # redraw
           self.Refresh(False)
       

    def udpReceivedData(self, raceOn, x,y,z,yaw):
        was = self.connected
        self.connected = True

        if not was:
           self.reInitBuffer = True
           self.Refresh(False)
        
        if raceOn: # only update when not paused, otherwise we jump back at position 0,0,0
          self.yaw = yaw
          self.x = x
          self.y = y
          self.z = z
          self.reInitBuffer = True
          self.Refresh(False)

