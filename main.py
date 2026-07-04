import pygame
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HIGHT = 500 

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
clock = pygame.time.Clock()

test_surface = pygame.Surface((100,200))
test_surface.fill(pygame.Color('gold'))

test_rec = pygame.Rect(100,200,100,100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((10,23,250))
    screen.blit(test_surface,(193,243))
    pygame.draw.rect(screen,pygame.Color('red'),test_rec)
    pygame.display.update()
    clock.tick(60)