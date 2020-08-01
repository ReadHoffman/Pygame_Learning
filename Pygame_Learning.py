# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 19:03:36 2020

@author: Read
"""


import pygame
from pygame.locals import KEYDOWN
import math
import random
import time
import operator

#set screen dimensions
screen_size = [800,600]
#background = pygame.Surface(screen.get_size())

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create classes
class Player:
    def __init__(self, name, pos, vector):
        self.name = name
        self.pos = pos
        self.vector = vector
#        self.image = pygame.image.load("p3_front.png")
        self.rect = pygame.Rect(  self.pos[0], self.pos[1], 10, 10 ) 
        self.color = WHITE
        
    def update(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
        
    

# start pygame
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock() # Used to manage how fast the screen updates
font = pygame.font.Font(None, 15)

# Loop until the user clicks the close button.
done = False

Player1 = Player('Read',(400,300),(.1,.1))

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)
    
    pygame.draw.rect(screen, Player1.color, Player1.rect, 1)
    Player1.update()
    
    
    # Limit to 60 frames per second
    clock.tick(60)
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fps, (screen_size[0]-50,50))
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
#    wait = 1000
#    pygame.time.wait(int(wait))
    
 
# Close everything down
pygame.quit()