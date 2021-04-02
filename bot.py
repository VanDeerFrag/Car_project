import constants as cst
from vehicle import Vehicle


class Bot(Vehicle):
    def __init__(self, vehicleModel, speedX=1, speedY=2, numColumn=2, numRow=-1):
        Vehicle.__init__(self, vehicleModel, speedX, speedY, numColumn, numRow)

    def updatePosition(self):
        Vehicle.updatePosition(self)

    def changeDestination(self, numColumn):
        if self.numColumn == numColumn:
            return False
        if self.numColumn > numColumn:
            if self.numColumn > 1:
                self.numColumn -= 1
                self.gotoX = self.numColumn * cst.SCREEN_COLUMN_SIZE + cst.SCREEN_COLUMN_SIZE - self.width / 2
                self.offsetX = (self.x - self.gotoX)
        else:
            if self.numColumn < 3:
                self.numColumn += 1
                self.gotoX = self.numColumn * cst.SCREEN_COLUMN_SIZE + cst.SCREEN_COLUMN_SIZE - self.width / 2
                self.offsetX = -(self.gotoX - self.x)

        self.x = self.gotoX + self.offsetX
        return True