# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 19:03:36 2020

@author: Read

todo
- fix random blocker spawning in enemy base
- make blockers a projectile deployment and then still able to shoot at really slow rate

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
        
    

#class Zone_Slice:
#    def __init__(self,name,pos1,pos2,pos3,color):
#        self.name = name
#        self.pos1 = pos1
#        self.pos2 = pos2
#        self.pos3 = pos3
#        self.color = color
#    
#    def draw(self):
#        pygame.draw.polygon(screen,self.color,(self.pos1,self.pos2,self.pos3),0)
   
class Zone:
    def __init__(self, num, pos, radius, color):
        self.num = num
        self.pos = pos
        self.radius = radius
        self.color = color
        self.rect = (screen, self.color , self.pos, self.radius)
        
    def draw(self):
        pygame.draw.circle( *self.rect )  

#class Base(Zone):
#    def __init__(self, num, pos, radius, color, combatant):
#        super().__init__( num, pos, radius, color)
#        self.combatant = combatant
#        self.points_banked = 0
#        
#    def bank_points(self,combatant):
#        if combatant.name = combatant
#        
#    def draw(self):
#        pygame.draw.circle( *self.rect ) 
##        screen.blit(pygame.font.Font(None,16).render(str(self.points_carried), True, pygame.Color('white')) ,self.pos) #hardcoded font size


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
            self.width = min(self.width_max,self.width + self.width_change*self.original_width)
        if self.width <= self.original_width*.01:
            self.visible = False
    
    def rect(self):
        return pygame.Rect( self.pos[0]-self.width/2, self.pos[1], self.width,self.height )
        
    def draw(self):
        return pygame.draw.rect(screen, RED, self.rect() )

class Projectile:
    def __init__(self,pos,pos_end,fired_by,color,mode):
        self.pos = pos
        self.pos_start = pos
        self.pos_end = pos_end
        self.color = color
        self.mode = mode
        self.width = 5 #hardcode not scaled
        
        self.height = 5 #hardcode not scaled
        self.speed = 2 #hardcode not scaled
        self.fired_by = fired_by
        self.phase = 1
        self.phase_max = 20
        self.boom_radius = 5
        
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
    
    def destroy(self):
        self.speed = 0 
        self.visible = False
    
    def draw(self):
        if self.visible == True:
            if self.mode=='Attack':
                if in_zone(self.center()).num<=3:
                    return pygame.draw.rect(screen, self.color , self.rect() )  
                else:
                    self.speed = 0 
                    if self.phase>=self.phase_max:
                        self.visible=False
                    else:
                        pygame.draw.circle(screen, RED , self.center(), self.boom_radius ) 
                        self.phase += 1
            if self.mode == 'Block':
                if distance_between(self.pos,self.pos_end)<=self.width:
                    blockers.append(Blocker(self.pos_end,40,4,self.fired_by,self.pos_start)) #hardcode width height
                    self.destroy()
                elif in_zone(self.center()).num<=3:
                    return pygame.draw.rect(screen, self.color , self.rect() )  
                else:
                    self.speed = 0 
                    if self.phase>=self.phase_max:
                        self.visible=False
                    else:
                        pygame.draw.circle(screen, RED , self.center(), self.boom_radius ) 
                        self.phase += 1



class Combatant(object):
    def __init__(self, name, c_type, pos, vector,color,width,height):
        self.name = name
        self.c_type = c_type
        self.pos = pos
        self.vector = vector
#        self.image = pygame.image.load("p3_front.png")
        
        self.color = color
        self.width = width
        self.height = height
        self.pos_spawn = pos
        self.base_radius = 40
        self.aim_pos = None
        self.friction = .995
        self.mode = 'Attack'
        self.wait_attack = 30
        self.timer_attack = 0
        self.wait_block = 120
        self.timer_block = 0
        self.points_carried = 0
        self.points_banked = 0
        self.base_attack_box = pygame.Rect(self.pos_spawn[0]-self.base_radius*.65, self.pos_spawn[1], self.width, self.height)
        self.base_block_box = pygame.Rect(self.pos_spawn[0]+self.base_radius*.65, self.pos_spawn[1], self.width, self.height)
        
    def center(self):
        return (self.pos[0]+self.width/2, self.pos[1]+self.height/2)
        
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        
    def draw(self):
        #base
        pygame.draw.circle(screen,WHITE,self.pos_spawn,40) #harssdcode
        #sprite
        pygame.draw.rect(screen, self.color , self.rect())  
        screen.blit(pygame.font.Font(None,16).render(str(self.points_carried), True, BLACK) ,self.pos) #hardcoded font size
        screen.blit(pygame.font.Font(None,16).render(str(self.points_banked), True, BLACK) ,add_pos(self.pos_spawn,(0,self.base_radius*.65)) ) #hardcoded font size

        pygame.draw.rect(screen, BLUE , self.base_attack_box)  
        pygame.draw.rect(screen, ORANGE , self.base_block_box)  
        
    def update_pos(self):
        self.pos = tuple(map(operator.add, self.pos, self.vector))
    
    # this ends the game if you die
    def check_death(self):
        if in_zone(self.center()).num == 4:
            self.color = RED
            return True
        
    def aim(self,target):
        if self.c_type == 'Computer':
            self.aim_pos = target.pos
        else:
            self.aim_pos = mouse_pos
    
    def fire_criteria_combatants(self):
        timer=False
        if self.mode == 'Attack':
            if self.timer_attack >= self.wait_attack:
                timer=True
        if self.mode == 'Block':
            if self.timer_block >= self.wait_block:
                timer=True
        self.timer_attack = self.timer_attack+1
        self.timer_block = self.timer_block+1
        return all([in_zone(self.center()).num == 3 , timer])
    
    def fire(self):
        if self.fire_criteria_combatants() ==True and self.fire_criteria_subclass()==True:
            self.aim(Combatant1) # hardcode, build strategy later for multiple players, highest score is target of all AI
            projectiles.append(Projectile(self.center(),self.aim_pos,self.name,self.color,self.mode))
            self.timer_attack = 0
            self.timer_block = 0
            
#            if self.mode == 'Attack':
#                projectiles.append(Projectile(self.center(),self.aim_pos,self.name,self.color),self.mode)
#                self.timer_attack = 0
#            if self.mode == 'Block':
#                blockers.append(Blocker(self.aim_pos,self.base_radius,4,self.name,self.center()),self.mode)#hardcode blocker size
#                self.timer_block = 0
                
    def points_add(self):
        if in_zone(self.center()).num==1:
            self.points_carried = self.points_carried + 1
        if distance_between(self.center(), self.pos_spawn)<=self.base_radius:
            self.points_banked = self.points_banked+self.points_carried
            self.points_carried=0


class Computer(Combatant):
    def __init__(self, name, c_type, pos, vector,color,width,height):
        super().__init__( name, c_type, pos, vector,color,width,height)
    
    def update_vector(self):
        pass

    def fire_criteria_subclass(self):
        return True
        
    
class Human(Combatant):
    def __init__(self, name, c_type, pos, vector,color,width,height):
        super().__init__( name, c_type, pos, vector,color,width,height)
    
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
        if SPACEDOWN==True and self.mode == 'Block':
            self.mode = 'Attack'
        elif SPACEDOWN==True and self.mode == 'Attack':
            self.mode = 'Block'
            
            
    def fire_criteria_subclass(self):
        return all([click==True])

                
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
Zone1 = Zone( 1,(screen1.center),30,RED )
Zone2 = Zone( 2,(screen1.center),150,YELLOW )
Zone3 = Zone( 3,(screen1.center),300,GREEN )
Zone4 = Zone( 4,(screen1.center),310,WHITE )
Zone5 = Zone( 5,(screen1.center),1000,BLACK ) #created for development, to prevent a Combatant from never bing in a zone

#toggle_attack1 = Zone_Slice('Toggle_Attack',screen1.center,(screen1.width_center,screen1.height_center+1000),(screen1.width_center+30,screen1.height_center+1000),ORANGE)

Zones = [Zone5,Zone4,Zone3,Zone2,Zone1]


spawn_human = (Zone3.pos[0],int(Zone3.pos[1]+ (Zone3.radius*.90)))
spawn_computer = (Zone3.pos[0],int(Zone3.pos[1]- (Zone3.radius*.90)))


#create Combatants
Combatant1 = Human('Read','Human',spawn_human,(0,0),BLUE,14,14)#hardcode
Combatant2 = Computer('Hal','Computer',spawn_computer,(0,0),TEAL,14,14)#hardcode

combatants=[Combatant1,Combatant2]

#create menu
Quit_Button = Button( (10,10),WHITE,30,20 )

# make cursor visible
pygame.mouse.set_visible(True)
pygame.mouse.set_cursor(*pygame.cursors.broken_x)


# create needed variables
SPACEDOWN=False

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
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
    

    
    #draw Combatant on screen
    [combatant.draw() for combatant in combatants]
    
    # draw all projectiles/blockers in current positions
    [projectile.draw() for projectile in projectiles]
    [blocker.draw() for blocker in blockers]

    # --- Update info after drawing
    #update vector using key inputs and then update position  
    [combatant.fire() for combatant in combatants]
    [combatant.update_vector() for combatant in combatants]
    [combatant.update_pos() for combatant in combatants]
    [combatant.points_add() for combatant in combatants]
    Combatant1.mode_toggle() 
    
    #end game on death
    done = any([combatant.check_death() for combatant in combatants])
    
    #check for projectile collisions
    for projectile in projectiles:
        for combatant in combatants :
            if distance_between(projectile.pos,combatant.pos)<=(combatant.width+combatant.height):
                if projectile.rect().colliderect(combatant.rect())==True and projectile.fired_by!=combatant.name:
                    #destroy projectile
                    projectile.speed = 0
                    projectile.visible=False
                    
                    # remove all points and relocate player to start pos in base
                    combatant.points_carried = 0
                    combatant.pos = combatant.pos_spawn
                    
            #check if projectile collided with attack/block toggle boxes
            if distance_between(projectile.pos,combatant.pos_spawn)<=(combatant.base_radius):
                if projectile.fired_by==combatant.name:
                    if projectile.rect().colliderect(combatant.base_attack_box)==True :
                        #destroy projectile and change mode to attack
                        projectile.destroy()
                        combatant.mode = 'Attack'
                else:
                    projectile.destroy()
            if distance_between(projectile.pos,combatant.pos_spawn)<=(combatant.base_radius):
                if projectile.fired_by==combatant.name:
                    if projectile.rect().colliderect(combatant.base_block_box)==True :
                        #destroy projectile and change mode to attack
                        projectile.destroy()
                        combatant.mode = 'Block'
                else:
                    projectile.destroy()
                    

                
        for blocker in blockers:
            if distance_between(projectile.pos,blocker.pos)<=(blocker.width+blocker.height):
                if projectile.rect().colliderect(blocker.rect())==True:
                    #destroy projectile
                    projectile.speed = 0
                    projectile.visible=False
                    
                    # change blocker size
                    if blocker.fired_by==projectile.fired_by:
                        blocker.change_size('Up')
                    else:
                        blocker.change_size('Down')
                        

                    
    #delete invisible projectiles and blockers 
    [projectiles.remove(projectile) for projectile in projectiles if projectile.visible==False ]
    [blockers.remove(blocker) for blocker in blockers if blocker.visible==False ]
    
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