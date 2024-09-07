import math

class Vector:
    #Vector class
    x = 0
    y = 0

    def __init__(self, xValue, yValue):
        self.x = xValue
        self.y = yValue

    def __str__(self):
        xStr, yStr = str((self.x)) , str((self.y))
        print(type(xStr))
        print("Vector(" + xStr + ","+ yStr + ")" )

    def __add__(self,other):
        self.x += other.x
        self.y += other.y

    def __sub__(self,other):
        self.x -= other.x
        self.y -= other.y

    def __dot__(self,other):
        total = (self.x * other.x) + (self.y + other.y)
        return total

    def __scale__(self, scaleValue):
        self.x *= scaleValue
        self.y *= scaleValue

    def __length__(self):
        return math.sqrt(math.pow(self.x,2) + math.pow(self.y,2))

    def __normalize__(self):
        if self.x != 0:
            self.x /= self.__length__
        if self.y != 0:
            self.y /= self.__length__

