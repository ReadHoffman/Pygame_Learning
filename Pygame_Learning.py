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



#set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TEAL = (51, 204, 204)
YELLOW = (255, 255, 0)


# Formulas

# move based on radians and distance
def new_pos(rads, offset):
    x = math.cos(rads) * offset
    y = math.sin(rads) * offset
    return (x, y)

# empty lists
projectiles = []

# Create classes
class Screen:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.size=(self.width,self.height)
        self.width_center = int(self.width/2)
        self.height_center = int(self.height/2)
        self.center = (self.width_center,self.height_center)
        
    def set_mode(self):
        return pygame.display.set_mode(self.size)

        
class Zone:
    def __init__(self,pos, radius, color):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.rect = (screen, self.color , self.pos, self.radius)
        
    def draw(self):
        pygame.draw.circle( *self.rect )  

class Projectile:
    def __init__(self,pos,pos_end,fired_by):
        self.pos = pos
        self.pos_start = pos
        self.pos_end = pos_end
        self.size = (3,3) #hardcode not scaled
        self.speed = 2 #hardcode not scaled
        self.fired_by = fired_by
        
        self.vector_full = ( (self.pos_end[0]-self.pos_start[0])*-1 ,self.pos_end[1]-self.pos_start[1]) #pygame flips y axis
        self.rads = math.atan2(*self.vector_full)+math.pi/2
        self.vector = new_pos(self.rads,self.speed)

    def update_pos(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
    
    def draw(self):
        rect = ( self.pos[0], self.pos[1], self.size[0],self.size[1] )
        return pygame.draw.rect(screen, BLACK , rect )  



class Player:
    def __init__(self, name, pos, vector,color):
        self.name = name
        self.pos = pos
        self.vector = vector
#        self.image = pygame.image.load("p3_front.png")
        
        self.color = color
        self.aim_pos = None
        
    @property
    def shape(self):
        return pygame.Rect(self.pos[0], self.pos[1], 10, 10)
        
    def draw(self):
        pygame.draw.rect(screen, self.color , self.shape)  
        
    def update_pos(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
        
    def update_vector(self):
        if pressed[pygame.K_w]: w=-.02 
        else: w=0
        if pressed[pygame.K_a]: a=-.02
        else: a=0
        if pressed[pygame.K_s]: s=.02
        else: s=0
        if pressed[pygame.K_d]: d=.02
        else: d=0
        ws = w+s
        ad = a+d
        self.vector = (self.vector[0]+ad,self.vector[1]+ws)
        
    def aim(self):
        self.aim_pos = pygame.mouse.get_pos()
        
        
    def fire(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.aim()
                projectiles.append(Projectile(self.pos,self.aim_pos,self.name))
#                pygame.draw.circle(screen, WHITE , self.aim_pos, 5) 
                

#create instance of screen
screen1 = Screen(1400,1000)

# start pygame
pygame.init()

#initialize screen
screen = pygame.display.set_mode(screen1.size)

clock = pygame.time.Clock() # Used to manage how fast the screen updates
font = pygame.font.Font(None, 15)

# Loop until the user clicks the close button.
done = False

#create player
Player1 = Player('Read',(400,300),(.1,.1),BLUE)

#create arena
Zone1 = Zone( (screen1.center),20,RED )
Zone2 = Zone( (screen1.center),60,ORANGE )
Zone3 = Zone( (screen1.center),150,YELLOW )
Zone4 = Zone( (screen1.center),300,GREEN )

Zones = [Zone4,Zone3,Zone2,Zone1]


# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()
    
    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)
    
    #draw all the zones
    [x.draw() for x in Zones]
    
    #draw player on screen
    Player1.draw()
    Player1.fire()

    # --- Update info after drawing
    #update vector and then update position
    Player1.update_vector()
    Player1.update_pos()
    
    #update projectiles
    [x.update_pos() for x in projectiles]
    [x.draw() for x in projectiles]
    
    
    # Limit to 60 frames per second
    clock.tick(60)
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fps, (screen1.width-20,20))
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
#    wait = 1000
#    pygame.time.wait(int(wait))
    
 
# Close everything down
pygame.quit()