from PointR import PointR
from math import sqrt

class RectangleR:
    def __init__(self, x = 0, y = 0, width = 0, height = 0, digits = 4):
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height
        self.Digits = digits

    def __getitem__(self, range):
        return RectangleR(self.X,self.Y,self.Width,self.Height,self.Digits)

    @property
    def TopLeft(self):
        return PointR(self.X,self.Y)

    @property
    def BottomRight(self):
        return PointR(self.X+self.Width, self.Y+self.Height)

    @property
    def Center(self):
        return PointR(self.X+self.Width/2.0, self.Y+self.Height/2.0)

    @property
    def MaxSide(self):
        return max(self.Width, self.Height)

    @property
    def MinSide(self):
        return min(self.Width, self.Height)

    @property
    def Diagonal(self):
        return sqrt(self.Width*self.Width+self.Height*self.Height)

    def __eq__(self, other):
        return (self.X == other.X and self.Y == other.Y and self.Width == other.Width and self.Height == other.Height)

    def Equals(self, obj):
        if isinstance(obj, RectangleR):
            return (self == obj)
        return false
