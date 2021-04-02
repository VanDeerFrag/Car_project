import pygame

theClock = pygame.time.Clock()

background = pygame.image.load('/home/sacha/Bureau/Docs/Wallpaper/9ZWANP.jpg')

background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)
x = 0
y = 0
w,h = background_size
running = True

while running:
    screen.blit(background,background_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if(y > h):
        y = 0
    else:
        y += 5
    screen.blit(background,(x,y))
    pygame.display.flip()
    pygame.display.update()
    theClock.tick(10)