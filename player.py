import constants as cst
from vehicle import Vehicle


# Class player handling all player's related task (like moving, dying) and data (like size, health, size)
class Player(Vehicle):
    def __init__(self, vehicleModel, remainingLives=1, speedX=1, speedY=2, numColumn=2, numRow=7):
        Vehicle.__init__(self, vehicleModel, speedX, speedY, numColumn, numRow)

        self.remainingLives = remainingLives

    def changeDestination(self, keyPressed):
        if keyPressed == "Left":
            if self.numColumn > 1:
                self.numColumn -= 1
                self.gotoX = self.numColumn * cst.SCREEN_COLUMN_SIZE + cst.SCREEN_COLUMN_SIZE - self.width / 2
                self.offsetX = (self.x - self.gotoX)
        if keyPressed == "Right":
            if self.numColumn < 3:
                self.numColumn += 1
                self.gotoX = self.numColumn * cst.SCREEN_COLUMN_SIZE + cst.SCREEN_COLUMN_SIZE - self.width / 2
                self.offsetX = -(self.gotoX - self.x)

        self.x = self.gotoX + self.offsetX
