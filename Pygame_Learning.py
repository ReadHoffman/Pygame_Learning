# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 19:03:36 2020

@author: Read

future enhancements
-

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

def distance_between(pos1,pos2):
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])

# determine which zone object is in
def in_zone(center):
    in_zone = [distance_between(center,zone.pos)<=zone.radius for zone in Zones] #eg player in green zone4 will return T,T,T,T  
    try:
        first_false_index = in_zone.index(False) #since zones are inclusive and ordered desc, the first false indicates the wides zone where player is not
    except:
        first_false_index = len(Zones)
    return Zones[first_false_index-1]

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
    def __init__(self, num, pos, radius, color):
        self.num = num
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
        self.width = 3 #hardcode not scaled
        
        self.height = 3 #hardcode not scaled
        self.speed = 2 #hardcode not scaled
        self.fired_by = fired_by
        self.boom_radius = 10
        
        self.vector_full = ( (self.pos_end[0]-self.pos_start[0])*-1 ,self.pos_end[1]-self.pos_start[1]) #pygame flips y axis
        self.rads = math.atan2(*self.vector_full)+math.pi/2
        self.vector = new_pos(self.rads,self.speed)

    @property
    def center(self):
        return (int(self.pos[0]+self.width/2), int(self.pos[1]+self.height/2))
    
    def update_pos(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
    
    def draw(self):
        if in_zone(self.center).num<=4:
            rect = ( self.pos[0], self.pos[1], self.width,self.height )
            result = pygame.draw.rect(screen, BLACK , rect )  
        else:
            self.speed = 0 
            result = pygame.draw.circle(screen, BLACK , self.center, self.boom_radius )  
        return result
    
    



class Player:
    def __init__(self, name, pos, vector,color,width,height):
        self.name = name
        self.pos = pos
        self.vector = vector
#        self.image = pygame.image.load("p3_front.png")
        
        self.color = color
        self.width = width
        self.height = height
        self.aim_pos = None
        
    @property
    def center(self):
        return (self.pos[0]+self.width/2, self.pos[1]+self.height/2)
        
    @property
    def shape(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        
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
    
    @property
    def in_zone(self):
        in_zone = [distance_between(self.center,zone.pos)<=zone.radius for zone in Zones] #eg player in green zone4 will return T,T,T,T  
        try:
            first_false_index = in_zone.index(False) #since zones are inclusive and ordered desc, the first false indicates the wides zone where player is not
        except:
            first_false_index = len(Zones)
        return Zones[first_false_index-1] #offset by one will give current player zone
        
        
    def fire(self):
        if click==True and in_zone(self.center).num == 4:
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
Player1 = Player('Read',(400,300),(.1,.1),BLUE,10,10)

#create arena
Zone1 = Zone( 1,(screen1.center),20,RED )
Zone2 = Zone( 2,(screen1.center),60,ORANGE )
Zone3 = Zone( 3,(screen1.center),150,YELLOW )
Zone4 = Zone( 4,(screen1.center),300,GREEN )
Zone5 = Zone( 5,(screen1.center),310,WHITE )
Zone6 = Zone( 6,(screen1.center),1000,BLACK ) #created for development, to prevent a player from never bing in a zone

Zones = [Zone6,Zone5,Zone4,Zone3,Zone2,Zone1]

# make cursor visible
pygame.mouse.set_visible(True)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()
    click = (pygame.mouse.get_pressed() == (1, 0, 0) )
    
    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)
    
    #draw all the zones
    [x.draw() for x in Zones]
    
    #draw player on screen
    Player1.draw()
    Player1.fire()

    # --- Update info after drawing
    #update vector using key inputs and then update position
    Player1.update_vector()
    Player1.update_pos()
    
    #update all projectiles positions
    [x.update_pos() for x in projectiles]
    
    # draw all projectiles in current positions
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