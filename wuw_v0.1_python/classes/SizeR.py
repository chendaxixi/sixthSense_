class SizeR:
    def __init__(self, width = 0, height = 0):
        self.Width = width
        self.Height = height

    def __getitem__(self, range):
        return SizeR(self.Width, self.Height)

    def __eq__(self, other):
        return (self.Width == other.Width and self.Height == other.Height)

    def Equals(self, obj):
        if isinstance(obj, SizeR):
            return (self == obj)
        return false
