import constants as cst
import pygame
import random
from vehicle import Vehicle, VehicleModel
from player import Player
from bot import Bot

class Vehicles:
    def __init__(self, window):
        """ Constructor. Pass in the file name of the sprite sheet. """
        self.window = window
        self.player = None
        self.vehicleModels = []
        self.vehiclesOnTheRoad = []
        self._loadModels()

    def _loadModels(self):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load('assets/Cars/cars.png')

        filepath = 'assets/Cars/cars.txt'
        # Using readlines()
        fileHandle = open(filepath, 'r')
        Lines = fileHandle.readlines()

        newVehicleModel = VehicleModel()  # Create the first vehicle model
        isFirstVehicle = True
        # Fetch all vehicle models with they params
        for line in Lines:
            if line == "":
                # end of file
                newVehicleModel.image = self.fetchImageModel(
                    newVehicleModel.x,
                    newVehicleModel.y,
                    newVehicleModel.width,
                    newVehicleModel.height
                )
                self.vehicleModels.append(newVehicleModel)
                # Add new vehicle
                newVehicleModel = VehicleModel()

                otherVehicle = Vehicle(newVehicleModel)
                otherVehicle.y

            elif not line.find(" ") >= 0:
                # New vehicule model
                line = line.replace(" ", "")  # Remove spaces
                if not isFirstVehicle:
                    # Add new vehicle model to the list
                    newVehicleModel.image = self._fetchImageModel(
                        newVehicleModel.x,
                        newVehicleModel.y,
                        newVehicleModel.width,
                        newVehicleModel.height
                    )
                    self.vehicleModels.append(newVehicleModel)

                # Prepare for the new vehicle model
                newVehicleModel = VehicleModel()
                newVehicleModel.name = line
                isFirstVehicle = False

            else:
                # Param of vehicle
                line = line.replace(" ", "")
                if line.find("xy:") >= 0:
                    newVehicleModel.setLocation(line.split(":")[1])
                elif line.find("size:") >= 0:
                    newVehicleModel.setSize(line.split(":")[1])

    def _fetchImageModel(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        # Create a new blank image
        image = pygame.Surface([width, height]).convert_alpha()
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((255,0,255)) # Transparency is Magenta
        # Return the image
        return image

    def addPlayer(self, remainingLives=3, speedX=4, speedY=1, numColumn=2):
        self.player = Player(self.vehicleModels[cst.PLAYER_INDEX],
                                remainingLives,
                                speedX,
                                speedY,
                                numColumn,
                                numRow=7)
        self.vehiclesOnTheRoad.append(self.player)

    def addBot(self):
        countVehicle = 0
        for oneVehicle in self.vehiclesOnTheRoad:
            if oneVehicle.y < 0:
                # One vehicle is already on the top row
                return
            if oneVehicle.y < (cst.SCREEN_ROW_SIZE * 4):
                # Count vehicles which are before the forth top row
                countVehicle += 1

        if countVehicle >= cst.BOTS_MAX_4ROWS:
            # Too many vehicles has already insert
            print(countVehicle)
            return

        # Don't always add a vehicle, it's random
        if random.randint(0, 1) == 0:
            if len(self.vehiclesOnTheRoad) < cst.BOTS_MAX_ALL_ROAD:
                # We can add one bot
                countOverflow = 0
                while countOverflow <= 100:
                    randomWay = random.randint(1, 3)  # Choice one way of the road
                    if not self._obstacleIsOnThisWay(randomWay):
                        self._addRandomVehiculeModel(randomWay)
                        break
                    countOverflow += 1  # security overflow

    def _obstacleIsOnThisWay(self, numWay):
        """
        Check if an obstacle is in the way
        @param numWay: numero of the way
        @return: True if an obstacle is on this way
        """
        for oneVehicle in self.vehiclesOnTheRoad:
            if type(oneVehicle) == Player:
                continue
            if oneVehicle.numColumn == numWay and oneVehicle.y <= 0:
                return True
        return False

    def _addRandomVehiculeModel(self, randomWay):
        randomModelIndex = cst.PLAYER_INDEX
        # Search random model index that isn't player
        while randomModelIndex == cst.PLAYER_INDEX:
            randomModelIndex = random.randint(0, len(self.vehicleModels) - 1)

        rndSpeed = 2
        # TODO : Rendre la vitesse des bots variables,
        #        mais pour ça il faut intégrer la détection de collision entre bots
        # rndSpeed = random.randint(1,3)
        oneBot = Bot(self.vehicleModels[randomModelIndex],
                        speedX=1,
                        speedY=rndSpeed,
                        numColumn=randomWay,
                        numRow=-1)
        self.vehiclesOnTheRoad.append(oneBot)

    def clearVehiculesOnTheRoad(self):
        self.vehiclesOnTheRoad = []

    def checkPlayerCollisions(self):
        if len(self.vehiclesOnTheRoad) == 0:
            return False

        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for oneVehicle in self.vehiclesOnTheRoad:
            if type(oneVehicle) == Player:
                continue

            vehicle_rect = pygame.Rect(oneVehicle.x, oneVehicle.y, oneVehicle.width, oneVehicle.height)
            if player_rect.colliderect(vehicle_rect):
                self.player.remainingLives -= 1
                return True
            else:
                return False

    def checkBotsCollisions(self):
        if len(self.vehiclesOnTheRoad) == 0:
            return False

        for oneVehicle in self.vehiclesOnTheRoad:
            if oneVehicle.isMoving:
                continue
            oneVehicle_rect = pygame.Rect(oneVehicle.x, oneVehicle.y+cst.SCREEN_ROW_SIZE, oneVehicle.width, oneVehicle.height+cst.SCREEN_ROW_SIZE)
            for anotherVehicle in self.vehiclesOnTheRoad:
                if oneVehicle == anotherVehicle:
                    continue

                anotherVehicle_rect = pygame.Rect(anotherVehicle.x, anotherVehicle.y, anotherVehicle.width, anotherVehicle.height)
                if oneVehicle_rect.colliderect(anotherVehicle_rect):
                    if not oneVehicle.isMoving:
                        #rndWay = random.choice(1, 3)
                        rndWay = random.choice([i for i in range(1, 3) if i != anotherVehicle.numColumn])
                        oneVehicle.changeDestination(rndWay)

    def update(self):
        # update position of player
        self.player.updatePosition()
        # update position of bots
        i = 0
        while i < len(self.vehiclesOnTheRoad):
            oneVehicle = self.vehiclesOnTheRoad[i]
            if type(oneVehicle) != Player:
                oneVehicle.y += oneVehicle.speedY
                oneVehicle.updatePosition()
                if oneVehicle.y >= cst.SCREEN_HEIGHT:
                    self.vehiclesOnTheRoad.pop(i)
                    i -= 1
                else:
                    self.window.blit(self.vehiclesOnTheRoad[i].image,
                                     (self.vehiclesOnTheRoad[i].x,
                                      self.vehiclesOnTheRoad[i].y))
            i += 1
