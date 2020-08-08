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

# move based on radians and distance, indexed to 0,0
def new_pos(rads, offset):
    x = math.cos(rads) * offset
    y = math.sin(rads) * offset
    return (x, y)

# add two positions together
def add_pos(pos1,pos2):
    return tuple(map(operator.add, pos1, pos2)) 

def distance_between(pos1,pos2):
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])

def vector_full(pos1,pos2):
    return ( (pos2[0]-pos1[0])*-1 ,pos2[1]-pos1[1])


# determine which zone object is in
def in_zone(center):
    in_zone = [distance_between(center,zone.pos)<=zone.radius for zone in Zones] #eg player in green zone4 will return T,T,T,T  
    try:
        first_false_index = in_zone.index(False) #since zones are inclusive and ordered desc, the first false indicates the wides zone where player is not
    except:
        first_false_index = len(Zones)
    return Zones[first_false_index-1]

def quit_on_clicked(rect_obj):
    if click==True and rect_obj.collidepoint(mouse_pos) == True:
        result = True
    else:
        result = False
    return result
#def increment_towards(pos,vector,pos_final,delta_v_rate,speed_final):
#    dist = distance_between(pos,pos_final)
#    speed = distance_between((0,0),vector)
#    decel_dist = 
    

# empty lists
projectiles = []
blockers = []

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

class Button:
    def __init__(self,pos,color,width,height):
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height
    
    @property
    def rect(self):
        return pygame.Rect( self.pos[0], self.pos[1], self.width,self.height )

    def draw(self):
        pygame.draw.rect(screen, WHITE , self.rect )  
        
    


   
class Zone:
    def __init__(self, num, pos, radius, color):
        self.num = num
        self.pos = pos
        self.radius = radius
        self.color = color
        self.rect = (screen, self.color , self.pos, self.radius)
        
    def draw(self):
        pygame.draw.circle( *self.rect )  

class Blocker:
    def __init__(self,pos,width,height,fired_by,pos_fired_by):
        self.pos = pos
        self.width = width
        self.height = height
        self.fired_by = fired_by
        self.pos_fired_by = pos_fired_by
        self.original_width = width
        self.vector_full = vector_full(self.pos_fired_by,self.pos)
        self.rads = math.atan2(*self.vector_full)
        self.width_change = .25
        self.width_max = width*2

        self.visible = True
        
    def change_size(self,direction):
        if direction=='Down':
            self.width = max(0,self.width - self.width_change*self.original_width)
        if direction == 'Up':
            self.width = min(self.width_max,self.width + self.width_change*self.original_widths)

            
    
#    def polygon(self):
#        pos1 = add_pos(self.pos, new_pos(self.rads,self.width/2) ) #bottom left
#        pos2 = add_pos(pos1, new_pos(self.rads+math.pi,self.width)) #bottom right
#        pos3 = add_pos(pos2, new_pos(self.rads+(math.pi*1.5),self.height) ) #top right
#        pos4 = add_pos(pos3, new_pos(self.rads,self.width) ) #top left
#        return [ pos1,pos2,pos3,pos4]
    
    def rect(self):
        return pygame.Rect( self.pos[0], self.pos[1], self.width,self.height )
        
    def draw(self):
        return pygame.draw.rect(screen, RED, self.rect() )

class Projectile:
    def __init__(self,pos,pos_end,fired_by):
        self.pos = pos
        self.pos_start = pos
        self.pos_end = pos_end
        self.width = 3 #hardcode not scaled
        
        self.height = 3 #hardcode not scaled
        self.speed = 2 #hardcode not scaled
        self.fired_by = fired_by
        self.phase = 1
        self.phase_max = 30
        self.boom_radius = 10
        
        self.vector_full = vector_full(self.pos_start,self.pos_end)
#       self.vector_full =  ( (self.pos_end[0]-self.pos_start[0])*-1 ,self.pos_end[1]-self.pos_start[1]) #pygame flips y axis
        self.rads = math.atan2(*self.vector_full)+math.pi/2
        self.visible = True
        
    def vector(self):
        return new_pos(self.rads,self.speed)

    def center(self):
        return (int(self.pos[0]+self.width/2), int(self.pos[1]+self.height/2))
    
    def update_pos(self):
        self.pos = add_pos(self.pos, self.vector() )
        
    def rect(self):
        return pygame.Rect( self.pos[0], self.pos[1], self.width,self.height )
    
    def draw(self):
        if self.visible == True:
            if in_zone(self.center()).num<=4:
                return pygame.draw.rect(screen, BLACK , self.rect() )  
            else:
                self.speed = 0 
                if self.phase>=self.phase_max:
                    self.visible=False
                else:
                    pygame.draw.circle(screen, BLACK , self.center(), self.boom_radius ) 
                    self.phase += 1



class Combatant(object):
    def __init__(self, name, pos, vector,color,width,height):
        self.name = name
        self.pos = pos
        self.vector = vector
#        self.image = pygame.image.load("p3_front.png")
        
        self.color = color
        self.width = width
        self.height = height
        self.aim_pos = None
        self.friction = .995
        self.mode = 'Block'
        self.wait_attack = 30
        self.timer_attack = 0
        self.wait_block = 30
        self.timer_block = 0
        
    def center(self):
        return (self.pos[0]+self.width/2, self.pos[1]+self.height/2)
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        
    def draw(self):
        pygame.draw.rect(screen, self.color , self.rect())  
        
    def update_pos(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
    
    # this ends the game if you die
    def check_death(self):
        if in_zone(self.center()).num == 5:
            self.color = RED
            return True

class Computer(Combatant):
    def __init__(self, name, pos, vector,color,width,height):
        super().__init__( name, pos, vector,color,width,height)
    
    def update_vector(self):
        pass
#        if pressed[pygame.K_w]: w=-.02 
#        else: w=0
#        if pressed[pygame.K_a]: a=-.02
#        else: a=0
#        if pressed[pygame.K_s]: s=.02
#        else: s=0
#        if pressed[pygame.K_d]: d=.02
#        else: d=0
#        ws = w+s
#        ad = a+d
#        self.vector = (self.vector[0]+ad,self.vector[1]+ws)
        
    def aim(self,target):
        self.aim_pos = target.pos
        
    def fire(self):
        if in_zone(self.center()).num == 4:
            self.aim(Combatant1)
            projectiles.append(Projectile(self.pos,self.aim_pos,self.name))    

class Human(Combatant):
    def __init__(self, name, pos, vector,color,width,height):
        super().__init__( name, pos, vector,color,width,height)
    
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
        self.vector = ((self.vector[0]+ad)*self.friction,(self.vector[1]+ws)*self.friction)
    
    def mode_toggle(self):
        if SPACEDOWN==True:
            if self.mode == 'Block': self.mode = 'Attack'
            else: self.mode = 'Block'
    
    def aim(self):
        self.aim_pos = mouse_pos
        
    def fire(self):
        print('Firing')
        if click==True and in_zone(self.center()).num == 4:
            self.aim()
            if self.mode == 'Attack' and self.timer_attack>=self.wait_attack:
                projectiles.append(Projectile(self.center(),self.aim_pos,self.name))
                self.timer_attack = 0
            elif self.mode == 'Block' and self.timer_block>=self.wait_block:
                blockers.append(Blocker(self.aim_pos,20,1,self.name,self.center()))
                self.timer_block = 0
        self.timer_attack = self.timer_attack+1
        self.timer_block = self.timer_block+1
                
#create instance of screen
screen1 = Screen(1000,800)

# start pygame
pygame.init()

#initialize screen
screen = pygame.display.set_mode(screen1.size)

clock = pygame.time.Clock() # Used to manage how fast the screen updates
font = pygame.font.Font(None, 15)

# Loop until the user clicks the close button.
done = False



#create arena
Zone1 = Zone( 1,(screen1.center),20,RED )
Zone2 = Zone( 2,(screen1.center),60,ORANGE )
Zone3 = Zone( 3,(screen1.center),150,YELLOW )
Zone4 = Zone( 4,(screen1.center),300,GREEN )
Zone5 = Zone( 5,(screen1.center),310,WHITE )
Zone6 = Zone( 6,(screen1.center),1000,BLACK ) #created for development, to prevent a Combatant from never bing in a zone

Zones = [Zone6,Zone5,Zone4,Zone3,Zone2,Zone1]

spawn_human = (Zone4.pos[0],Zone4.pos[1]+ ((Zone3.radius+Zone4.radius)/2) )
spawn_computer = (Zone4.pos[0],Zone4.pos[1]- ((Zone3.radius+Zone4.radius)/2) )

#create Combatants
Combatant1 = Human('Read',spawn_human,(0,0),BLUE,10,10)#
Combatant2 = Computer('Computer',spawn_computer,(0,0),TEAL,10,10)#

combatants=[Combatant1,Combatant2]

#create menu
Quit_Button = Button( (10,10),WHITE,30,20 )

# make cursor visible
pygame.mouse.set_visible(True)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)


# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    SPACEDOWN=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: SPACEDOWN = True
            else: SPACEDOWN = False
    pressed = pygame.key.get_pressed()
    click = (pygame.mouse.get_pressed() == (1, 0, 0) )
    mouse_pos = pygame.mouse.get_pos()
    
    
    
    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)
    done = quit_on_clicked(Quit_Button.rect )
    
    #draw menu
    Quit_Button.draw()
    
    #draw all the zones
    [zone.draw() for zone in Zones]
    
    # draw all projectiles/blockers in current positions
    [projectile.draw() for projectile in projectiles]
    [blocker.draw() for blocker in blockers]
    
    #draw Combatant on screen
    [combatant.draw() for combatant in combatants]
    [combatant.fire() for combatant in combatants]


    # --- Update info after drawing
    #update vector using key inputs and then update position
    [combatant.update_vector() for combatant in combatants]
    [combatant.update_pos() for combatant in combatants]
    Combatant1.mode_toggle() 
    
    #end game on death
    done = any([combatant.check_death() for combatant in combatants])
    
    #check for projectile collisions
    for projectile in projectiles:
        for combatant in combatants:
            if projectile.rect().colliderect(combatant.rect())==True:
                #destroy projectile
                projectile.speed = 0
                projectile.visible=False
                
#                #relocate player to start pos in base
#                if combatant.name=='Read': #hardcode, fix this section later
#                    combatant.pos = spawn_human
#                else:
#                    combatant.pos = spawn_computer
                
        for blocker in blockers:
            if projectile.rect().colliderect(blocker.rect())==True:
                #destroy projectile
                projectile.speed = 0
                projectile.visible=False
                
                # change blocker size
                if blocker.fired_by==projectile.fired_by:
                    blocker.change_size('Up')
                else:
                    blocker.change_size('Down')
                    
    #delete invisible projectiles 
    [projectiles.remove(projectile) for projectile in projectiles if projectile.visible==False ]
    #update all projectiles positions
    [projectile.update_pos() for projectile in projectiles]
    
    
    
    
    
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