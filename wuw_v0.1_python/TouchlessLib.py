#coding=utf-8

#TouchlessLib模块定义
##标记物识别

import threading
import cv2.cv as cv
import Image
import wx

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
    pass

#RGB类定义

class RGB:
    pass

#Marker类定义
class Marker:
    pass
