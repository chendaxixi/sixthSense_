#coding=utf-8

#NBestList类声明
##返回与所画点列相近的手势列表

class NBestList:
    class NBestResult:
        def __init__(self, name="", score=-1.0, distance=-1.0, angle=0.0):
            self.__name = name
            self.__score = score
            self.__distance = distance
            self.__angle = angle

        @property
        def Name(self):
            return self.__name

        @property
        def Score(self):
            return self.__score

        @property
        def Distance(self):
            return self.__distance

        @property
        def Angle(self):
            return self.__angle

        @property
        def IsEmpty(self):
            return self.__score == -1.0

        def CompareTo(self, obj):
            if isinstance(obj, NBestList.NBestResult):
                if self.Score < obj.Score:
                    return 1
                elif self.Score > obj.Score:
                    return -1
                else:
                    return 0
            else:
                raise TypeError("object is not a Result")

    def __init__(self):
        self.__nBestList = []

    @property
    def IsEmpty(self):
        return len(self.__nBestList) == 0

    def AddResult(self, name, score, distance, angle):
        r = NBestList.NBestResult(name, score, distance, angle)
        self.__nBestList.append(r)

    def SortDescending(self):
        self.__nBestList.sort(cmp = NBestList.NBestResult.CompareTo)

    @property
    def Name(self):
        if len(self.__nBestList) > 0:
            r = self.__nBestList[0]
            return r.Name
        return ""

    @property
    def Score(self):
        if len(self.__nBestList) > 0:
            r = self.__nBestList[0]
            return r.Score
        return -1.0

    @property
    def Distance(self):
        if len(self.__nBestList) > 0:
            r = self.__nBestList[0]
            return r.Distance
        return -1.0
    
    @property
    def Angle(self):
        if len(self.__nBestList) > 0:
            r = self.__nBestList[0]
            return r.Angle
        return 0.0

    def __getitem__(self, key):
        if key >= 0 and key < len(self.__nBestList):
            return self.__nBestList[key]
        return None

    @property
    def Names(self):
        s = []
        counts = len(self.__nBestList)
        for i in range(counts):
            s.append(self.__nBestList[i].Name)
        return s

    @property
    def NamesString(self):
        s = ""
        for r in self.__nBestList:
            s += "{0},".format(r.Name)
        ss = ""
        return ss.join(s.split(","))

    @property
    def Scores(self):
        s = []
        for r in self.__nBestList:
            s.append(r.Score)
        return s

    @property
    def ScoresString(self):
        s = ""
        for r in self.__nBestList:
            s += "%.3f," % round(r.Score, 3)
        ss = ""
        return ss.join(s.split(","))
        
        
            
