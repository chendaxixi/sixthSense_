#coding=utf-8

from Gesture import Gesture

#Category类定义
##成员如下:
###_name：如clock
###_prototypes：属于该Category的手势集，如clock01,clock02,clock03

class Category:

    def __init__(self, name, examples):
        self.__name = name
        self.__prototypes = []
        for p in examples:
            self.AddExample(p)

    @property
    def Name(self):
        return self.__name

    @property
    def NumExamples(self):
        return len(self.__prototypes)

    #get the category name from the gesture name
    @staticmethod
    def ParseName(s):
        i = len(s)-1
        while i >= 0:
            if not s[i].isdigit():
                category = s[0:i+1]
                break
            i -= 1
        return category

    def AddExample(self, p):
        success = True
        try:
            name = Category.ParseName(p.Name)
            if name != self.__name:
                raise ValueError("Prototype name does not equal the name of the category to which it was added.")

            counts = len(self.__prototypes)
            for i in range(counts):
                p0 = self.__prototypes[i]
                if p0.Name == p.Name:
                    raise ValueError("Prototype name was added more than once to its category.")
        except ValueError, msg:
            print msg
            success = False
        if success:
            self.__prototypes.append(p)

    def __getitem__(self, key):
        if key >= 0 and key < len(self.__prototypes):
            return self.__prototypes[key]
        else:
            return None
        

    
