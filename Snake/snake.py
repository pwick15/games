 
# IMPORTS
from multiprocessing import Event
import pygame
from pygame.locals import *
import time 
import os
import random
import pygments

from sympy import BlockMatrix

# PARAMETERS
SIZE = 40
WIDTH = 1000
HEIGHT = 800

class Apple:
    def __init__(self, surface) -> None:
        self.parent_screen = surface
        self.image = pygame.image.load("./resources/apple.jpeg").convert()
        self.pos_x = random.randint(0 + 1, WIDTH/SIZE - 1) * SIZE
        self.pos_y = random.randint(0 + 1, HEIGHT/SIZE - 1) * SIZE
        
    def draw(self):
        self.parent_screen.blit(self.image,(self.pos_x, self.pos_y))
    
    def move_apple(self):
        self.pos_x = random.randint(0, WIDTH/SIZE - 1) * SIZE
        self.pos_y = random.randint(0, HEIGHT/SIZE - 1) * SIZE


class Snake:
    def __init__(self, surface, length) -> None:
        self.parent_screen = surface
        self.len = length
        self.block = pygame.image.load("./resources/block.jpeg").convert()
        self.block_x = [SIZE * (self.len - i) for i in range(self.len)]
        self.block_y = [SIZE] * self.len
        self.direction = 'right'

    def draw(self):
        self.parent_screen.fill((123,142,172)) # clears the screen
        for i in range(self.len): # for the number of blocks in the snake
            self.parent_screen.blit(self.block,(self.block_x[i],self.block_y[i]))

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.len-1, 0, -1):
            self.block_x[i] = self.block_x[i-1]
            self.block_y[i] = self.block_y[i-1]

        if self.direction == 'right': # right
            self.block_x[0] += SIZE
        if self.direction == 'left': # left
            self.block_x[0] -= SIZE
        if self.direction == 'down': # down
            self.block_y[0] += SIZE
        if self.direction == 'up': # up
            self.block_y[0] -= SIZE

        self.draw()

    def add_length(self):
        self.len += 1

        if self.direction == 'right':
            new_block_x = self.block_x[-1] - SIZE
            new_block_y = self.block_y[-1]
        if self.direction == 'left':
            new_block_x = self.block_x[-1] + SIZE
            new_block_y = self.block_y[-1]
        if self.direction == 'up':
            new_block_x = self.block_x[-1]
            new_block_y = self.block_y[-1] + SIZE
        if self.direction == 'down':
            new_block_x = self.block_x[-1] 
            new_block_y = self.block_y[-1] - SIZE

        self.block_x.append(new_block_x)
        self.block_y.append(new_block_y)


class Game:
    def __init__(self):

        #set position of window
        x = 100
        y = 45
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)        
        pygame.init() # we use init to initialise the whole pygame module

        # create the surface
        self.surface = pygame.display.set_mode(size=(WIDTH,HEIGHT)) # this is the background, the main window
        self.surface.fill((123,142,172))

        # create snake object
        self.snake = Snake(self.surface, 1)
        self.snake.draw()

        # create apple object
        self.apple = Apple(self.surface)
        self.apple.draw()

        pygame.display.flip()
        
        print('game initialised!')

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.len}", True, (255,255,255))
        self.surface.blit(score, (800,10))


    def detect_collision(self, apple_x, apple_y, snake_x, snake_y):
        if (snake_x == apple_x) and (snake_y == apple_y):
            return True
        return False
 
    def play(self):
        self.snake.walk()
        self.apple.draw()    
        self.display_score()
        pygame.display.flip()

        # snake collides with apple
        if self.detect_collision(self.apple.pos_x, self.apple.pos_y, self.snake.block_x[0], self.snake.block_y[0]):
            self.snake.add_length()
            self.apple.move_apple()

        # snake collides with itself --> end game
        for i in range(3,self.snake.len):
            if self.detect_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise "Game over"

    def show_game_over(self):
        self.surface.fill((123,142,172))
        font = pygame.font.SysFont('arial', 30)
        game_over_msg = font.render(f'Game over! You had a score of {self.snake.len}.', True, (255,255,255))
        play_again_msg = font.render(f'Press "Enter" to restart or "ESC" to close the window', True, (255,255,255))
        self.surface.blit(game_over_msg, (WIDTH / 2, HEIGHT / 2))
        self.surface.blit(play_again_msg, (WIDTH / 2, HEIGHT / 2 + 30))
        pygame.display.flip()

    def loop(self): # cycle the behaviour of the snake
        for i in range(self.snake.len):
            if self.snake.block_x[i] > WIDTH:
                self.snake.block_x[i] = 0

            if self.snake.block_x[i] < 0:
                self.snake.block_x[i] = WIDTH

            if self.snake.block_y[i] > HEIGHT-10:
                self.snake.block_y[i] = 0

            if self.snake.block_y[i] < 0:
                self.snake.block_y[i] = HEIGHT


    def run(self):
            
        # in any UI application, we use event loops which wait for user input (mouse or keyboard input)
        running = True 
        pause = False

        while running:
            for event in pygame.event.get(): # this gives all the types of events that are possible
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        self.surface.fill((123,142,172))

                        # create snake object
                        self.snake = Snake(self.surface, 1)
                        self.snake.draw()

                        pause = False



                    if event.key == K_UP and self.snake.direction != 'down':
                        self.snake.move_up()

                    if event.key == K_DOWN and self.snake.direction != 'up':
                        self.snake.move_down()

                    if event.key == K_LEFT and self.snake.direction != 'right':
                        self.snake.move_left()

                    if event.key == K_RIGHT and self.snake.direction != 'left':
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            if pause == False:
                try:
                    self.play()
                except Exception as e:
                    self.show_game_over()
                    pause = True

            self.loop()
            time.sleep(0.1)


if __name__ == '__main__':
    game = Game()
    print('game definitely initialised')
    game.run()
    

    pygame.display.flip() # whenever you update the surface, you have to either update or flip the surface


