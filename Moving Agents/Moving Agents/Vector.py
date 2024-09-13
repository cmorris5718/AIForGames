import math

class Vector:   

    #constructor
    def __init__(self, xValue, yValue):
        self.x = xValue
        self.y = yValue

    #overwriting the string operator
    def __str__(self):
        return ("Vector(" + str(self.x) +","+ str(self.y)+")")

    #overwriting the + operator
    def __add__(self,other):
        sumVec = (Vector)(self.x + other.x, self.y + other.y)
        return sumVec

    #overwriting the - operator
    def __sub__(self,other):
        subVec = (Vector)(self.x - other.x, self.y - other.y)
        return subVec

    #returns the dot product of two input vectors
    def dot(vector0, vector1):
        total = vector0.x * vector1.x + vector0.y * vector1.y
        return total

    #return a vector that has been scaled by scaleValue
    def scale(self, scaleValue):
        scaledVec = (Vector)(self.x * scaleValue, self.y * scaleValue)
        return scaledVec

    #returns the length of a vector
    def length(self):
        value = math.sqrt(self.x ** 2 + self.y ** 2)
        return value
    
    #normalizes a vectorx
    def normalize(self):
        vLength = self.length()
        if vLength != 0:
            self.x /= vLength
            self.y /= vLength
        return self