from math import (sin, cos, tan,
                  acos, asin, atan)

class Triangle:
    def __init__(self, hype, angle1, side2:None|int=None,
                 side3:None|int=None, angle2:None|int=None):
        self.sideMain = hype
        self.angleMain = angle1

    def find_opp(self, print:bool):
        oppo = sin(self.angleMain) * self.sideMain
        if print == True:
            print(oppo)
        else:
            return(oppo)

    def find_adj(self, print:bool):
        adj = cos(self.angleMain) * self.sideMain
        if print == True:
            print(adj)
        else:
            return(adj)

    def find_angle(self, print:bool):
        angl = 90 - self.angleMain
        if print == True:
            print(angl)
        else:
            return(angl)