#coding=utf-8

import math
from random import random
from random import randint
from RectangleR import RectangleR
from PointR import PointR
from SizeR import SizeR
class Utils:

    ##Lengths and Rects
    
    #返回能包络points点列的最小矩形
    @staticmethod
    def FindBox(points):
        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")

        for p in points:
            if p.X < minX:
                minX = p.X
            if p.X > maxX:
                maxX = p.X
            if p.Y < minY:
                minY = p.Y
            if p.Y > maxY:
                maxY = p.Y
                
        return RectangleR(minX,minY,maxX-minX,maxY-minY)

    #返回两点距离
    @staticmethod
    def Distance(p1, p2):
        dx = p2.X - p1.X
        dy = p2.Y - p1.Y
        return math.sqrt(dx * dx + dy * dy)

    #返回点列中心
    @staticmethod
    def Centroid(points):
        xsum = 0.0
        ysum = 0.0
        for p in points:
            xsum += p.X
            ysum += p.Y
        return PointR(xsum / len(points), ysum / len(points))

    #返回点列表示的路径长度
    @staticmethod
    def PathLength(points):
        length = 0
        i = 1
        counts = len(points)
        while i < counts:
            length += Utils.Distance(points[i-1], points[i])
            i += 1
        return length
    

    ##Angles and Rotations

    #弧度转换为角度
    @staticmethod
    def RadToDeg(rad):
        return rad * 180.0 / math.pi

    #角度转换为弧度
    @staticmethod
    def DegToRad(deg):
        return deg * math.pi / 180.0

    #返回end点在以start为原点，水平向右为x轴正向，向下为y轴正向时所对的弧度
    @staticmethod
    def AngleInRadians(start, end, positiveOnly):
        radians = 0.0
        if start.X != end.X:
            radians = math.atan2(end.Y-start.Y, end.X-start.X)
        else:
            if end.Y < start.Y:
                radians = -math.pi / 2.0
            elif end.Y > start.Y:
                radians = math.pi / 2.0
        if positiveOnly and radians < 0.0:
            radians += math.pi * 2.0
        return radians

    #返回end点在以start为原点，水平向右为x轴正向，向下为y轴正向时所对的角度
    @staticmethod
    def AngleInDegrees(start, end, positiveOnly):
        radians = Utils.AngleInRadians(start, end, positiveOnly)
        return Utils.RadToDeg(radians)

    #绕中心点顺时针旋转radians弧度
    @staticmethod
    def RotateByRadians(points, radians):
        newPoints = []
        c = Utils.Centroid(points)

        cos = math.cos(radians)
        sin = math.sin(radians)

        cx = c.X
        cy = c.Y

        counts = len(points)
        for i in range(counts):
            p = points[i]
            dx = p.X - cx
            dy = p.Y - cy
            q = PointR()
            q.X = dx * cos - dy * sin + cx
            q.Y = dx * sin + dy * cos + cy
            newPoints.append(q)
        return newPoints

    #绕中心点顺时针旋转degrees角度
    @staticmethod
    def RotateByDegrees(points, degrees):
        radians = Utils.DegToRad(degrees)
        return RotateByRadians(points, radians)

    #返回p点绕c点顺时针旋转radians弧度后结果
    @staticmethod
    def RotatePoint(p, c, radians):
        q = PointR()
        q.X = (p.X - c.X) * math.cos(radians) - (p.Y - c.Y) * math.sin(radians) + c.X
        q.Y = (p.X - c.X) * math.sin(radians) + (p.Y - c.Y) * math.cos(radians) + c.Y
        return q

    ##Translations

    #转换坐标，以toPt为左上角
    @staticmethod
    def TranslateBBoxTo(points, toPt):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += toPt.X - r.X
            p.Y += toPt.Y - r.Y
            newPoints.append(p)
        return newPoints

    #转换坐标，以toPt为中心点
    @staticmethod
    def TranslateCentroidTo(points, toPt):
        newPoints = []
        centroid = Utils.Centroid(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += toPt.X - centroid.X
            p.Y += toPt.Y - centroid.Y
            newPoints.append(p)
        return newPoints

    #平移
    @staticmethod
    def TranslateBy(points, sz):
        newPoints = []
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X += sz.Width
            p.Y += sz.Height
            newPoints.append(p)
        return newPoints

    ##Scaling

    #根据原点进行放缩，使矩形变成sz大小
    @staticmethod
    def ScaleTo(points, sz):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            if r.Width != 0.0:
                p.X *= (sz.Width / r.Width)
            if r.Height != 0.0:
                p.Y *= (sz.Height / r.Height)
            newPoints.append(p)
        return newPoints

    #根据原点进行放缩，使矩形放大sz倍
    @staticmethod
    def ScaleBy(points, sz):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= sz.Width
            p.Y *= sz.Height
            newPoints.append(p)
        return newPoints

    @staticmethod
    def ScaleToMax(points, box):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= (box.MaxSide / r.MaxSide)
            p.Y *= (box.MaxSide / r.MaxSide)
            newPoints.append(p)
        return newPoints

    @staticmethod
    def ScaleToMin(points, box):
        newPoints = []
        r = Utils.FindBox(points)
        counts = len(points)
        for i in range(counts):
            p = points[i][:]
            p.X *= (box.MinSide / r.MinSide)
            p.Y *= (box.MinSide / r.MinSide)
            newPoints.append(p)
        return newPoints

    ##Path Sampling and Distance

    #从点列中平均得选出n个
    @staticmethod
    def Resample(points, n):
        I = 1.0 * Utils.PathLength(points) / (n-1)
        D = 0.0
        srcPts = []
        for p in points:
            srcPts.append(p[:])
        dstPts = []
        dstPts.append(srcPts[0][:])
        counts = len(srcPts)
        i = 1
        while i < counts:
            pt1 = srcPts[i-1]
            pt2 = srcPts[i]

            d = Utils.Distance(pt1, pt2)
            if (D+d) >= I:
                qx = pt1.X + ((I - D) / d) * (pt2.X - pt1.X)
                qy = pt1.Y + ((I - D) / d) * (pt2.Y - pt1.Y)
                q = PointR(qx, qy)
                dstPts.append(q)
                srcPts.insert(i, q[:])
                counts += 1
                D = 0.0
            else:
                D += d
            i += 1
        if len(dstPts) == n-1:
            dstPts.append(srcPts[len(srcPts) -1][:])
        return dstPts

    #计算两条路径的平均距离
    @staticmethod
    def PathDistance(path1, path2):
        distance = 0
        counts = len(path1)
        for i in range(counts):
            distance += Utils.Distance(path1[i], path2[i])
        return distance / counts

    ##Random Numbers

    #产生num个不重复的low-high间的随机数
    @staticmethod
    def Random(low, high, num):
        array = []
        n = high - low + 1
        if num > n:
            return array
        if n * 1.0 / num < 1.0 / 3.0:
            for i in range(num):
                array.append(i)
            i = 0
            while i < num:
                array[i] = randint(low, high)
                for j in range(i):
                    if array[i] == array[j]:
                        i -= 1
                        break
            return array
        tmp = []
        for i in range(n):
            tmp.append(i + low)
        for i in range(num):
            t = randint(0, n-i-1)
            array.append(tmp[t])
            tmp[t] = tmp[n-i-1]
        return array
    
    
