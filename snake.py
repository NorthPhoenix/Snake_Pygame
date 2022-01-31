import pygame
import sys
import random
from pygame.math import Vector2

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.future_direction = Vector2(0,0)
        self.new_block = False

        self.crunch_sound = pygame.mixer.Sound('Sounds/food_sound.mp3')

    def draw_snake(self):
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                pygame.draw.rect(screen, (87, 41, 75), block_rect)
            else:
                pygame.draw.rect(screen, (150, 66, 83), block_rect)

    def move_snake(self):
        if not self.future_direction == (self.direction * -1):
            self.direction = self.future_direction
            
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

    def play_food_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.future_direction = Vector2(0,0)


class Fruit:
    def __init__(self):
        self.mochi_red = pygame.transform.smoothscale(pygame.image.load('Graphics/mochi_red.png').convert_alpha(), (cell_size, cell_size))
        self.mochi_blue = pygame.transform.smoothscale(pygame.image.load('Graphics/mochi_blue.png').convert_alpha(), (cell_size, cell_size))
        self.mochi_frost = pygame.transform.smoothscale(pygame.image.load('Graphics/mochi_frost.png').convert_alpha(), (cell_size, cell_size))
        self.mochi_yellow = pygame.transform.smoothscale(pygame.image.load('Graphics/mochi_yellow.png').convert_alpha(), (cell_size, cell_size))
        self.mochi_pink = pygame.transform.smoothscale(pygame.image.load('Graphics/mochi_pink.png').convert_alpha(), (cell_size, cell_size))
        self.mochi_types = [self.mochi_red, self.mochi_blue, self.mochi_frost, self.mochi_yellow, self.mochi_pink]
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(self.mochi_img, fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.mochi_img = self.mochi_types[random.randint(0, len(self.mochi_types) - 1)]
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Grass:
    def __init__(self):
        self.grass_color1 = (207, 255, 112)
        self.grass_color2 = (184, 255, 112)

    def draw_grass(self):
        for col in range(0, cell_number):
            x_pos = col * cell_size

            for row in range(0, cell_number):
                y_pos = row * cell_size

                if (col + row) % 2 == 0:
                    block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                    pygame.draw.rect(screen, self.grass_color1, block_rect)
                else:
                    block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                    pygame.draw.rect(screen, self.grass_color2, block_rect)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.grass = Grass()
        self.font_size = 30
        self.game_font = pygame.font.Font('Fonts/Cuddle Bunny.ttf', self.font_size)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.grass.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:

            #self.snake.play_food_sound()
            valid_fruit_pos = False
            while not valid_fruit_pos:
                self.fruit.randomize()
                valid_fruit_pos = True
                for block in self.snake.body:
                    if block == self.fruit.pos:
                        valid_fruit_pos = False

            self.snake.add_block()

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < cell_number):
            self.snake.reset()
        if not (0 <= self.snake.body[0].y < cell_number):
            self.snake.reset()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.reset()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)
        
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()


cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption('Danger Noodle')
clock = pygame.time.Clock()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

main_game = Main()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            main_game.game_over()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                main_game.snake.future_direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN:
                main_game.snake.future_direction = Vector2(0,1)

            if event.key == pygame.K_RIGHT:
                main_game.snake.future_direction = Vector2(1,0)

            if event.key == pygame.K_LEFT:
                main_game.snake.future_direction = Vector2(-1,0)

        if event.type == SCREEN_UPDATE:
            main_game.update()
            
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
