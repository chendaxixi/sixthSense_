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

class WuwPanel(wx.Panel):
    Width = Value.WuwWidth
    Height = Value.WuwHeight
    def __init__(self, parent):
        self.Grid = self.Width / 100
        wx.Panel.__init__(self, parent)

        #构建TabPage构件组
        wx.btnShowHide=wx.Button(self,pos=(self.Width-self.Grid*5,self.Grid),
                                 size=(3*self.Grid,3*self.Grid))
        wx.btnExit=wx.Button(self,label="Exit",pos=(self.Width-self.Grid*9,self.Grid),
                             size=(3*self.Grid,3*self.Grid))
        wx.tabSettings=wx.Notebook(self,pos=(self.Width-self.Grid*62,self.Grid*3),
                                   size=(60*self.Grid,20*self.Grid))
        wx.pictureBoxDisplay=wx.StaticBox(self,pos=(self.Width-self.Grid*62,self.Grid*23),
                                             size=(60*self.Grid,50*self.Grid))
        wx.tabSettings.SetTabSize((self.Grid,1.5*self.Grid))
        wx.tabPageCamera=wx.Panel(wx.tabSettings)
        wx.tabPageTokens=wx.Panel(wx.tabSettings)
        wx.tabPageApps=wx.Panel(wx.tabSettings)
        wx.tabSettings.AddPage(wx.tabPageCamera, "Camera")
        wx.tabSettings.AddPage(wx.tabPageTokens, "Tokens")
        wx.tabSettings.AddPage(wx.tabPageApps, "Apps")
        ##构建TabPageCamera
        wx.comboBoxCameras=wx.ComboBox(wx.tabPageCamera,value="Select A Camera",
                                       pos=(0,0), size=(25*self.Grid,2*self.Grid))
        wx.lblCameraInfo=wx.StaticText(wx.tabPageCamera,label="No Camera Selected",
                                       pos=(0,3*self.Grid),size=(25*self.Grid,2*self.Grid))
        wx.buttonCameraProperties=wx.Button(wx.tabPageCamera,label="Adjust Camera Properties",
                                            pos=(0,5*self.Grid),size=(23*self.Grid,2*self.Grid))
        wx.labelCameraFPS=wx.StaticText(wx.tabPageCamera,label="Current FPS:",
                                        pos=(0,7*self.Grid),size=(8*self.Grid,2*self.Grid))
        wx.labelCameraFPSValue=wx.StaticText(wx.tabPageCamera,label="0.00",
                                             pos=(8*self.Grid,7*self.Grid),
                                             size=(6*self.Grid,2*self.Grid))
        wx.checkBoxCameraFPSLimit=wx.CheckBox(wx.tabPageCamera,label="Limit Frames Per Second",
                                              pos=(0,9*self.Grid),
                                              size=(16*self.Grid,2*self.Grid))
        wx.CameraFPSLimit=wx.TextCtrl(wx.tabPageCamera,value="30",
                                      pos=(17*self.Grid,9*self.Grid),
                                      size=(6*self.Grid,2*self.Grid))
        wx.lblRecord=wx.StaticText(wx.tabPageCamera,label="[Recording]",
                                   pos=(41*self.Grid,1*self.Grid),
                                   size=(8*self.Grid,2*self.Grid))
        wx.btnRecord=wx.Button(wx.tabPageCamera,label="RECORD",
                               pos=(42*self.Grid,3*self.Grid),
                               size=(6*self.Grid,2*self.Grid))
        wx.btnLoad=wx.Button(wx.tabPageCamera,label="LOAD",
                             pos=(42*self.Grid,5*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        wx.btnView=wx.Button(wx.tabPageCamera,label="VIEW",
                             pos=(42*self.Grid,7*self.Grid),
                             size=(6*self.Grid,2*self.Grid))
        wx.btnClear=wx.Button(wx.tabPageCamera,label="CLEAR",
                              pos=(42*self.Grid,9*self.Grid),
                              size=(6*self.Grid,2*self.Grid))
        ##构建TabPageTokens
        wx.buttonMarkerAdd=wx.Button(wx.tabPageTokens,label="New Marker",
                                     pos=(0,0),size=(10*self.Grid,2*self.Grid))
        wx.comboBoxMarkers=wx.ComboBox(wx.tabPageTokens,value="Edit Existing Marker",
                                       pos=(11*self.Grid,0),
                                       size=(14*self.Grid,2*self.Grid))
        wx.lblTotalMarker=wx.StaticText(wx.tabPageTokens,label="Number of markers:",
                                        pos=(26*self.Grid,0),
                                        size=(13*self.Grid,2*self.Grid))
        wx.lblMarkerCount=wx.StaticText(wx.tabPageTokens,label="0",
                                        pos=(40*self.Grid,0),
                                        size=(4*self.Grid,2*self.Grid))
        wx.buttonMarkerSave=wx.Button(wx.tabPageTokens,label="Save M",
                                      pos=(45*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        wx.buttonMarkerLoad=wx.Button(wx.tabPageTokens,label="Load M",
                                      pos=(52*self.Grid,0),
                                      size=(6*self.Grid,2*self.Grid))
        wx.lblMarkerControl=wx.StaticText(wx.tabPageTokens,label="No Marker Selected",
                                          pos=(0,3*self.Grid),
                                          size=(58*self.Grid,2*self.Grid))
        wx.buttonMarkerRemove=wx.Button(wx.tabPageTokens,label="Remove This Marker",
                                        pos=(0,5*self.Grid),
                                        size=(20*self.Grid,2*self.Grid))
        wx.checkBoxMarkerHighlight=wx.CheckBox(wx.tabPageTokens,label="Highlight Marker",
                                               pos=(0,7*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        wx.checkBoxMarkerSmoothing=wx.CheckBox(wx.tabPageTokens,label="Smooth Marker Data",
                                               pos=(0,9*self.Grid),
                                               size=(16*self.Grid,2*self.Grid))
        wx.labelMarkerThresh=wx.StaticText(wx.tabPageTokens,label="Marker Threshold:",
                                           pos=(0,11*self.Grid),
                                            size=(15*self.Grid,2*self.Grid))
        wx.MarkerThresh=wx.TextCtrl(wx.tabPageTokens,value="0",
                                    pos=(15*self.Grid,11*self.Grid),
                                    size=(5*self.Grid,2*self.Grid))
        wx.labelMarkerData=wx.TextCtrl(wx.tabPageTokens,pos=(21*self.Grid,5*self.Grid),
                                       size=(37*self.Grid,8*self.Grid))
        wx.labelMarkerData.SetEditable(False)
        ##构建TabPageApps
        wx.labelDemoInstructions=wx.TextCtrl(wx.tabPageApps,pos=(44*self.Grid,0),
                                             size=(16*self.Grid,16*self.Grid))
        wx.labelDemoInstructions.SetEditable(False)

        #构建Label组
        wx.labelM=wx.StaticText(self, label=" M", pos=(4*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        wx.labelN=wx.StaticText(self, label=" N", pos=(4*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        wx.labelO=wx.StaticText(self, label=" O", pos=(1*self.Grid,self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        wx.labelP=wx.StaticText(self, label=" P", pos=(1*self.Grid,4*self.Grid),
                                size=(2*self.Grid,2*self.Grid))
        wx.labelM.SetBackgroundColour("ORANGE RED")
        wx.labelO.SetBackgroundColour("ORANGE RED")
        wx.labelN.SetBackgroundColour("RED")
        wx.labelP.SetBackgroundColour("RED")
        wx.labelDemoName=wx.StaticText(self, label="WUW", pos=(7*self.Grid,self.Grid),
                                       size=(4*self.Grid,2*self.Grid))
        wx.lblResult=wx.StaticText(self, label="Test", pos=(12*self.Grid,self.Grid),
                                   size=(12*self.Grid,2*self.Grid))
        

def main():
    app = wx.App(False)
    frame = wx.Frame(None, wx.ID_ANY, "WUW", size=(WuwPanel.Width,WuwPanel.Height))
    panel = WuwPanel(frame)
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()
