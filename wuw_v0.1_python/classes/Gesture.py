#coding=utf-8

from Utils import Utils
from PointR import PointR
from SizeR import SizeR
from Value import Value

#Gesture类定义
##成员如下：
###Name:如clock03
###RawPoints:Gesture对应的完整点列
###Points:Gesture对应的抽样点列，具体的比较均通过Points


class Gesture:

    def __init__(self, name="", points=[]):
        self.Name = name
        self.RawPoints = []
        for p in points:
            self.RawPoints.append(p[:])

        if len(points) == 0:
            self.Points = []
        else:
            p = Utils.Resample(points, Value.NumResamplePoints)
        
            radians = Utils.AngleInRadians(Utils.Centroid(p), p[0], False)
            p = Utils.RotateByRadians(p, -radians)

            p = Utils.ScaleTo(p, Value.ResampleScale)

            p = Utils.TranslateCentroidTo(p, Value.ResampleOrigin)
            self.Points = p

    @property
    def Duration(self):
        if len(self.RawPoints) >= 2:
            p1 = self.RawPoints[0]
            p2 = self.RawPoints[len(self.RawPoints)-1]
            return p2.T - p1.T
        else:
            return 0

    #get the gesture name from the file name
    @staticmethod
    def ParseName(filename):
        start = filename.rfind("\\")
        end = filename.rfind(".")
        return filename[start+1:end]

    def CompareTo(self, obj):
        if isinstance(obj, Gesture):
            return cmp(self.Name, obj.Name)
        else:
            raise TypeError("object is not a Gesture")

    def __getitem__(self, range):
        return Gesture(self.Name, self.RawPoints)
        
