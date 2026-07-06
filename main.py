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
        
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            
            if index== 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == V2(1,0):
            self.head = self.head_left
        elif head_relation == V2(-1,0):
            self.head = self.head_right
        elif head_relation == V2(0,1):
            self.head = self.head_up
        elif head_relation == V2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == V2(1,0):
            self.tail = self.tail_left
        elif tail_relation == V2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == V2(0,1):
            self.tail = self.tail_up
        elif tail_relation == V2(0,-1):
            self.tail = self.tail_down

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
        if len(self.pipes_list) == 0:
            print(f'[Debug] Pipe List is empty!')
        for pipe in self.pipes_list:
            pipe_x = pipe['x']
            for y in range(0, pipe['top_end']):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)
                if y == pipe['top_end'] - 1:
                    screen.blit(pipe_rim_top, pipe_rect)
                else:
                    screen.blit(pipe_body_sprite, pipe_rect)
            for y in range(pipe['bottom_start'], cell_number):
                pipe_rect = pygame.Rect(pipe_x, y * cell_size, cell_size, cell_size)
                
                if y == pipe['bottom_start']:
                    screen.blit(pipe_rim_bottom, pipe_rect)
                else:
                    screen.blit(pipe_body_sprite, pipe_rect)

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
pipe_raw = pygame.image.load('Graphics/pipe.png').convert_alpha()
pipe_w = pipe_raw.get_width()
pipe_h = pipe_raw.get_height()
rim_height = int(pipe_h * 0.25)
pipe_rim_raw = pipe_raw.subsurface(pygame.Rect(0, 0, pipe_w, rim_height))
pipe_rim_bottom = pygame.transform.smoothscale(pipe_rim_raw, (cell_size, cell_size))

pipe_rim_top = pygame.transform.flip(pipe_rim_bottom, False, True)

body_height = pipe_h - rim_height
pipe_body_raw = pipe_raw.subsurface(pygame.Rect(0, rim_height, pipe_w, body_height))
pipe_body_sprite = pygame.transform.smoothscale(pipe_body_raw, (cell_size, cell_size))

bg_surface_raw = pygame.image.load('Graphics/bglong.png').convert()
zoomed_width = int(screen_cords * 2)
zoomed_height = int(screen_cords * 1.5)
bg_surface = pygame.transform.smoothscale(bg_surface_raw, (zoomed_width, zoomed_height))
bg_x_pos = 0
bg_scroll_speed = 1


clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,16)

main_game = MAIN()

while True:
    main_game.check_if_game_close()

    bg_x_pos -= bg_scroll_speed
    if bg_x_pos <= -zoomed_width:
        bg_x_pos = 0
    crop_y = (screen_cords - zoomed_height) + 60

    screen.blit(bg_surface, (bg_x_pos, crop_y))
    screen.blit(bg_surface, (bg_x_pos + zoomed_width, crop_y))

    main_game.draw_elemnts()
    pygame.display.update()
    clock.tick(60)