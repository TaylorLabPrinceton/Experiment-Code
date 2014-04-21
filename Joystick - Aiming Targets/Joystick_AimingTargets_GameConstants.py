import math
import pygame
from pygame.locals import *
import sys
import os
#Initialize Pygame
pygame.init()
#Set Mouse to not show
#pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

#Define Screen Size
if os.name == 'nt': # are we running Windows?
    screen = pygame.display.set_mode((1024,768), FULLSCREEN)
    x, y = screen.get_size()
    FULL_SCREEN = False

else:
    x,y = (1024,768)
    FULL_SCREEN = True
    #screen = pygame.display.set_mode((1024,768), FULLSCREEN)


#Define Screen Size
SCREEN_SIZE = (x,y)
SCREEN_RECT = ((0,0),(0,SCREEN_SIZE[1]),SCREEN_SIZE,(SCREEN_SIZE[1],0)) #Defines coordinates of the screen
SCREEN_CENTER = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2)
SCREEN_CENTER = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2)


#SCREEN_CENTER = (450,550)
#This will  make the game be in the center of the screen
GAME_SIZE = (x,y)
one = (SCREEN_CENTER[0] - GAME_SIZE[0]/2, SCREEN_CENTER[1] - GAME_SIZE[1]/2)
two = (SCREEN_CENTER[0] - GAME_SIZE[0]/2, SCREEN_CENTER[1] + GAME_SIZE[1]/2)
three = (SCREEN_CENTER[0] + GAME_SIZE[0]/2, SCREEN_CENTER[1] + GAME_SIZE[1]/2)
four = (SCREEN_CENTER[0] + GAME_SIZE[0]/2, SCREEN_CENTER[1] - GAME_SIZE[1]/2)
GAME_RECT = (one,two,three,four)

#If you want full screen , then set FULL_SCREEN = TRUE (make sure to get the above RES correct)

BACKGROUND_COLOR = (0,0,0)          #Background screen color
#The current screen size is 1024 x 768 pixels
#The tablet size is 9 x 12 inches, which is 304.8 x 228.6 mm
#The ratio of the screen and the tablet are the same 0.75 (or 1.333)
#So the conversion is 3.35958 pixels to mm or 0.297657 mm to pixels
PIXEL2MM = 0.297657 #I multiply all the output so that it is in mm
MM2PIXEL = 3.35958
SAMPLING_RATE = 60 #was 100
JOYSTICKXGAIN = SCREEN_SIZE[0]/SAMPLING_RATE
JOYSTICKYGAIN = SCREEN_SIZE[1]/SAMPLING_RATE

#Cursor Properties
CURSOR_COLOR = (255,255,255)        
CURSOR_HIT_COLOR = (255,0,0)        
CURSOR_MISS_COLOR = (255,0,0)        
#CURSOR_WIDTH = 4*MM2PIXEL
CURSOR_WIDTH = 6.21


CURSOR_DRIFT_TOLERANCE = 3
CURSOR_COLOR_LEFT = (255,128,0)        
CURSOR_HIT_COLOR_LEFT = (255,128,0)        
CURSOR_MISS_COLOR_LEFT = (255,128,0)        
#CURSOR_WIDTH_LEFT = 4*MM2PIXEL


#Start Position Properties
START_POSITION = SCREEN_CENTER
START_COLOR = (255,255,255)
START_HOLD_COLOR = (255,255,255)
#START_WIDTH = 6*MM2PIXEL
START_WIDTH = 8.28

START_TOLERANCE = START_WIDTH*2
HOLD_TOLERANCE_LEFT = START_TOLERANCE*2
HOLD_TOLERANCEY_LEFT = 690
HOLD_TOLERANCEX = 200
HOLD_TOLERANCEY = 710

#Target Setting
TARGET_DISTANCE = 80
#TARGET_WIDTH = 6*MM2PIXEL
TARGET_WIDTH = 12
TARGET_COLOR = (0,255,0)
TARGET_HIT = (0,255,0)
TARGET_PASS_COLOR = (255,255,255)
TARGET_MISS_SLOW = (0,0,255)
TARGET_MISS_FAST = (255,0,0)
TARGET_RING_COLOR = (0,0,255)
TARGET_RING_PASS_COLOR = (0,255,0)
TARGET_LEFT_TOLERANCE = TARGET_WIDTH*1
TARGET_RIGHT_TOLERANCE = TARGET_WIDTH*1
##PROP_COLOR_RIGHT = (0,0,255)
##PROP_COLOR_LEFT = (255,0,0)
##PROP_COLOR_OVER = (0,0,255)
##PROP_START_ANGLE = 45
##PROP_END_ANGLE = 135




TARGET_TOLERANCE = TARGET_WIDTH/3
AIMING_TARGET_ANGLES = [0,30,150,180,210,330]
AIMING_TARGET_DISTANCES = [80,92.376,92.376,80,92.376,92.376]
AIMING_TARGET_WIDTH = 8.21
AIMING_TARGET_COLOR = (0,0,255)

#Game timing info
MOVE_TIME = 0.4
MOVE_WINDOW = 0.2

HOLD_TIME = 1.00
OVER_TIME = 0.5
FEEDBACK_TIME = 1.5
BLOCKFB_TIME = 5.0
#PROP_DELAY_TIME = 0
SCORE_COLOR = (255,255,255)

#Filename directories
TRIALSET_DIR = 'TargetFiles'
DATA_DIR = 'Data'

#Variables in Trial File
TRIAL_NUM = []
TARGET_DISTANCE = []
TARGET_ANGLE = []
ROTATION = []
AIMING_TARGETS = []
TARGET_RING = []
ONLINE_FEEDBACK = []
ENDPOINT_FEEDBACK = []
BINARY_FEEDBACK = []
PAUSE = []
SHOW_SCORE = []
GOAL = []
INSTRUCTION = []
NUMERICFB = []

#Need this list for the user input window
LETTERS = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
           "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
NUMBERS = ["0","1","2","3","4","5","6","7","8","9","_"]

#COLORMAP
NUM_COLORS = 63
COLORMAP = [(0, 0, 143.4375),
            (0, 0,159.3750),
            (0, 0, 175.3125),
            (0, 0, 191.2500),
         (0,         0,  207.1875),
         (0,         0,  223.1250),
         (0,         0,  239.0625),
         (0,         0,  255.0000),
         (0,   15.9375,  255.0000),
         (0,   31.8750,  255.0000),
         (0,   47.8125,  255.0000),
         (0,   63.7500,  255.0000),
         (0,   79.6875,  255.0000),
         (0,   95.6250,  255.0000),
         (0,  111.5625,  255.0000),
         (0,  127.5000,  255.0000),
         (0,  143.4375,  255.0000),
         (0,  159.3750,  255.0000),
         (0,  175.3125,  255.0000),
         (0,  191.2500,  255.0000),
         (0,  207.1875,  255.0000),
         (0,  223.1250,  255.0000),
         (0,  239.0625,  255.0000),
         (0,  255.0000,  255.0000),
   (15.9375,  255.0000,  239.0625),
   (31.8750,  255.0000,  223.1250),
   (47.8125,  255.0000,  207.1875),
   (63.7500,  255.0000,  191.2500),
   (79.6875,  255.0000,  175.3125),
   (95.6250,  255.0000,  159.3750),
  (111.5625,  255.0000,  143.4375),
  (127.5000,  255.0000,  127.5000),
  (143.4375,  255.0000,  111.5625),
  (159.3750,  255.0000,   95.6250),
  (175.3125,  255.0000,   79.6875),
  (191.2500,  255.0000,   63.7500),
  (207.1875,  255.0000,   47.8125),
  (223.1250,  255.0000,   31.8750),
  (239.0625,  255.0000,   15.9375),
  (255.0000,  255.0000,         0),
  (255.0000,  239.0625,         0),
  (255.0000,  223.1250,         0),
  (255.0000,  207.1875,         0),
  (255.0000,  191.2500,         0),
  (255.0000,  175.3125,         0),
  (255.0000,  159.3750,         0),
  (255.0000,  143.4375,         0),
  (255.0000,  127.5000,         0),
  (255.0000,  111.5625,         0),
  (255.0000,   95.6250,         0),
  (255.0000,   79.6875,         0),
  (255.0000,   63.7500,         0),
  (255.0000,   47.8125,         0),
  (255.0000,   31.8750,         0),
  (255.0000,   15.9375,         0),
  (255.0000,         0,         0),
  (239.0625,         0,         0),
  (223.1250,         0,         0),
  (207.1875,         0,         0),
  (191.2500,         0,         0),
  (175.3125,        0,        0),
  (159.3750,         0,         0),
  (143.4375,         0,         0),
  (127.5000,         0,         0)]

##            if FIND_START:
##                self.flag = 1
##            if HOLD_START:
##                self.flag = 2
##            if SHOW_TARGET:
##                self.flag = 3
##            if MOVE_RT:
##                self.flag = 4
##            if MOVING:
##                self.flag = 5
##            if MOVE_END:
##                self.flag = 6
##            if FEEDBACK:
##                self.flag = 7
            
