from PointR import PointR
from math import sqrt

class RectangleR:
    def __init__(self, x = 0, y = 0, width = 0, height = 0, digits = 4):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__Digits = digits

    def __getitem__(self, range):
        return RectangleR(self.__x,self.__y,self.__width,self.__height,self.__Digits)

    @property
    def X(self):
        return round(self.__x, self.__Digits)
    @X.setter
    def X(self, value):
        self.__x = value

    @property
    def Y(self):
        return round(self.__y, self.__Digits)
    @Y.setter
    def Y(self, value):
        self.__y = value

    @property
    def Width(self):
        return round(self.__width, self.__Digits)
    @Width.setter
    def Width(self, value):
        self.__width = value

    @property
    def Height(self):
        return round(self.__height, self.__Digits)
    @Height.setter
    def Height(self, value):
        self.__height = value

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
        return max(self.__width, self.__height)

    @property
    def MinSide(self):
        return min(self.__width, self.__height)

    @property
    def Diagonal(self):
        return sqrt(self.Width*self.Width+self.Height*self.Height)

    def __eq__(self, other):
        return (self.X == other.X and self.Y == other.Y and self.Width == other.Width and self.Height == other.Height)

    def Equals(self, obj):
        if isinstance(obj, RectangleR):
            return (self == obj)
        return false
