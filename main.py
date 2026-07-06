import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import sys
import random 
from pygame.math import Vector2 as V2

pygame.init()

#Grid & Screen Settings
cell_size = 34
cell_number =25

#Pipe Settings
pipe_speed = 2
top_bottom_pipe_space = 4
pipe_to_pipe_space = 500

#Color Settings
BG_COLOR = (10,23,250)
SNAKE_COLOR = (183,111,122)
FRUIT_COLOR = (194, 54, 22)
PIPE_COLOR = (34,139,30)

class SNAKE:
    def __init__(self):
        self.body = [V2(5,10),V2(4,10),V2(3,10)]
        self.direction = V2(1,0)
        self.last_moved_direction = V2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            snake_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,SNAKE_COLOR,snake_rect)

    def move_snake(self):
        self.last_moved_direction = self.direction
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()
    def draw_fruit(self):
        x_pos = int(self.pos.x * cell_size)
        y_pos = int(self.pos.y * cell_size) 
        fruit_rect = pygame.Rect(x_pos - 3, y_pos - 3, 40, 40)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x  = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = V2(self.x , self.y) 

class PIPES:
    def __init__(self):
        self.pipes_list=[]
        self.pipe_gap= top_bottom_pipe_space
        self.pipe_speed = pipe_speed
        self.spawn_pipe()

    def spawn_pipe(self):
        x_pixel_pos = cell_number*cell_size
        top_pipe_end = random.randint(2, cell_number-self.pipe_gap-2)
        bottom_pipe_start = top_pipe_end+self.pipe_gap
        new_pipe = {
            'x':x_pixel_pos,
            'top_end':top_pipe_end,
            'bottom_start':bottom_pipe_start,
            'spawned_next': False,
            'scored':False

        }
        self.pipes_list.append(new_pipe)
        #print(f'[Debug] new pipe at x={x_pixel_pos}, Gap:(Y1={top_pipe_end} Y2={bottom_pipe_start}) ')

    def move_pipes(self):
        for pipe in self.pipes_list:
            pipe['x']-= self.pipe_speed
        old_count = len(self.pipes_list)
        self.pipes_list= [pipe for pipe in self.pipes_list if pipe['x']>=-cell_size]

        #if len(self.pipes_list)< old_count:
            #print(f'[Debug] Out of screen pips had removed')

    def draw_pipes(self):
        if len(self.pipes_list)== 0:
            print(f'[Debug] Pipe List is empty!')

        for pipe in self.pipes_list:

            for y in range(0, pipe['top_end']):
                pipe_rect = pygame.Rect(pipe['x'], y*cell_size , cell_size , cell_size)
                pygame.draw.rect(screen,PIPE_COLOR, pipe_rect)

            for y in range(pipe['bottom_start'],cell_number):
                pipe_rect = pygame.Rect(pipe['x'], y*cell_size , cell_size , cell_size)
                pygame.draw.rect(screen, PIPE_COLOR, pipe_rect)
    def check_and_spawn(self):
        if len(self.pipes_list) > 0:
            last_pipe = self.pipes_list[-1]
            screen_width_pixels = cell_number * cell_size
        else:
            self.spawn_pipe()

        if last_pipe['x'] <= screen_width_pixels - pipe_to_pipe_space and not last_pipe['spawned_next']:
            last_pipe['spawned_next'] = True
            self.spawn_pipe()
        
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.pipes = PIPES()
        self.snake_timer = 0
        self.score =0

    def update(self):
        self.pipes.move_pipes()
        self.pipes.check_and_spawn()
        self.check_lose()

        self.snake_timer += 1
        if self.snake_timer >= 9:
            self.snake.move_snake()
            self.check_snake_fruit_collision()
            self.check_pipe_passing()
            self.snake_timer=0

    def draw_elemnts(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.pipes.draw_pipes()

    def inputs(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.snake.last_moved_direction.y != 1:
                self.snake.direction = V2(0, -1)   
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.snake.last_moved_direction.y != -1:
                self.snake.direction = V2(0, 1) 
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            if self.snake.last_moved_direction.x != 1:
                self.snake.direction = V2(-1, 0)
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            if self.snake.last_moved_direction.x != -1:
                self.snake.direction = V2(1, 0)

    def check_snake_fruit_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            fruit_points = random.randint(49,74)
            print(f'[Debug] Eat apple. added: {fruit_points}')
            self.score += fruit_points

    def check_lose(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            print(f'[Debug] snake touched itself')
            self.game_over()
        elif not 0 <= self.snake.body[0].y < cell_number:
            print(f'[Debug] snake touched itself')
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        snake_head = self.snake.body[0]
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size
            if snake_head.x == pipe_grid_x:
                if snake_head.y < pipe['top_end'] or snake_head.y >= pipe['bottom_start']:
                    print("[Debug] Snake hit a pipe!")
                    self.game_over()
    
    def game_over(self):
        print(f'Final Score {self.score}')
        pygame.quit()
        sys.exit()

    def check_if_game_close(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                print(f'Final Score {self.score}')
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                self.update()
            if event.type == pygame.KEYDOWN:
                self.inputs(event)

    def check_pipe_passing(self):
        snake_head = self.snake.body[0]
        for pipe in self.pipes.pipes_list:
            pipe_grid_x = pipe['x'] // cell_size
            
            if snake_head.x > pipe_grid_x and not pipe['scored']:
                if pipe['top_end'] <= snake_head.y < pipe['bottom_start']:
                    pipe['scored'] = True
                    pipe_points = random.randint(9,23)
                    self.score += pipe_points
                    print(f'[Debug] Snake passed throw a Pipe.. add score {pipe_points}')


screen_cords = cell_number * cell_size
screen = pygame.display.set_mode((screen_cords, screen_cords))
apple = pygame.image.load('Graphics/apple.png').convert_alpha() 
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,16)

main_game = MAIN()

while True:
    main_game.check_if_game_close()
    screen.fill(BG_COLOR)
    main_game.draw_elemnts()
    pygame.display.update()
    clock.tick(60)