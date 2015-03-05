#coding=utf-8

#TouchlessLib模块定义
##标记物识别

import threading
import cv2.cv as cv
import Image
import wx
import numpy as np
import math
import time

#摄像头类定义
class Camera:
    
    def __init__(self, name="camera"):
        self.__name = name
        self.__height = 480
        self.__width = 640
        self.__img = None
        self.__imgLock = threading.RLock()
        self.__fpslimit = 30
        self.__cam = None

    @property
    def CaptureHeight(self):
        return self.__height
    @CaptureHeight.setter
    def CaptureHeight(self, value):
        self.__height = value

    @property
    def CaptureWidth(self):
        return self.__width
    @CaptureWidth.setter
    def CaptureWidth(self, value):
        self.__width = value

    @property
    def Fps(self):
        return self.__fpslimit
    @Fps.setter
    def Fps(self, value):
        self.__fpslimit = value

    def ToString(self):
        return self.__name

    def Start(self):
        if not self.isOn():
            self.__cam = cv.CaptureFromCAM(0)

    def Stop(self):
        if self.isOn():
            self.__cam = cv.CaptureFromCAM(0)
            self.__cam = None

    def isOn(self):
        if self.__cam == None:
            return False
        else:
            return True

    def ImageCaptured(self):
        self.__imgLock.acquire()
        img = cv.QueryFrame(self.__cam)
        self.__img = Image.fromstring("RGB", (self.__width, self.__height), img.tostring())
        self.__imgLock.release()

    def GetCurrentImage(self):
        self.__imgLock.acquire()
        if self.__img == None:
            img = None
        else:
          #  img = self.__img.copy()
            img = self.__img.transpose(Image.FLIP_LEFT_RIGHT)
        self.__imgLock.release()
        return img

    def Dispose(self):
        self.Stop()
        self.__img = None


#Image To Bitmap
def ImageToBitmap(img):
    img2 = wx.EmptyImage(img.size[0], img.size[1])
    img2.SetData(img.tostring())
    bitmap = wx.BitmapFromImage(img2)
    return bitmap


#HSV类定义
class HSV:
    def __init__(self, h=0,s=0,v=0):
        self.HSV_MAX_HUE = 360
        self.HSV_MAX_SAT = 255
        self.HSV_MAX_VAL = 255
        self.__h = h
        self.__s = s
        self.__v = v

    @property
    def Hue(self):
        return self.__h
    @Hue.setter
    def Hue(self, value):
        self.__h = value

    @property
    def Sat(self):
        return self.__s
    @Sat.setter
    def Sat(self, value):
        self.__s = value

    @property
    def Val(self):
        return self.__v
    @Val.setter
    def Val(self, value):
        self.__v = value

    @staticmethod
    def ConvertFromColor(c):
        return RGB.ConvertToHSV(RGB(c.Red(),c.Green(),c.Blue()))

    @staticmethod
    def ConvertToColor(hsv):
        rgb = HSV.ConvertToRGB(hsv)
        return wx.Colour(rgb.Red,rgb.Grn,rgb.Blu)

    @staticmethod
    def ConvertToRGB(hsv):
        num = (int)(hsv.Hue / 60) % 6
        num2 = (float)(hsv.Hue/60.0) - (int)(hsv.Hue/60)
        b = (int)(hsv.Val * (hsv.HSV_MAX_SAT - hsv.Sat) / hsv.HSV_MAX_SAT)
        r = (int)(hsv.Val * (hsv.HSV_MAX_SAT - (float)(num2*hsv.Sat)) / (float)(hsv.HSV_MAX_SAT))
        g = (int)(hsv.Val * (hsv.HSV_MAX_SAT - (float)(1.00-num2)*hsv.Sat) / (float)(hsv.HSV_MAX_SAT))
        if num == 0:
            return RGB(hsv.Val, g, b)
        elif num == 1:
            return RGB(r, hsv.Val, b)
        elif num == 2:
            return RGB(b, hsv.Val, g)
        elif num == 3:
            return RGB(b, r, hsv.Val)
        elif num == 4:
            return RGB(g, b, hsv.Val)
        elif num == 5:
            return RGB(hsv.Val, b, r)
        else:
            return RGB()

    @staticmethod
    def GetBinnedHSV(hsv, binCounts):
        h = (int)((hsv.Hue*(binCounts.Hue-1)) / hsv.HSV_MAX_HUE)
        s = (int)((hsv.Sat*(binCounts.Sat-1)) / hsv.HSV_MAX_SAT)
        v = (int)((hsv.Val*(binCounts.Val-1)) / hsv.HSV_MAX_VAL)
        return HSV(h,s,v)


#RGB类定义
class RGB:
    def __init__(self, r=0,g=0,b=0):
        self.HSV_MAX_RED = 255
        self.HSV_MAX_GRN = 255
        self.HSV_MAX_BLU = 255
        self.__r = r
        self.__g = g
        self.__b = b

    @property
    def Red(self):
        return self.__r
    @Red.setter
    def Red(self, value):
        self.__r = value

    @property
    def Grn(self):
        return self.__g
    @Grn.setter
    def Grn(self, value):
        self.__g = value

    @property
    def Blu(self):
        return self.__b
    @Blu.setter
    def Blu(self, value):
        self.__b = value

    @staticmethod
    def ConvertFromColor(c):
        return RGB(c.Red(),c.Green(),c.Blue())

    @staticmethod
    def ConvertToColor(rgb):
        return wx.Colour(rgb.Red,rgb.Grn,rgb.Blu)

    @staticmethod
    def ConvertToHSV(rgb):
        max_ = max(rgb.Red, rgb.Grn, rgb.Blu)
        min_ = min(rgb.Red, rgb.Grn, rgb.Blu)
        hsv = HSV()
        hsv.Val = max_
        if max_ == 0:
            hsv.Sat = 0
        else:
            hsv.Sat = (int)(255 * (max_ - min_) / max_)
        if max_ == min_:
            hsv.Hue = 0
            return hsv
        if rgb.Red == max_:
            hsv.Hue = (int)((60*(rgb.Grn-rgb.Blu)/(max_-min_) + 360) % 360)
            return hsv
        if rgb.Grn == max_:
            hsv.Hue = (int)(60*(rgb.Blu-rgb.Red)/(max_-min_) + 120)
            return hsv
        if rgb.Blu == max_:
            hsv.Hue = (int)(60*(rgb.Red-rgb.Grn)/(max_-min_) + 240)
            return hsv

#ScanCommand定义：True为addMarker,False为remMarker


#MarkerScanCommand类定义
class MarkerScanCommand:
    def __init__(self, m, c, i):
        self.marker = m
        self.command = c
        self.coordinate = i


#MarkerEventData类定义
class MarkerEventData:
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__dx = 0
        self.__dy = 0
        self.__present = False
        self.__area = 0
        self.__bounds = None
        self.__colorAvg = None
        self.__timestamp = None
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0

    @property
    def X(self):
        return self.__x
    @X.setter
    def X(self, value):
        self.__x = value

    @property
    def Y(self):
        return self.__y
    @Y.setter
    def Y(self, value):
        self.__v = value

    @property
    def DX(self):
        return self.__dx
    @DX.setter
    def DX(self, value):
        self.__dx = value

    @property
    def DY(self):
        return self.__dy
    @DY.setter
    def DY(self, value):
        self.__dy = value

    @property
    def Present(self):
        return self.__present
    @Present.setter
    def Present(self, value):
        self.__present = value

    @property
    def ColorAvg(self):
        return self.__colorAvg
    @ColorAvg.setter
    def ColorAvg(self, value):
        self.__colorAvg = value

    @property
    def Area(self):
        return self.__area
    @Area.setter
    def Area(self, value):
        self.__area = value

    @property
    def Bounds(self):
        return self.__bounds
    @Bounds.setter
    def Bounds(self, value):
        self.__bounds = value

    @property
    def Timestamp(self):
        return self.__timestamp
    @Timestamp.setter
    def Timestamp(self, value):
        self.__timestamp = value

    
#Marker类定义
class Marker:
    def __init__(self, name):
        self.__name = name
        self.__highlight = True
        self.__smoothingEnabled = True
        self.smoothingFactor = 0.55
        self.searchMinX = MarkerScanCommand(self, True, 0)
        self.searchMaxX = MarkerScanCommand(self, False, 0)
        self.searchMinY = MarkerScanCommand(self, True, 0)
        self.searchMaxY = MarkerScanCommand(self, False, 0)
        self.binsHue = 0
        self.binsSat = 0
        self.binsVal = 0
        self.__currData = None
        self.__frequencyThreshhold = 0
        self.__lastGoodData = None
        self.__prevData = None
        self.__provideCalculatedProperties = False
        self.__representativeColor = None

    @property
    def CurrentData(self):
        return self.__currData
    @CurrentData.setter
    def CurrentData(self, value):
        self.__currData = value

    @property
    def Highlight(self):
        return self.__highlight
    @Highlight.setter
    def Highlight(self, value):
        self.__highlight = value

    @property
    def LastGoodData(self):
        return self.__lastGoodData
    @LastGoodData.setter
    def LastGoodData(self, value):
        self.__lastGoodData = value

    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, value):
        self.__name = value

    @property
    def PreviousData(self):
        return self.__prevData
    @PreviousData.setter
    def PreviousData(self, value):
        self.__prevData = value

    @property
    def ProvideCalculatedProperties(self):
        return self.__provideCalculatedProperties
    @ProvideCalculatedProperties.setter
    def ProvideCalculatedProperties(self, value):
        self.__provideCalculatedProperties = value

    @property
    def RepresentativeColor(self):
        return self.__representativeColor
    @RepresentativeColor.setter
    def RepresentativeColor(self, value):
        self.__representativeColor = value

    @property
    def SmoothingEnabled(self):
        return self.__smoothingEnabled
    @SmoothingEnabled.setter
    def SmoothingEnabled(self, value):
        self.__smoothingEnabled = value

    @property
    def Threshold(self):
        return self.__frequencyThreshhold
    @Threshold.setter
    def Threshold(self, value):
        self.__frequencyThreshhold = value

    def ToString(self):
        return self.__name

    def SetMarkerAppearance(self, rawHsvFreq):
        shape = rawHsvFreq.shape
        self.binsHue = (int)(shape[0])
        self.binsSat = (int)(shape[1])
        self.binsVal = (int)(shape[2])
        self.__representativeColor = wx.Colour(0,0,0)
        num = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        for i in range(self.binsHue):
            for j in range(self.binsSat):
                for k in range(self.binsVal):
                    if rawHsvFreq[i,j,k] > 0:
                        num += rawHsvFreq[i,j,k]
                        num3 += rawHsvFreq[i,j,k] * i
                        num4 += rawHsvFreq[i,j,k] * j
                        num5 += rawHsvFreq[i,j,k] * k
                        num2 += 1
        if num2 == 0:
            return False
        self.Threshold = (int)((2 * num) / num2)
        self.__representativeColor = HSV.ConvertToColor(HSV((int)(num3/num),(int)(num4/num),(int)(num5/num)))
        return True


#TouchlessMgr类定义
class TouchlessMgr:
    def __init__(self):
        self.__markers = []
        self.__markerScanCommandsX = []
        self.__markerScanCommandsY = []
        self.__scanMarkersX = []
        self.__scanMarkersY = []
        self.__cameras = []
        self.__camHeight = 0
        self.__camWidth = 0
        self.__currentCamera = None

    @property
    def Cameras(self):
        return self.__cameras

    @property
    def CurrentCamera(self):
        return self.__currentCamera
    @CurrentCamera.setter
    def CurrentCamera(self, value):
        self.__currentCamera = value

    @property
    def MarkersCount(self):
        return len(self.__markers)

    @property
    def Markers(self):
        return self.__markers

    def AddMarker(self, name, img, center, radius):
        item = Marker(name)
        item.SetMarkerAppearance(self.GetMarkerAppearance(img, center, radius))
        self.__markers.append(item)
        return item

    def CleanupCameras(self):
        if not self.__currentCamera == None:
            self.__currentCamera.Stop()
        self.__cameras = []
        self.__currentCamera = None

    def __del__(self):
        self.CleanupCameras()
        self.__markers = []

    def GetMarkerAppearance(self, img, center, radius, binCounts=HSV(40,20,10)):
        height = img.size[1]
        width = img.size[0]
        numArray = np.zeros((binCounts.Hue,binCounts.Sat,binCounts.Val))
        flag = False
        for i in range(height):
            for j in range(width):
                data = img.getpixel((j,i))
                binnedHSV = HSV.GetBinnedHSV(RGB.ConvertToHSV(RGB(data[0],data[1],data[2])),binCounts)
                num = j - center.x
                num2 = i - center.y
                flag = math.sqrt(num*num+num2*num2) < radius
                if flag:
                    numArray[binnedHSV.Hue,binnedHSV.Sat,binnedHSV.Val] += 2
                else:
                    numArray[binnedHSV.Hue,binnedHSV.Sat,binnedHSV.Val] -= 1
        return numArray

    def postProcessMarker(self, marker):
    #    marker.currData.Timestamp =
        if marker.currData.Area > 0:
            marker.currData.Present = True
            #marker.currData.ColorAvg =
            marker.currData.X /= marker.currData.Area
            marker.currData.Y /= marker.currData.Area
            marker.currData.Bounds = wx.Rect(marker.currData.left,marker.currData.top,marker.currData.right-marker.currData.left,marker.currData.bottom-marker.currData.top)
            if marker.prevData.

    def preProcessMarker(self, marker, imgWidth, imgHeight):
        pass

    def RefreshCameraList(self):
        self.CleanupCameras()
        self.__cameras = []
        self.__currentCamera = Camera()
        self.__camHeight = self.__currentCamera.CaptureHeight
        self.__camWidth = self.__currentCamera.CaptureWidth
        self.__cameras.append(self.__currentCamera)
        self.__currentCamera.Start()

    def RemoveMarker(self, index):
        count = len(self.__markers)
        if index < 0 or index >= count:
            raise IndexError("index")
        self.__markers.pop(index)

    def UpdateMarkers(self, img):
        pass
