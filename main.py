import pygame
import sys
import random 
from pygame.math import Vector2 as V2

class SNAKE:
    def __init__(self):
        self.body = [V2(5,10),V2(6,10),V2(7,10)]
        self.direction = V2(1,0)
    def draw_snake(self):
        for blcok in self.body:
            x_pos = int(blcok.x*cell_size)
            y_pos = int(blcok.y*cell_size)
            snake_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(183,111,122),snake_rect)
    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0]+self.direction)
        self.body = body_copy[:]
class FRUIT:
    def __init__(self):
        self.x  = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = V2(self.x , self.y) 

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y*cell_size,cell_size,cell_size)
        pygame.draw.rect(screen,(126,155,123),fruit_rect)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def update(self):
        self.snake.move_snake()
        self.check_snake_fruit_collision()
    def draw_elemnts(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def inputs(self):
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.snake.direction = V2(0,-1)
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.snake.direction = V2(0,1)
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            self.snake.direction = V2(-1,0)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            self.snake.direction = V2(1,0)
    def check_snake_fruit_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            print("Snake & Fruit collided") # Debug
pygame.init()

cell_size = 40
cell_number =20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
clock = pygame.time.Clock()



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

main_game = MAIN()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            main_game.inputs()
            
            
    screen.fill((10,23,250))
    main_game.draw_elemnts()
    pygame.display.update()
    clock.tick(60)