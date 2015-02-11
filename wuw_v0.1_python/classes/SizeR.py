class SizeR:
    def __init__(self, cx = 0, cy = 0):
        self.__cx = cx
        self.__cy = cy

    def __getitem__(self, range):
        return SizeR(self.__cx, self.__cy)

    @property
    def Width(self):
        return self.__cx
    @Width.setter
    def Width(self, value):
        self.__cx = value

    @property
    def Height(self):
        return self.__cy
    @Height.setter
    def Height(self, value):
        self.__cy = value

    def __eq__(self, other):
        return (self.Width == other.Width and self.Height == other.Height)

    def Equals(self, obj):
        if isinstance(obj, SizeR):
            return (self == obj)
        return false
