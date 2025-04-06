from math import (sin, cos)

class Triangle:
    def __init__(self, hype, angle1, side2:None|int=None,
                 side3:None|int=None, angle2:None|int=None):
        self.sideMain = hype
        self.angleMain = angle1

    def find_opp(self, printer:bool):
        oppo = sin(self.angleMain) * self.sideMain
        if printer == True:
            print(oppo)
        else:
            return(oppo)

    def find_adj(self, printer:bool):
        adj = cos(self.angleMain) * self.sideMain
        if printer == True:
            print(adj)
        else:
            return(adj)

    def find_angle(self, printer:bool):
        angl = 90 - self.angleMain
        if printer == True:
            print(angl)
        else:
            return(angl)