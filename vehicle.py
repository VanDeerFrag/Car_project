import constants as cst


class VehicleModel:

    def __init__(self):
        self.name = ""
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.image = None

    def setLocation(self, location):
        # print(xy)
        if location != "":
            location = location.split(",")
            self.x = int(location[0])
            self.y = int(location[1])

    def setSize(self, size):
        # print(size)
        if size != "":
            hw = size.split(",")
            self.width = int(hw[0])
            self.height = int(hw[1])


class Vehicle:
    def __init__(self, vehicleModel, speedX=1, speedY=1, numColumn=2, numRow=-1):
        self.name = vehicleModel.name
        self.width = vehicleModel.width
        self.height = vehicleModel.height
        self.image = vehicleModel.image
        self.x = numColumn * cst.SCREEN_COLUMN_SIZE + cst.SCREEN_COLUMN_SIZE - self.width / 2
        self.y = cst.SCREEN_ROW_SIZE * numRow - cst.SCREEN_ROW_SIZE / 2 - (
                cst.SCREEN_ROW_SIZE - vehicleModel.height) / 2
        self.speedX = speedX
        self.speedY = speedY
        self.numColumn = numColumn
        self.numRow = numRow
        self.offsetX = 0
        self.gotoX = self.x
        self.isMoving = False

    def __str__(self):
        return f"{self.name} : loc({self.x}, {self.y}), size({self.width}, {self.height})"

    def updatePosition(self):
        if self.offsetX > 0:
            self.isMoving = True
            self.offsetX -= self.speedX  # Vitesse de déplacement latérale
            if self.offsetX < 0:
                self.offsetX = 0  # Trop loin, fin du déplacement
        elif self.offsetX < 0:
            self.isMoving = True
            self.offsetX += self.speedX  # Vitesse de déplacement latérale
            if self.offsetX > 0:
                self.offsetX = 0  # Trop loin, fin du déplacement
        else:
            self.isMoving = False
        self.x = self.gotoX + self.offsetX
