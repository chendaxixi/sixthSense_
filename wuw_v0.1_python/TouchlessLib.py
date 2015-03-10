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
        self.CaptureHeight = 480
        self.CaptureWidth = 640
        self.__img = None
        self.__imgLock = threading.RLock()
        self.Fps = 30
        self.__cam = None

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
        self.__img = Image.fromstring("RGB", (self.CaptureWidth, self.CaptureHeight), img.tostring())
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
        self.Hue = h
        self.Sat = s
        self.Val = v

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
        self.Red = r
        self.Grn = g
        self.Blu = b

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
        self.X = 0
        self.Y = 0
        self.DX = 0
        self.DY = 0
        self.Present = False
        self.Area = 0
        self.Bounds = wx.Rect(0,0,0,0)
        self.ColorAvg = None
        self.Timestamp = time.time()
        self.top = 480 
        self.bottom = 0
        self.left = 640
        self.right = 0

#ColorKey类定义
class ColorKey:
    def __init__(self, h=HSV()):
        self.hsv = h
        self.key = (h.Hue+(h.Sat*h.HSV_MAX_HUE))+((h.Val*h.HSV_MAX_SAT)*h.HSV_MAX_HUE)

    def SetHsv(self, value):
        self.hsv = value
        self.key = (value.Hue+(value.Sat*value.HSV_MAX_HUE))+((value.Val*value.HSV_MAX_SAT)*value.HSV_MAX_HUE)

#Marker类定义
class Marker:
    def __init__(self, name):
        self.Name = name
        self.Highlight = True
        self.SmoothingEnabled = True
        self.smoothingFactor = 0.55
        self.searchMinX = MarkerScanCommand(self, True, 0)
        self.searchMaxX = MarkerScanCommand(self, False, 0)
        self.searchMinY = MarkerScanCommand(self, True, 0)
        self.searchMaxY = MarkerScanCommand(self, False, 0)
        self.binsHue = 0
        self.binsSat = 0
        self.binsVal = 0
        self.CurrData = MarkerEventData()
        self.Threshold = 0
        self.LastGoodData = None
        self.PreviousData = MarkerEventData()
        self.ProvideCalculatedProperties = False
        self.RepresentativeColor = None
        self.hsvFreq = {}
        self.OnChange = None

    def ToString(self):
        return self.__name

    def SetMarkerAppearance(self, rawHsvFreq):
        shape = rawHsvFreq.shape
        self.binsHue = (int)(shape[0])
        self.binsSat = (int)(shape[1])
        self.binsVal = (int)(shape[2])
        self.RepresentativeColor = wx.Colour(0,0,0)
        num = 0
        num2 = 0
        num3 = 0
        num4 = 0
        num5 = 0
        for i in range(self.binsHue):
            for j in range(self.binsSat):
                for k in range(self.binsVal):
                    if rawHsvFreq[i,j,k] > 0:
                        key = str.format("{0}", ColorKey(HSV(i,j,k)).key)
                        self.hsvFreq[key] = rawHsvFreq[i,j,k]
                        num += rawHsvFreq[i,j,k]
                        num3 += rawHsvFreq[i,j,k] * i
                        num4 += rawHsvFreq[i,j,k] * j
                        num5 += rawHsvFreq[i,j,k] * k
                        num2 += 1
        print self.hsvFreq
        if num2 == 0:
            return False
        self.Threshold = (int)((2 * num) / num2)
        num3 /= num2
        num3 %= 360
        num4 /= num2
        num4 %= 255
        num5 /= num2
        num5 %= 255
        self.RepresentativeColor = HSV.ConvertToColor(HSV(num3,num4,num5))
        return True

    def FireMarkerEventData(self):
        if not self.OnChange == None:
            self.OnChange(self.CurrData)

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
        self.CurrentCamera = None
        self.lock = threading.RLock()

    def MarkerScanCommandComparison(self, obj1, obj2):
        if obj1.coordinate > obj2.coordinate:
            return 1
        elif obj1.coordinate == obj2.coordinate:
            return 0
        else:
            return -1

    @property
    def Cameras(self):
        return self.__cameras

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
        if not self.CurrentCamera == None:
            self.CurrentCamera.Stop()
        self.__cameras = []
        self.CurrentCamera = None

    def __del__(self):
        self.CleanupCameras()
        self.__markers = []

    def CaptureCallbackProc(self):
        if not self.CurrentCamera == None:
            self.CurrentCamera.ImageCaptured()
            self.UpdateMarkers(self.CurrentCamera.GetCurrentImage())

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
        marker.CurrData.Timestamp = time.time()
        if marker.CurrData.Area > 0:
            marker.CurrData.Present = True
            marker.CurrData.ColorAvg = marker.RepresentativeColor
            marker.CurrData.X /= marker.CurrData.Area
            marker.CurrData.Y /= marker.CurrData.Area
            marker.CurrData.Bounds = wx.Rect(marker.CurrData.left,marker.CurrData.top,marker.CurrData.right-marker.CurrData.left,marker.CurrData.bottom-marker.CurrData.top)
            if marker.PreviousData.Present:
                marker.CurrData.DX = marker.CurrData.X-marker.PreviousData.X
                marker.CurrData.DY = marker.CurrData.Y-marker.PreviousData.Y
            if marker.SmoothingEnabled:
                marker.CurrData.X = (marker.CurrData.X+((marker.CurrData.Bounds.left+marker.CurrData.Bounds.right)/2))/2
                marker.CurrData.Y = (marker.CurrData.Y+((marker.CurrData.Bounds.top+marker.CurrData.Bounds.bottom)/2))/2
                if marker.PreviousData.Present:
                    smoothingFactor = marker.smoothingFactor
                    num2 = 1.00-smoothingFactor
                    marker.CurrData.Area = (int)((smoothingFactor*marker.CurrData.Area)+(num2*marker.PreviousData.Area))
                    marker.CurrData.X=(int)((smoothingFactor*marker.CurrData.X)+(num2*marker.PreviousData.X))
                    marker.CurrData.Y=(int)((smoothingFactor*marker.CurrData.Y)+(num2*marker.PreviousData.Y))
                    marker.CurrData.DX = marker.CurrData.X - marker.PreviousData.X
                    marker.CurrData.DY = marker.CurrData.Y - marker.PreviousData.Y
                    marker.CurrData.top = (int)((smoothingFactor*marker.CurrData.top)+(num2*marker.PreviousData.top))
                    marker.CurrData.bottom = (int)((smoothingFactor*marker.CurrData.bottom)+(num2*marker.PreviousData.bottom))
                    marker.CurrData.left = (int)((smoothingFactor*marker.CurrData.left)+(num2*marker.PreviousData.left))
                    marker.CurrData.right = (int)((smoothingFactor*marker.CurrData.right)+(num2*marker.PreviousData.right))
                    marker.CurrData.Bounds = wx.Rect(marker.CurrData.left,marker.CurrData.top,marker.CurrData.right-marker.CurrData.left,marker.CurrData.bottom-marker.CurrData.top)
                marker.FireMarkerEventData()
            else:
                marker.CurrData.Present = False
                            
    def preProcessMarker(self, marker, imgWidth, imgHeight):
        if marker.PreviousData.Present:
            marker.lastGoodData = marker.PreviousData
        if marker.CurrData.Present:
            marker.lastGoodData = marker.CurrData
        marker.PreviousData = marker.CurrData
        marker.CurrData = MarkerEventData()
        if marker.PreviousData.Present:
            num = imgWidth / 20
            num2 = imgHeight / 20
            if marker.PreviousData.DX < 0:
                num3 = 0.25
            else:
                num3 = 4.00
            if marker.PreviousData.DY < 0:
                num4 = 0.25
            else:
                num4 = 4.00
            marker.searchMinX.coordinate = ((marker.PreviousData.left+((int)(((float)(marker.PreviousData.DX))/num3)))-(marker.PreviousData.Bounds.Width / 3)) - num
            marker.searchMaxX.coordinate = ((marker.PreviousData.right+((int)(marker.PreviousData.DX*num3)))+(marker.PreviousData.Bounds.Width / 3)) + num
            marker.searchMinY.coordinate = ((marker.PreviousData.top+((int)(((float)(marker.PreviousData.DY))/num4)))-(marker.PreviousData.Bounds.Height / 3)) - num2
            marker.searchMaxY.coordinate = ((marker.PreviousData.bottom+((int)(marker.PreviousData.DY*num4)))+(marker.PreviousData.Bounds.Height / 3)) + num2
            marker.searchMinX.coordinate = max(marker.searchMinX.coordinate,0)
            marker.searchMaxX.coordinate = min(marker.searchMaxX.coordinate,imgWidth-1)
            marker.searchMinY.coordinate = max(marker.searchMinY.coordinate,0)
            marker.searchMaxY.coordinate = min(marker.searchMaxY.coordinate,imgHeight-1)
            data = marker.PreviousData
        else:
            marker.searchMinX.coordinate = 0
            marker.searchMinY.coordinate = 0
            marker.searchMaxX.coordinate = imgWidth-1
            marker.searchMaxY.coordinate = imgHeight -1
        marker.CurrData.top = imgHeight
        marker.CurrData.bottom = 0
        marker.CurrData.left = imgWidth
        marker.CurrData.right = 0

    def RefreshCameraList(self):
        self.CleanupCameras()
        self.__cameras = []
        self.CurrentCamera = Camera()
        self.__camHeight = self.CurrentCamera.CaptureHeight
        self.__camWidth = self.CurrentCamera.CaptureWidth
        self.__cameras.append(self.CurrentCamera)
        self.CurrentCamera.Start()

    def RemoveMarker(self, index):
        count = len(self.__markers)
        if index < 0 or index >= count:
            raise IndexError("index")
        self.__markers.pop(index)

    def UpdateMarkers(self, img):
        if self.MarkersCount == 4:
            self.lock.acquire()
            t1 = time.time()
            hsv = HSV()
            flag = True
            key = ColorKey()
            array = self.__markers[:]
            self.__markerScanCommandsY = []
            for marker in self.__markers:
                self.preProcessMarker(marker,img.size[0],img.size[1])
                self.__markerScanCommandsY.append(marker.searchMinY)
                self.__markerScanCommandsY.append(marker.searchMaxY)
            self.__markerScanCommandsY.sort(cmp=self.MarkerScanCommandComparison)
            counts = len(self.__markerScanCommandsY)
            for i in range(counts):
                if self.__markerScanCommandsY[i].command:
                    self.__scanMarkersY.append(self.__markerScanCommandsY[i].marker)
                else:
                    self.__scanMarkersY.remove(self.__markerScanCommandsY[i].marker)
                if not len(self.__scanMarkersY) == 0:
                    self.__markerScanCommandsX = []
                    for marker in self.__scanMarkersY:
                        self.__markerScanCommandsX.append(marker.searchMinX)
                        self.__markerScanCommandsX.append(marker.searchMaxX)
                    self.__markerScanCommandsX.sort(cmp = self.MarkerScanCommandComparison)
                    count = len(self.__markerScanCommandsX)
                    for j in range(count):
                        if self.__markerScanCommandsX[j].command:
                            self.__scanMarkersX.append(self.__markerScanCommandsX[j].marker)
                        else:
                            self.__scanMarkersX.remove(self.__markerScanCommandsX[j].marker)
                        if not len(self.__scanMarkersX) == 0:
                            if (counts < (i+1)) or (count <(j+1)):
                                raise AssertionError("This state should never be reached, this means that we are processing in an area after an add command, but not before a remove command, check search bounds for inversion")
                            for k in range(self.__markerScanCommandsY[i].coordinate,self.__markerScanCommandsY[i+1].coordinate+1):
                                xy = (self.__markerScanCommandsX[j].coordinate,k)
                                coordinate = self.__markerScanCommandsX[j].coordinate
                                while coordinate <= self.__markerScanCommandsX[j+1].coordinate:
                                    flag = True
                                    for marker in self.__scanMarkersX:
                                        if flag:
                                            rgb = img.getpixel(xy)
                                            hsv = RGB.ConvertToHSV(RGB(rgb[0],rgb[1],rgb[2]))
                                            flag = False
                                        if (marker.Highlight and marker.PreviousData.Present) and (((coordinate == marker.searchMinX.coordinate)or(coordinate == marker.searchMaxX.coordinate))or((k == marker.searchMinY.coordinate)or(k == marker.searchMaxY.coordinate))):
                                            color = marker.RepresentativeColor
                                            img.putpixel(xy,(color.red,color.green,color.blue))
                                        key.SetHsv(HSV.GetBinnedHSV(hsv,HSV(marker.binsHue,marker.binsSat,marker.binsVal)))
                                        key_ = str.format("{0}", key.key)
                                        if marker.hsvFreq.has_key(key_) and ((int)(marker.hsvFreq[key_]) > marker.Threshold):
                                            marker.CurrData.Area += 1
                                            marker.CurrData.X += coordinate
                                            marker.CurrData.Y += k
                                            if k < marker.CurrData.top:
                                                marker.CurrData.top = k
                                            if k > marker.CurrData.bottom:
                                                marker.CurrData.bottom = k
                                            if coordinate < marker.CurrData.left:
                                                marker.CurrData.left = coordinate
                                            if coordinate > marker.CurrData.right:
                                                marker.CurrData.right = coordinate
                                            if marker.Highlight:
                                                color = marker.RepresentativeColor
                                                img.putpixel(xy,(color.red,color.green,color.blue))
                                    coordinate += 1
                                    xy = (coordinate, k)
            for marker in array:
                self.postProcessMarker(marker)
            print time.time() - t1
            self.lock.release()

            
