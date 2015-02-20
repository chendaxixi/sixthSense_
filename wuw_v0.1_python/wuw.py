#coding=utf-8

"""
** WUW Python
** Chendaxixi
** SixthSense Group
** Date: 2015/02/10
"""

#WUW应用
##包括窗口建立和响应函数

import wx
from classes.Value import Value
import threading
import TouchlessLib
import time

class WuwPanel(wx.Panel):
    Width = Value.WuwWidth
    Height = Value.WuwHeight
    def __init__(self, parent):
        self.Grid = self.Width / 100
        wx.Panel.__init__(self, parent)

        #构建TabPage构件组
        self.btnShowHide=wx.Button(self,pos=(self.Width-self.Grid*5,self.Grid),
                                 size=(3*self.Grid,3*self.Grid))
        self.btnExit=wx.Button(self,label="Exit",pos=(self.Width-self.Grid*9,self.Grid),
                             size=(3*self.Grid,3*self.Grid))
        self.tabSettings=wx.Notebook(self,pos=(self.Width-self.Grid*62,self.Grid*3),
                                   size=(60*self.Grid,20*self.Grid))
        self.pictureBoxDisplay=wx.StaticBox(self,pos=(self.Width-self.Grid*66,self.Grid*23),
                                             size=(64*self.Grid,48*self.Grid))
        self.tabSettings.SetTabSize((self.Grid,1.5*self.Grid))
        self.tabPageCamera=wx.Panel(self.tabSettings)
        self.tabPageTokens=wx.Panel(self.tabSettings)
        self.tabPageApps=wx.Panel(self.tabSettings)
        self.tabSettings.AddPage(self.tabPageCamera, "Camera")
        self.tabSettings.AddPage(self.tabPageTokens, "Tokens")
        self.tabSettings.AddPage(self.tabPageApps, "Apps")
        ##构建TabPageCamera
        self.comboBoxCameras=wx.ComboBox(self.tabPageCamera,value="Select A Camera",
                                       pos=(0,0), size=(25*self.Grid,2*self.Grid))
        self.lblCameraInfo=wx.StaticText(self.tabPageCamera,label="No Camera Selected",
                                       pos=(0,3*self.Grid),size=(25*self.Grid,2*self.Grid))
        self.buttonCameraProperties=wx.Button(self.tabPageCamera,label="Adjust Camera Properties",
                                            pos=(0,5*self.Grid),size=(23*self.Grid,2*self.Grid))
        self.labelCameraFPS=wx.StaticText(self.tabPageCamera,label="Current FPS:",
                                        pos=(0,7*self.Grid),size=(8*self.Grid,2*self.Grid))
        self.labelCameraFPSValue=wx.StaticText(self.tabPageCamera,label="0.00",
                                             pos=(8*self.Grid,7*self.Grid),
                                             size=(6*self.Grid,2*self.Grid))
        self.checkBoxCameraFPSLimit=wx.CheckBox(self.tabPageCamera,label="Limit Frames Per Second",
                                              pos=(0,9*self.Grid),
                                              size=(16*self.Grid,2*self.Grid))
        self.CameraFPSLimit=wx.TextCtrl(self.tabPageCamera,value="30",
                                      pos=(17*self.Grid,9*self.Grid),
                                      size=(6*self.Grid,2*self.Grid))
        self.lblRecord=wx.StaticText(self.tabPageCamera,label="[Recording]",
                                   pos=(41*self.Grid,1*self.Grid),
                                   size=(8*self.Grid,2*self.Grid))
        self.btnRecord=wx.Button(self.tabPageCamera,label="RECORD",
                               pos=(42*self.Grid,3*self.Grid),
                               size=(6*self.Grid,2*self.Grid))
        self.btnLoad=wx.Button(self.tabPageCamera,label="LOAD",
                             pos=(42*self.Grid,5*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        self.btnView=wx.Button(self.tabPageCamera,label="VIEW",
                             pos=(42*self.Grid,7*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        self.btnClear=wx.Button(self.tabPageCamera,label="CLEAR",
                              pos=(42*self.Grid,9*self.Grid),
                              size=(6*self.Grid,2*self.Grid))
        ##构建TabPageTokens
        self.buttonMarkerAdd=wx.Button(self.tabPageTokens,label="New Marker",
                                     pos=(0,0),size=(10*self.Grid,2*self.Grid))
        self.comboBoxMarkers=wx.ComboBox(self.tabPageTokens,value="Edit Existing Marker",
                                       pos=(11*self.Grid,0),
                                       size=(14*self.Grid,2*self.Grid))
        self.lblTotalMarker=wx.StaticText(self.tabPageTokens,label="Number of markers:",
                                        pos=(26*self.Grid,0),
                                        size=(13*self.Grid,2*self.Grid))
        self.lblMarkerCount=wx.StaticText(self.tabPageTokens,label="0",
                                        pos=(40*self.Grid,0),
                                        size=(4*self.Grid,2*self.Grid))
        self.buttonMarkerSave=wx.Button(self.tabPageTokens,label="Save M",
                                      pos=(45*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        self.buttonMarkerLoad=wx.Button(self.tabPageTokens,label="Load M",
                                      pos=(52*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        self.lblMarkerControl=wx.StaticText(self.tabPageTokens,label="No Marker Selected",
                                          pos=(0,3*self.Grid),
                                          size=(58*self.Grid,2*self.Grid))
        self.buttonMarkerRemove=wx.Button(self.tabPageTokens,label="Remove This Marker",
                                        pos=(0,5*self.Grid),
                                        size=(20*self.Grid,2*self.Grid))
        self.checkBoxMarkerHighlight=wx.CheckBox(self.tabPageTokens,label="Highlight Marker",
                                               pos=(0,7*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        self.checkBoxMarkerSmoothing=wx.CheckBox(self.tabPageTokens,label="Smooth Marker Data",
                                               pos=(0,9*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        self.labelMarkerThresh=wx.StaticText(self.tabPageTokens,label="Marker Threshold:",
                                           pos=(0,11*self.Grid),
                                            size=(15*self.Grid,2*self.Grid))
        self.MarkerThresh=wx.TextCtrl(self.tabPageTokens,value="0",
                                    pos=(15*self.Grid,11*self.Grid),
                                    size=(5*self.Grid,2*self.Grid))
        self.labelMarkerData=wx.TextCtrl(self.tabPageTokens,pos=(21*self.Grid,5*self.Grid),
                                       size=(37*self.Grid,8*self.Grid))
        self.labelMarkerData.SetEditable(False)
        ##构建TabPageApps
        self.labelDemoInstructions=wx.TextCtrl(self.tabPageApps,pos=(44*self.Grid,0),
                                             size=(16*self.Grid,16*self.Grid))
        self.labelDemoInstructions.SetEditable(False)

        #构建Label组
        self.labelM=wx.StaticText(self, label=" M", pos=(4*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelN=wx.StaticText(self, label=" N", pos=(4*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelO=wx.StaticText(self, label=" O", pos=(1*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelP=wx.StaticText(self, label=" P", pos=(1*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        self.labelM.SetBackgroundColour("ORANGE RED")
        self.labelO.SetBackgroundColour("ORANGE RED")
        self.labelN.SetBackgroundColour("RED")
        self.labelP.SetBackgroundColour("RED")
        self.labelDemoName=wx.StaticText(self, label="WUW", pos=(7*self.Grid,self.Grid),
                                       size=(4*self.Grid,2*self.Grid))
        self.lblResult=wx.StaticText(self, label="Test", pos=(12*self.Grid,self.Grid),
                                   size=(12*self.Grid,2*self.Grid))

#线程——捕获某帧图像 
class ThreadCapture(threading.Thread):
    def __init__(self, threadname, times, cam):
        threading.Thread.__init__(self, name=threadname)
        self.__cam = cam
        self.__times = times
        self.__stop = False
    def run(self):
        while not self.__stop:
            self.__cam.ImageCaptured()
            time.sleep(self.__times)
    def stop(self):
        self.__stop = True

#线程——捕获图像显示
class ThreadShow(threading.Thread):
    def __init__(self, threadname, times, panel, cam):
        threading.Thread.__init__(self, name=threadname)
        self.__times = times
        self.__panel = panel
        self.__cam = cam
        self.__stop = False
    def run(self):
        while not self.__stop:
            img = self.__cam.GetCurrentImage()
            bmp = TouchlessLib.ImageToBitmap(img)
            dc = wx.ClientDC(self.__panel.pictureBoxDisplay)
            dc.DrawBitmap(bmp,0,0)
            time.sleep(self.__times)
    def stop(self):
        self.__stop = True

def main():
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "WUW", size=(WuwPanel.Width,WuwPanel.Height))
    panel = WuwPanel(frame)
    frame.Show(True)
    cam = TouchlessLib.Camera()
    cam.Start()
    threadCapture = ThreadCapture("Capture", 0.03, cam)
    threadShow = ThreadShow("Show", 0.03, panel, cam)
    threadCapture.start()
    threadShow.start()
    app.MainLoop()
    threadCapture.stop()
    threadShow.stop()

if __name__ == "__main__":
    main()
