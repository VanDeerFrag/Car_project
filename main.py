import time
import pygame
import constants as cst
from vehicles import Vehicles
from roads import Roads


class MyApp:

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        icon_surface = pygame.image.load('assets/icon.ico')
        self.font = pygame.font.Font('assets/LEMONMILK-Regular.otf', 20)
        pygame.display.set_icon(icon_surface)
        pygame.display.set_caption("Car Project")
        self.window = pygame.display.set_mode((cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.allVehicles = Vehicles(self.window)
        self.allVehicles.addPlayer()
        self.road = Roads(self.window, cst.SCREEN_WIDTH, cst.SCREEN_HEIGHT)
        self.game_state = "menu"
        self.soundEnabled = False
        self.init_game()
        self.display()

    def init_game(self):
        self.allVehicles.clearVehiculesOnTheRoad()
        self.init_timer = time.time()
        self.score = self.init_timer

    def keydown(self, key, lockKey):
        if self.game_state == "in_game":
            if key == pygame.K_LEFT:  # If the key down is the left arrow
                if not lockKey:  # To avoid key retention
                    self.allVehicles.player.changeDestination('Left')
                    lockKey = True
            elif key == pygame.K_RIGHT:  # If the key down is the right arrow
                if not lockKey:  # To avoid key retention
                    self.allVehicles.player.changeDestination('Right')
                    lockKey = True
        elif self.game_state == "menu" or self.game_state == "game_over":
            if key == pygame.K_RETURN:
                self.init_game()
                self.game_state = "in_game"
        return lockKey

    def display(self):
        if self.game_state == "menu":
            self.display_menu()
        elif self.game_state == "in_game":
            self.display_game()
        elif app.game_state == "game_over":
            if self.allVehicles.player.remainingLives > 0:
                self.display_end_level()
            else:
                self.display_game_over()
        # Applies new changes on the display.
        pygame.display.flip()

    def display_menu(self):
        self.window.fill(cst.COLOR_GREEN)
        cargame_txt = self.font.render("CAR GAME", True, cst.COLOR_BLACK)
        pressenter_txt = self.font.render("Press Enter to start.", True, cst.COLOR_BLACK)
        tuto_txt = self.font.render("Use Left and Right.", True, cst.COLOR_BLACK)
        self.window.blit(cargame_txt, (cst.SCREEN_WIDTH / 2 - cargame_txt.get_size()[0] / 2, 100))
        self.window.blit(tuto_txt, (cst.SCREEN_WIDTH / 2 - tuto_txt.get_size()[0] / 2, 200))
        self.window.blit(pressenter_txt, (cst.SCREEN_WIDTH / 2 - pressenter_txt.get_size()[0] / 2, 300))

    def display_game(self):
        # Color entire window with a certain color.
        self.window.fill(cst.COLOR_GREEN)
        # time.time() - init_timer
        self.road.display(4)
        self.window.blit(self.allVehicles.player.image,
                         (self.allVehicles.player.x,
                          self.allVehicles.player.y))
        self.allVehicles.update()
        pygame.draw.rect(self.window, cst.COLOR_BROWN, pygame.Rect(0, 0, cst.SCREEN_WIDTH, 100))
        pygame.draw.rect(self.window, cst.COLOR_BLACK, pygame.Rect(0, 0, cst.SCREEN_WIDTH, 100), 2)
        score_txt = self.font.render("Score :", True, cst.COLOR_BLACK)
        self.window.blit(score_txt, (100, 50 - score_txt.get_size()[1] / 2))
        self.score = int(((time.time() - self.init_timer) * 30) / 100)
        # print(score)
        value_txt = self.font.render(str(self.score) + " Km", True, cst.COLOR_BLACK)
        self.window.blit(value_txt, (200, 50 - value_txt.get_size()[1] / 2))

    def display_game_over(self):
        self.window.fill(cst.COLOR_GREEN)
        gameover_txt = self.font.render("GAME OVER", True, cst.COLOR_BLACK)
        pressenter_txt = self.font.render("Press Enter to restart.", True, cst.COLOR_BLACK)
        score_txt = self.font.render(f"Your score: {str(self.score)}", True, cst.COLOR_BLACK)
        self.window.blit(gameover_txt, (cst.SCREEN_WIDTH / 2 - gameover_txt.get_size()[0] / 2, 100))
        self.window.blit(pressenter_txt, (cst.SCREEN_WIDTH / 2 - pressenter_txt.get_size()[0] / 2, 200))
        self.window.blit(score_txt, (cst.SCREEN_WIDTH / 2 - score_txt.get_size()[0] / 2, 300))

    def display_end_level(self):
        self.window.fill(cst.COLOR_BLUE)
        gameover_txt = self.font.render("CRASH", True, cst.COLOR_BLACK)
        pressenter_txt = self.font.render("Press Enter to continue.", True, cst.COLOR_BLACK)
        remainingLives_txt = self.font.render(f"Vies restantes : {str(self.allVehicles.player.remainingLives)}", True, cst.COLOR_BLACK)
        self.window.blit(gameover_txt, (cst.SCREEN_WIDTH / 2 - gameover_txt.get_size()[0] / 2, 100))
        self.window.blit(pressenter_txt, (cst.SCREEN_WIDTH / 2 - pressenter_txt.get_size()[0] / 2, 200))
        self.window.blit(remainingLives_txt, (cst.SCREEN_WIDTH / 2 - remainingLives_txt.get_size()[0] / 2, 300))

app = MyApp()

launched = True
lockKey = False
countLock = cst.COUNT_LOCK
while launched:
    # Collect and use events for user.
    if lockKey:
        countLock -= 1
        if countLock <= 0:
            lockKey = False
            countLock = cst.COUNT_LOCK

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
        elif event.type == pygame.KEYDOWN:  # If a key is down
            lockKey = app.keydown(event.key, lockKey)

    if app.game_state == "in_game":
        app.allVehicles.addBot()

        if app.allVehicles.checkPlayerCollisions():
            app.score = int((time.time() - app.init_timer) * 30)
            app.game_state = "game_over"
            if app.soundEnabled:
                pygame.mixer.music.load("assets/game-over.wav")
                pygame.mixer.music.play(1)  # Play one time
        app.allVehicles.checkBotsCollisions()

    if app.game_state != "game_over" and pygame.mixer.music.get_busy() == False:
        if app.soundEnabled:
            pygame.mixer.music.load("assets/background_music.wav")
            pygame.mixer.music.play(-1)  # Play in loop
    app.display()

    # For fps.
    app.clock.tick(cst.FPS)

# Force exit program
pygame.display.quit()
