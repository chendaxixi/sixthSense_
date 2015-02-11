#coding=utf-8
#实点类，T表示绘制该店的时刻

class PointR:
    def __init__(self, x = 0, y = 0, t = 0):
        self.X = x
        self.Y = y
        self.T = t
        
    def __getitem__(self, range):
        return PointR(self.X, self.Y, self.T)

    def __eq__(self, other):
        return (self.X == other.X and self.Y == other.Y)

    def Equals(self, obj):
        if isinstance(obj, PointR):
            return (self == obj)
        return false
