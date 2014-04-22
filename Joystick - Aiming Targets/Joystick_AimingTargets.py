#!/usr/bin/python


#Load modules, these are the python modules that we need to run the game
import pygame, sys, os, math, time, datetime
from pygame.locals import *
from Joystick_AimingTargets_GameConstants import *
from Joystick_AimingTargets_GameWindow_Screen import *


#=========================================================================
#These classes define the cursor, start, and target objects
#Right hand cursor 
class cursor_info:
    def __init__(self):
        #Define Cursor
        self.width = int(CURSOR_WIDTH)
        self.color = CURSOR_COLOR
        self.hitcolor = CURSOR_HIT_COLOR
        self.misscolor = CURSOR_MISS_COLOR
        self.x = SCREEN_CENTER[0]
        self.y = SCREEN_CENTER[1]
        self.position = (self.x,self.y)
        self.angle = 0
        self.r = 0
        self.xf = 0
        self.yf = 0
        self.position_final = (0,0)
        self.xfb = 0
        self.yfb = 0
        self.position_fb = (0,0)


#Right hand
class hand_info:
    def __init__(self):
        #Define Hand
        self.x = 0
        self.y = 0
        self.position = (0,0)
        self.angle = 0
        self.r = 0
        self.xf = 0
        self.yf = 0
        self.position_final = (0,0)
      
class start_info:
    def __init__(self):
        #Create Start Position
        self.x = SCREEN_CENTER[0]
        self.y = SCREEN_CENTER[1]
        self.color = START_COLOR
        self.hold_color = START_HOLD_COLOR
        self.position =( int(START_POSITION[0]),int(START_POSITION[1]))
        self.width = int(START_WIDTH)
        self.center = SCREEN_CENTER
        self.tolerance = START_TOLERANCE

class target_info:
     def __init__(self):
        #Create Targets
        self.x = 0
        self.y = 0
        self.position = (0,0)
        self.distance = 0
        self.angle = 0
        self.hit = 0
        self.ring_color = TARGET_RING_COLOR
        self.ring_pass_color = TARGET_RING_PASS_COLOR
        self.color = TARGET_COLOR
        self.width = int(TARGET_WIDTH)
        self.hitcolor = TARGET_HIT
        self.missslow_color = TARGET_MISS_SLOW
        self.missfast_color = TARGET_MISS_FAST
        self.tolerance = TARGET_TOLERANCE
        self.line_startx = 0
        self.line_endx = 0
        self.line_starty = SCREEN_RECT[0][1]
        self.line_endy = SCREEN_RECT[3][1]

class aiming_target_info():
    def __init__(self):
        #Creat Aiming Targets
        self.x = 0
        self.y = 0
        self.num = 0
        self.distances = AIMING_TARGET_DISTANCES
        self.color = AIMING_TARGET_COLOR
        self.width = int(AIMING_TARGET_WIDTH)
        self.position = (0,0)
        self.targets = 0
        self.center = 90
        self.start = -180
        self.end = 180
        

#====This is the main game class, where all the game pertinent stuff is initialized and the trial loop is in here====
class Game:
    def __init__(self):
        #initialize the pygame module
        pygame.init()
	#Set joystick up
	pygame.joystick.init()
	joystick_count = pygame.joystick.get_count()
	if joystick_count > 1:
            print "Error more than one joystick detected"
            print joystick_count
        else:
            joystick = pygame.joystick.Joystick(0) #use the first joystick
            joystick.init()
            joystick_name = joystick.get_name()
            joystick_numaxes = joystick.get_numaxes()
            print "Joystick Name"
            print joystick_name
            print "Joystick Axes"
            print joystick_numaxes
        #Set Mouse up
        pygame.mouse.set_visible(False)
        
        #Create Window
        if FULL_SCREEN:
            self.screen = pygame.display.set_mode((0,0), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(SCREEN_SIZE, NOFRAME) #This looks like full
            #self.screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE) #This looks like full
            
        self.draw_rectlist = []
        self.draw_noerase_rectlist = []
        self.erase_rectlist = []
        ScreenUpdate(self)  #updates the screen

        #This calls the function that prompts the user for the filename and trialset filename
        GameInputWindow(self,DATA_DIR,TRIALSET_DIR)   #returns trialset_fname and subject_fname
        
        #Load trialset and test how many trials
        trialset_file = open(TRIALSET_DIR+'/'+self.trialset_fname)
        trialset = trialset_file.readlines()
        trialset_file.close()
        self.trialset_len = len(trialset)-1
        self.max_score = self.trialset_len

        trialset_variables = trialset[0].replace('"','').split()
        for trial in trialset[1:]:
            values = trial.split()
            TRIAL_NUM.append(float(values[0]))
            TARGET_DISTANCE.append(float(values[1]))
            TARGET_ANGLE.append(float(values[2]))
            ROTATION.append(float(values[3]))
            AIMING_TARGETS.append(float(values[4]))
            TARGET_RING.append(float(values[5]))
            ONLINE_FEEDBACK.append(int(values[6]))
            ENDPOINT_FEEDBACK.append(float(values[7]))
            BINARY_FEEDBACK.append(float(values[8]))
            PAUSE.append(float(values[9]))
            SHOW_SCORE.append(float(values[10]))
            GOAL.append(float(values[11]))
            INSTRUCTION.append(float(values[12]))
            NUMERICFB.append (float(values[13]))

        #Abstracted file
        history = {'trial_num':[],'target_distance':[],'target_angle':[],'rotation':[], 'aiming_targets':[],'target_ring':[],
                   'online_feedback':[],'endpoint_feedback':[],'binary_feedback':[],'goal':[],'instruction':[],'numericfb':[],'currentpoints':[],'totalpoints':[],'currentscore':[],'totalscore':[],'pause':[], 'show_score':[],'cursor_angle':[],'cursor_r':[],'hand_angle':[],'hand_r':[],
                   'abs_start_x':[],'abs_start_y':[],'abs_target_x':[],'abs_target_y':[],'abs_cursor_x':[],'abs_cursor_y':[],
                   'abs_hand_x':[],'abs_hand_y':[],'start_x':[],'start_y':[],'target_x':[],'target_y':[],
                   'cursor_x':[],'cursor_y':[],'hand_x':[],'hand_y':[],'hit':[],
                   'trial_time':[],'reaction_time':[],'movement_time':[],'fb_time':[],'find_time':[],'hold_time':[],
                   'abs_start_time':[],'abs_target_time':[],'pixel2mm':[],'joystick_axis0':[],'joystick_axis1':[],'joystick_axis2':[],'joystick_axis3':[]}
            
        #Raw cursor position
        move_data = {'trial_num':[],'flag':[],'t':[],'dt':[],'trial_time':[],'rotation':[],'start_x':[],'start_y':[],
                     'cursor_x':[],'cursor_y':[],'hand_x':[],'hand_y':[],'joystick_axis0':[],'joystick_axis1':[],'joystick_axis2':[],'joystick_axis3':[]}

        #Setup stuff
        cursor = cursor_info()
        hand = hand_info()
        target = target_info()
        aiming = aiming_target_info()
        start = start_info()
	joystick_axis0 = 0
	joystick_axis1 = 0
	joystick_axis2 = 0 #only using first two axes
	joystick_axis3 = 0 #only using first two axes
        self.trial_num = 0
        self.flag = 1
        self.total_score = 0
        self.current_score  = 0
        self.total_points = 0
        self.current_points  = 0
        self.possible_points = 0
        self.total_trials = 0
        self.score_color = SCORE_COLOR
        self.score_position = (SCREEN_CENTER[0]-SCREEN_CENTER[0]/1.5,SCREEN_CENTER[1])
        self.points_font_size = POINTS_FONT_SIZE
        self.points_position = POINTS_POSITION
        self.points_color = POINTS_COLOR
        self.cue_position = (SCREEN_CENTER[0]-110,SCREEN_CENTER[1]-150)
        self.exit = False
        self.font_size = FONT_SIZE
        errorangle = 0
        
        #Timing
        clock = pygame.time.Clock()
        if os.name == 'nt': # are we running Windows?
            self.previous_time = time.clock()
        else:
            self.previous_time = time.time()
        self.game_time = 0
        self.trial_time = 0
        self.hold_time = 0
        self.find_time = 0
        self.rt = 0
        self.move_time = 0
        self.fb_time = 0
        self.trial_start_time = 0
        self.reached_target_time = 0
        self.save_trial_time = 0


        #Trial Flags
        FIND_START = True           #Flag 1
        HOLD_START = False          #Flag 2
        SHOW_TARGET = False         #Flag 3
        MOVING = False              #Flag 4
        FEEDBACK = False            #Flag 5
        NEXT_TRIAL = False #Flag 6
        TARGET_FILL = 1
        CURSOR_VISIBLE = False
        CURSOR_ZOOM = True
        CURSOR_CONTROL = True
        HIT = False
        CURSOR_ENDPOINT_FB = False
        
        
        #Game Pertinent Functions----------------------------------------------------------------------
        def CurrentEvent(self):
            if FIND_START:
                self.flag = 1
            if HOLD_START:
                self.flag = 2
            if SHOW_TARGET:
                self.flag = 3
            if MOVING:
                self.flag = 4
            if FEEDBACK:
                self.flag = 5
            if NEXT_TRIAL:
                self.flag = 6

        #Computes the cursor velocity
        def CursorVelocity(x1,y1,x2,y2,dt):
            vx = (x2 - x1)/dt
            vy = (y2 - y1)/dt
            speed = math.sqrt(vx*vx + vy*vy)
            direction = math.atan2(vy,vx)
            return (vx,vy,speed,direction)
        
        def TargetLocation(target,start):
            target.x = start.x + target.distance*math.cos(target.angle*math.pi/180)
            target.y = start.y - target.distance*math.sin(target.angle*math.pi/180)
            target.position = (int(target.x),int(target.y))

        def AimingTargetLocation(aiming,target,start):
            #Plot aiming targets
            if aiming.target > 0:
                #Compute how many targets
                aiming_increment = aiming.center/aiming.target
                angle = aiming.start
                color_increment = math.floor(len(COLORMAP)/(aiming.target*2))
                start_count = 0
                end_count = NUM_COLORS
                for i in range(int(aiming.target*2)):
                    #print(angle,math.fabs(angle))
                    if math.fabs(angle) <= 90:
                        #Get colors
                        color_start = COLORMAP[start_count]
                        color_end = COLORMAP[end_count]
                        #Compute x,y position for aiming target
                        x = start.x + target.distance*math.cos((target.angle+angle)*math.pi/180)
                        y = start.y - target.distance*math.sin((target.angle+angle)*math.pi/180)
                        aiming.position = (int(x),int(y))
                        #plot current aiming target
                        self.draw_noerase_rectlist.append(pygame.draw.circle(self.screen, color_start, aiming.position, aiming.width*2, 1))
                        start_count = int(start_count + color_increment)
                        end_count = int(end_count - color_increment)

                       #Compute x,y position for opposite aiming target
                        x = start.x + target.distance*math.cos((target.angle-angle)*math.pi/180)
                        y = start.y - target.distance*math.sin((target.angle-angle)*math.pi/180)
                        aiming.position = (int(x),int(y))
                        self.draw_noerase_rectlist.append(pygame.draw.circle(self.screen, color_end, aiming.position, aiming.width*2, 1))
                        start_count = int(start_count + color_increment)
                        end_count = int(end_count - color_increment)

                    elif math.fabs(angle) > 90:
                        #Compute x,y position for aiming target
                        x = start.x + target.distance*math.cos((target.angle+angle)*math.pi/180)
                        y = start.y - target.distance*math.sin((target.angle+angle)*math.pi/180)
                        aiming.position = (int(x),int(y))
                        #plot current aiming target
                        self.draw_noerase_rectlist.append(pygame.draw.circle(self.screen, (128,128,128), aiming.position, aiming.width, 0))
                        #Compute x,y position for opposite aiming target
                        x = start.x + target.distance*math.cos((target.angle-angle)*math.pi/180)
                        y = start.y - target.distance*math.sin((target.angle-angle)*math.pi/180)
                        aiming.position = (int(x),int(y))
                        #plot current aiming target
                        self.draw_noerase_rectlist.append(pygame.draw.circle(self.screen, (128,128,128), aiming.position, aiming.width, 0))                    
                    #compute next target and colors
                    angle = angle + aiming_increment

                ScreenUpdateNoErase(self)
                    
        def StartDist(cursor,hand,start):
            x = cursor.x - start.x
            y = start.y - cursor.y  
            r = math.sqrt(x*x + y*y)
            angle = math.atan2(y,x)
            cursor.r = r
            cursor.angle = angle
            x = hand.x - start.x
            y = start.y - hand.y
            r = math.sqrt(x*x + y*y)
            hand.angle = math.atan2(y,x)
            hand.r = r
            
        def FieldRotation(x,y,angle,start,target): #THIS IS THE NORMAL ENVIRONMENTAL ROTATION
            if angle != 0:
                #Left handed coordinate system remember
                angle = angle*math.pi/180
                xc = x - start.x
                yc = y - start.y
                phi = math.atan2(yc,xc)
                xr = xc*math.cos(angle) + yc*math.sin(angle)
                yr = - xc*math.sin(angle) + yc*math.cos(angle)
                x = xr + start.x
                y = yr + start.y
            else:
                x = x
                y = y
            return (x,y)
        
        def RotFBloc(cursor,start,target):#This function sets the feedback location for a rotation
            if self.online_feedback == 0: #Endpoint feedback 
                x = cursor.x - start.x
                y = start.y - cursor.y
                #set r to be target distance
                r = target.distance
                angle = math.atan2(y,x)
                cursor.xfb = r*math.cos(angle) + start.x
                cursor.yfb = -r*math.sin(angle) + start.y
                cursor.position_fb = (int(cursor.xfb),int(cursor.yfb))
            elif self.online_feedback == 1:  #Online feedback 
                x = cursor.x - start.x
                y = start.y - cursor.y
                #set r to be target distance
                r = target.distance
                angle = math.atan2(y,x)
                cursor.xfb = r*math.cos(angle) + start.x
                cursor.yfb = -r*math.sin(angle) + start.y
                cursor.position_fb = (int(cursor.xfb),int(cursor.yfb))
            
         #This will display the score following the end of the block
        def GameScore(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, self.font_size)
            text = font.render("Total Score is "+str(int(self.total_points))+" out of "
                               +str(int(self.possible_points))+". You collected "+
                               str(int(100*self.total_points/self.possible_points))+
                               "% of points available.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            ScreenUpdate(self)
            #I only use this here because I dont care about timing at the end of the game
            pygame.time.delay(int(blockfb_time*1000))
            
        def pausescreen(self):
           	while self.pause_chk < 1:
           		for event in pygame.event.get():
                #Check for space key while pausing
           			if event.type == KEYDOWN:
           				if event.key == K_SPACE:
           					self.pause_chk = 1

         #This will display the score following the end of the block
        def GoalInstPause(self,blockfb_time):
           	self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
           	font = pygame.font.Font(None, 36)
           	text = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
           	self.draw_rectlist.append(self.screen.blit(text, self.score_position))
           	text2 = font.render("green target.", 1, self.score_color)
           	self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0]+130,self.score_position[1]+25)))
           	ScreenUpdate(self)
           	pausescreen(self)
            
        def GoalInstReminder(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            text2 = font.render("green target.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0]+130,self.score_position[1]+25)))
            text4 = font.render("Total Score is "+str(int(self.total_score))+" out of "
                               +str(int(self.total_trials))+". You collected "+
                               str(int(100*self.total_score/self.total_trials))+
                               "% of points available.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text4, (self.score_position[0],self.score_position[1]-100)))
            ScreenUpdate(self)
            pygame.time.delay(int((blockfb_time+2)*1000))
            self.pause_chk = 1
        
        def GoalReminderScore(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            text = font.render("green target.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+130,self.score_position[1]+25)))
            text4 = font.render("Total Score is "+str(int(self.total_score))+" out of "
                               +str(int(self.total_trials))+". You collected "+
                               str(int(100*self.total_score/self.total_trials))+
                               "% of points available.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text4, (self.score_position[0],self.score_position[1]-100)))
            ScreenUpdate(self)
            pygame.time.delay(int(blockfb_time*1000))
            self.pause_chk = 1
        
        def GoalReminderFirstTrial(self):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            text = font.render("green target.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+130,self.score_position[1]+25)))
            ScreenUpdate(self)
            pausescreen(self)
            
        def GoalReminder(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            text = font.render("green target.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+130,self.score_position[1]+25)))
            ScreenUpdate(self)
            pygame.time.delay(int(blockfb_time*1000))
            self.pause_chk = 1
            
        def BreakScreen(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Please take a short 30 second break", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, self.score_position))
            ScreenUpdate(self)
            pygame.time.delay(int(30000))#30 second break
            PostBreakScreen(self,blockfb_time)
            
        def PostBreakScreen(self,blockfb_time):       
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Get ready! The experiment will now continue.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0],self.score_position[1]-100)))
            text2 = font.render("Reminder: The goal of the task is to get your red cursor on the", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, self.score_position))
            text3 = font.render("green target.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text3, (self.score_position[0]+130,self.score_position[1]+25)))
            ScreenUpdate(self)
            pausescreen(self)
        

        def WashReminderPause(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Aim directly for the green target", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+160,self.score_position[1])))
            text2 = font.render("You will not see feedback of your reaches for some of the movements", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0],self.score_position[1]+50)))
            ScreenUpdate(self)
            pausescreen(self)
            
        def WashReminder(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Aim directly for the green target", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+160,self.score_position[1])))
            text2 = font.render("You will not see feedback of your reaches for some of the movements", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0]-50,self.score_position[1]+50)))
            ScreenUpdate(self)
            pygame.time.delay(int(blockfb_time*1000))
            self.pause_chk = 1
            
            
        def WashReminderScore(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Aim directly for the green target", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+160,self.score_position[1])))
            text2 = font.render("You will not see feedback of your reaches for some of the movements", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0],self.score_position[1]+50)))
            text4 = font.render("Total Score is "+str(int(self.total_score))+" out of "
                               +str(int(self.total_trials))+". You collected "+
                               str(int(100*self.total_score/self.total_trials))+
                               "% of points available.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text4, (self.score_position[0],self.score_position[1]-100)))
            ScreenUpdate(self)
            pygame.time.delay(int((blockfb_time+2)*1000))
            self.pause_chk = 1
            
        def WashReminderScorePause(self,blockfb_time):
            self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            font = pygame.font.Font(None, 36)
            text = font.render("Aim directly for the green target", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text, (self.score_position[0]+160,self.score_position[1])))
            text2 = font.render("You will not see feedback of your reaches for some of the movements", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text2, (self.score_position[0],self.score_position[1]+50)))
            text4 = font.render("Total Score is "+str(int(self.total_score))+" out of "
                               +str(int(self.total_trials))+". You collected "+
                               str(int(100*self.total_score/self.total_trials))+
                               "% of points available.", 1, self.score_color)
            self.draw_rectlist.append(self.screen.blit(text4, (self.score_position[0],self.score_position[1]-100)))
            ScreenUpdate(self)
            pausescreen(self)


            
        def GameHistoryUpdate(history,cursor,target,start,move_data,PIXEL2MM):
            history_keys = ['trial_num','target_distance','target_angle','rotation', 'aiming_targets','target_ring',
                            'online_feedback','endpoint_feedback','binary_feedback','goal','instruction','numericfb','currentpoints','totalpoints','currentscore','totalscore','pause','show_score','cursor_angle','cursor_r','hand_angle','hand_r',
                            'abs_start_x','abs_start_y','abs_target_x','abs_target_y','abs_cursor_x','abs_cursor_y',
                            'abs_hand_x','abs_hand_y','start_x','start_y','target_x','target_y',
                            'cursor_x','cursor_y','hand_x','hand_y','hit',
                            'trial_time','reaction_time','movement_time','fb_time','find_time','hold_time',
                            'abs_start_time','abs_target_time','pixel2mm', 'joystick_axis0', 'joystick_axis1', 'joystick_axis2', 'joystick_axis3']
            move_keys = ['trial_num','flag','t','dt','trial_time','rotation','start_x','start_y','cursor_x','cursor_y','hand_x','hand_y','joystick_axis0', 'joystick_axis1', 'joystick_axis2', 'joystick_axis3']
            #Variables to save for output
            history['trial_num'].append(self.trial_num+1)
            history['target_distance'].append(target.distance*PIXEL2MM)
            history['target_angle'].append(target.angle)
            history['rotation'].append(self.rotation)
            history['aiming_targets'].append(aiming.target)
            history['target_ring'].append(self.target_ring)
            history['online_feedback'].append(self.online_feedback)
            history['endpoint_feedback'].append(self.endpoint_feedback)
            history['binary_feedback'].append(self.binary_feedback)
            history['goal'].append(self.goal)
            history['instruction'].append(self.instruction)
            history['numericfb'].append(self.numericfb)
            history['currentpoints'].append(self.current_points)
            history['totalpoints'].append(self.total_points)
            history['currentscore'].append(self.current_score)
            history['totalscore'].append(self.total_score)
            history['pause'].append(self.pause)
            history['show_score'].append(self.show_score)

            history['cursor_angle'].append(cursor.angle*180/math.pi)
            history['cursor_r'].append(cursor.r*PIXEL2MM)
            history['hand_angle'].append(hand.angle*180/math.pi)
            history['hand_r'].append(hand.r*PIXEL2MM)
            
            history['abs_start_x'].append(start.x*PIXEL2MM)
            history['abs_start_y'].append(start.y*PIXEL2MM)
            history['abs_target_x'].append(target.x*PIXEL2MM)
            history['abs_target_y'].append(target.y*PIXEL2MM)
            history['abs_cursor_x'].append(cursor.xf*PIXEL2MM)
            history['abs_cursor_y'].append(cursor.yf*PIXEL2MM)
            history['abs_hand_x'].append(hand.xf*PIXEL2MM)
            history['abs_hand_y'].append(hand.yf*PIXEL2MM)

            history['start_x'].append((start.x - start.x)*PIXEL2MM)
            history['start_y'].append((start.y - start.y)*PIXEL2MM)
            history['target_x'].append((target.x - start.x)*PIXEL2MM)
            history['target_y'].append((start.y - target.y)*PIXEL2MM)
            history['cursor_x'].append((cursor.xf - start.x)*PIXEL2MM)
            history['cursor_y'].append((start.y - cursor.yf)*PIXEL2MM)
            history['hand_x'].append((hand.xf - start.x)*PIXEL2MM)
            history['hand_y'].append((start.y - hand.yf)*PIXEL2MM)

            history['hit'].append(target.hit)
            history['trial_time'].append(self.save_trial_time)
            history['reaction_time'].append(self.rt)
            history['movement_time'].append(self.move_time)
            history['fb_time'].append(self.fb_time)
            history['find_time'].append(self.find_time)
            history['hold_time'].append(self.hold_time)

            history['abs_start_time'].append(self.trial_start_time)
            history['abs_target_time'].append(self.reached_target_time)
            history['pixel2mm'].append(PIXEL2MM)
            history['joystick_axis0'].append(joystick_axis0)
            history['joystick_axis1'].append(joystick_axis1)
            history['joystick_axis2'].append(joystick_axis2)
            history['joystick_axis3'].append(joystick_axis3)
                            


            
            #Print the number of points
            if self.trial_num+1 >= self.trialset_len or self.exit:
                if self.max_score > 0:
                    GameScore(self,BLOCKFB_TIME)
            #Write the data (occurs after every trial
            WriteGameData(self,DATA_DIR,history,history_keys,move_data,move_keys) #This is a general function defined above
        #--------------------------------------------------------------------------------------------------------------        
        #Print goal on first trial
        cursor.r = 1000 #Stops it jumping to feedback on first trial
        self.pause_chk = 0
        self.pause_clear = 0
        self.show_score = 0
        GoalReminderFirstTrial(self)
        
        #iteration variables
        sample_time = 0
        trialnum = 0
        num_samples = 0
        x = 0
        y = 0
        x0 = 0
        y0 = 0
        trial_first_loop = True
        slowchk = 0
        SLOW = 0
        
        #This is the main trial loop------------------------------------------------------------------------------------------------------------------
        while trialnum < self.trialset_len:
            #Update Event Codes and timing
            #Set clock speed
            clock.tick(SAMPLING_RATE)
            if os.name == 'nt': # are we running Windows?
                self.current_time = time.clock()
            else:
                self.current_time = time.time()
            dt = self.current_time - self.previous_time
            self.game_time += dt
            self.previous_time += dt
            self.trial_time += dt
            sample_time += dt
            num_samples += 1
            CurrentEvent(self)
            
            
            #Get current trialset variables on first run through the trial loop only
            if trial_first_loop:
                target.distance = int(TARGET_DISTANCE[trialnum]*MM2PIXEL)
                target.angle = TARGET_ANGLE[trialnum]
                self.rotation = ROTATION[trialnum]
                aiming.target = AIMING_TARGETS[trialnum]
                self.target_ring = TARGET_RING[trialnum]
                self.online_feedback = ONLINE_FEEDBACK[trialnum]
                self.endpoint_feedback = ENDPOINT_FEEDBACK[trialnum]
                self.binary_feedback = BINARY_FEEDBACK[trialnum]
                self.pause = PAUSE[trialnum]
                self.show_score = SHOW_SCORE[trialnum]
                self.goal = GOAL[trialnum]
                self.instruction = INSTRUCTION[trialnum]
                self.numericfb = NUMERICFB[trialnum]
                self.hold_time = 0
                self.find_time = 0
                FIND_START = True
                trial_first_loop = False
                #Print trial number
                #font = pygame.font.Font(None, 36)
                #text = font.render("Trial "+str(int(trialnum+1)), 1, self.score_color)
                #self.draw_noerase_rectlist.append(self.screen.blit(text, (24,744)))

            #Poll mouse input and do any rotation computations
            for event in pygame.event.get():
                #Check for escape key for quiting the game
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit = True
                        GameHistoryUpdate(history,cursor,target,start,move_data,PIXEL2MM)    #This will call the saving function to save the game
                        pygame.display.quit()   #Closes the display
                        sys.exit()                          #Calls interrupt to end game
#                    if event.type == KEYDOWN:
#                        if event.key == K_SPACE:
#                            if NEXT_TRIAL: #Will only work if you are in the next_trial phase of the trial
#                                self.pause_chk = 1
                #Poll joystick
                x0 = hand.x
                y0 = hand.y
                joystick_axis0 = joystick.get_axis(0)
                joystick_axis1 = joystick.get_axis(1)
                joystick_axis2 = joystick.get_axis(2)
                joystick_axis3 = joystick.get_axis(3)

                x = ((joystick_axis0*(SCREEN_SIZE[0]/3.8))+(SCREEN_SIZE[0]/2))
                y = ((joystick_axis1*(SCREEN_SIZE[1]/2.8))+(SCREEN_SIZE[1]/2))

                #Compute cursor speed
                vx,vy,speed,direction = CursorVelocity(x0,y0,x,y,dt)

                #Record hand position
                hand.x = x
                hand.y = y
                hand.vx = vx
                hand.vy = vy
                hand.position = (int(x),int(y))
                
                #Apply rotation and place x and y into cursor class - as of now
                if self.online_feedback == 0:  #ENDPOINT ROTATION
                    (x,y) = FieldRotation(x,y,self.rotation,start,target)                            
                    cursor.x = int(x)
                    cursor.y = int(y)
                    cursor.position = (int(x),int(y))
                elif self.online_feedback == 1: #ONLINE FEEDBACK ROTATION
                    (x,y) = FieldRotation(x,y,self.rotation,start,target)                            
                    cursor.x = int(x)
                    cursor.y = int(y)
                    cursor.position = (int(x),int(y))
                    
                #Compute cursor distance relative to start
                StartDist(cursor, hand,start) 
            
            #THIS IS RIGHT HAND ONLY--------------------------------------------------------------------------------
            #Waiting for subject to find the start position
            if FIND_START:
                #Update Event Codes and timing
                self.find_time += dt
                CurrentEvent(self)
                #Plot start
                self.draw_rectlist.append(pygame.draw.circle(self.screen, start.color, start.position, start.width, 1))
                if cursor.r <= start.tolerance:
                    HOLD_START = True
                    FIND_START = False
                    CURSOR_VISIBLE = True
                    CURSOR_ZOOM = False
                    self.hold_time = 0
                
            #Subject must calm down and hold in the start position
            if HOLD_START:
                #Update Event Codes and timing
                self.hold_time += dt
                CurrentEvent(self)
                #Plot start
                self.draw_rectlist.append(pygame.draw.circle(self.screen, start.hold_color, start.position, start.width, 1)) #Keep drawing target
                #If they leave the start position, them make them go back
                if cursor.r > start.tolerance:
                    FIND_START = True
                    HOLD_START = False
                    CURSOR_ZOOM = True
                    CURSOR_VISIBLE = False
                    self.hold_time = 0
                    
                if cursor.r < start.tolerance/2 and self.hold_time >= HOLD_TIME:
                    SHOW_TARGET = True
                    HOLD_START = False
                    self.rt = 0
                    self.total_trials += 1
                    self.save_trial_time = self.trial_time
                    self.trial_time = 0
                    self.trial_start_time = self.game_time
                    #Plot target
                    TargetLocation(target,start)
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, TARGET_FILL))
                    #Plot aiming targets
                    AimingTargetLocation(aiming,target,start)
                    
            #If they waited long enough, then show them the target
            if SHOW_TARGET:
                #Update Event Codes and timing
                self.rt += dt
                CurrentEvent(self)
                 #Plot target
                #TargetLocation(target,start)
                
                #Plot target ring
                if self.target_ring == 1: #Draw circle
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.ring_color, start.position, target.distance, 1))
                    
                #Draw target last
                self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, 0))

                #If they moved outside the start circle
                if cursor.r > start.width:
                    MOVING = True
                    SHOW_TARGET = False
                    if self.online_feedback:
                        CURSOR_VISIBLE = True
                    else:
                        CURSOR_VISIBLE = False
                    self.move_time = 0

            #They are moving!    
            if MOVING:
                #Update Event Codes and timing
                self.move_time += dt
                CurrentEvent(self)

                #Plot target ring
                if self.target_ring == 1: #Draw circle
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.ring_color, start.position, target.distance, 1))
                    
                #Plot target
                self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, 0))
                #Did they hit the target? #THIS IF FOR FEEDBACK
                if cursor.r >= target.distance:
                    if cursor.angle*180/math.pi < -22.5:
                        fixedangle = cursor.angle*180/math.pi + 360
                    else:
                        fixedangle = cursor.angle*180/math.pi
                        #print (cursor.angle*180/math.pi, fixedangle, target.angle)

                    if math.fabs((target.angle - fixedangle)) < target.tolerance:
                        #if (cursor.x >= (target.x - target.width-tol) and cursor.x <= (target.x + target.width+tol) ) and (cursor.y >= (target.y - target.width-1) and cursor.y <= (target.y + target.width+1) ):
                        HIT = 1
                        target.hit = 1
                        if self.numericfb == 1:
                            self.current_points = 100
                            self.total_points += self.current_points
                            self.possible_points += 100
                        else:
                            self.current_score = 1
                            self.total_score += self.current_score
                        if self.binary_feedback > 0:
                            TARGET_FILL = 0
                            s = pygame.mixer.Sound('correct.wav')
                            s.play()
                        else:
                            TARGET_FILL = 1
                            s = pygame.mixer.Sound('chime1.wav')
                            s.play()
                    else:
                        HIT = 2
                        target.hit = 0
                        if self.numericfb == 1:
                            errorangle = math.fabs(target.angle-(cursor.angle*180/math.pi))
                            if errorangle > 180:
                                errorangle = math.fabs(360-errorangle)
                            self.current_points = int(100*((90- errorangle + target.tolerance)/90))
                            if self.current_points < 0:
                                self.current_points = 0
                            elif self.current_points > 100:
                                self.current_points = 100
                            self.total_points += self.current_points
                            self.possible_points += 100
                        if self.binary_feedback > 0:
                            TARGET_FILL = 1
                            s = pygame.mixer.Sound('incorrect.wav')
                            s.play()
                        else:
                            TARGET_FILL = 1
                            s = pygame.mixer.Sound('chime1.wav')
                            s.play()
                    if self.move_time > MOVE_TIME:
                       	HIT = 3
                       	SLOW = 1  


                    MOVING = False
                    CURSOR_VISIBLE = False
                    #Grab cursor characteristics
                    cursor.xf = cursor.x
                    cursor.yf = cursor.y
                    cursor.position_final_fb = (cursor.x,cursor.y)
                    #Grab hand characteristics
                    hand.xf = hand.x
                    hand.yf = hand.y
                    hand.position_final = (hand.x,hand.y)
                    self.delay_time = 0
                    #Plots FB location stuff
                    RotFBloc(cursor,start,target)

                    FEEDBACK = True
                    self.fb_time = 0   

            #Trial over, so show the feedback
            if FEEDBACK:
                #Update Event Codes and timing
                self.fb_time += dt
                self.reached_target_time = self.game_time
                CurrentEvent(self)
                #Plot aiming targets
                #AimingTargetLocation(aiming,target,start)
                #Plot target ring
                if self.target_ring == 1: #Draw circle
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.ring_color, start.position, target.distance, 1))

                #Paint the correct feedback        
                if HIT == 1 and self.endpoint_feedback == 1: #Hit
                    CURSOR_ENDPOINT_FB = True
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, TARGET_FILL))
                elif HIT == 2 and self.endpoint_feedback == 1: #Miss trial
                    CURSOR_ENDPOINT_FB = True
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, TARGET_FILL))
                elif HIT == 3 and self.endpoint_feedback == 1: #Slow trial
                    CURSOR_ENDPOINT_FB = True
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, TARGET_FILL))
                elif self.endpoint_feedback == 0:
                    CURSOR_ENDPOINT_FB = False
                    self.draw_rectlist.append(pygame.draw.circle(self.screen, target.color, target.position, target.width, TARGET_FILL))
                if self.numericfb == 1:
                    #Calulate feedback location
                    numericfbx = (target.distance*.6)*math.cos(target.angle*math.pi/180) + start.x
                    numericfby = -(target.distance*.6)*math.sin(target.angle*math.pi/180) + start.y
                    self.points_position = (int(numericfbx),int(numericfby))
                    #draw points
                    font = pygame.font.Font(None, self.points_font_size)
                    text = font.render(str(int(self.current_points)), 1, self.points_color)
                    self.draw_rectlist.append(self.screen.blit(text, self.points_position))   
                #Feedback time is over so reset everything
                if self.fb_time > FEEDBACK_TIME:
                    NEXT_TRIAL = True
                    FEEDBACK = False
                    CURSOR_ENDPOINT_FB = False

                    if SLOW == 1 and slowchk < 1:
                        s = pygame.mixer.Sound('tooslow.wav')
                        s.play()
                        slowchk = 1
                    
            if NEXT_TRIAL: #Clean up for next trial and check instructions

                if self.pause == 1 and self.show_score == 0 and self.pause_chk < 1:
                    GoalReminder(self,BLOCKFB_TIME)
                elif self.pause ==1 and self.show_score == 1 and self.pause_chk < 1:
                	GoalReminderScore(self,BLOCKFB_TIME)
                elif self.pause == 2 and self.pause_chk < 1:
                    GoalInstPause(self,BLOCKFB_TIME)
                elif self.pause == 3 and self.pause_chk < 1:
                    GoalInstReminder(self,BLOCKFB_TIME)
                elif self.pause == 4 and self.pause_chk < 1:
                    BreakScreen(self,BLOCKFB_TIME)
                elif self.pause == 5 and self.show_score == 0 and self.pause_chk < 1:
                    WashReminder(self,BLOCKFB_TIME)
                elif self.pause == 5 and self.show_score == 1 and self.pause_chk < 1:
                    WashReminderScore(self,BLOCKFB_TIME)
                elif self.pause == 6 and self.show_score == 0 and self.pause_chk < 1:
                    WashReminderPause(self,BLOCKFB_TIME)
                elif self.pause == 6 and self.show_score == 1 and self.pause_chk < 1:
                    WashReminderScorePause(self,BLOCKFB_TIME)
                else:
                    self.pause_chk = 1

                if self.pause_chk > 0:
                    #Update all the variables
                    FIND_START = True
                    NEXT_TRIAL = False
                    CURSOR_ZOOM = True
                    TARGET_FILL = 1
                    HIT = -1                    
                    GameHistoryUpdate(history,cursor,target,start,move_data,PIXEL2MM)
                    self.current_score = 0
                    #Reinitialize everything
                    trialnum += 1
                    self.trial_num = trialnum
                    num_samples = 0
                    trial_first_loop = True
                    #Clean times (start time doesnt get reset nor does trial_time)
                    self.find_time = 0
                    self.hold_time = 0
                    self.rt = 0
                    self.move_time = 0
                    self.fb_time = 0
                    SLOW = 0
                    slowchk = 0
                    self.pause_chk = 0
                    self.current_points = 0

  
                    CurrentEvent(self)
                    #Clean up the movement data, so it doesnt bog down the game
                    move_data = {'trial_num':[],'flag':[],'t':[],'dt':[],'trial_time':[],'rotation':[],
                     'start_x':[],'start_y':[],'cursor_x':[],'cursor_y':[],'hand_x':[],'hand_y':[],'joystick_axis0':[],'joystick_axis1':[],'joystick_axis2':[],'joystick_axis3':[]}
                    self.draw_rectlist.append(self.screen.fill(BACKGROUND_COLOR))
            
            #Save movement data
            move_data['trial_num'].append(self.trial_num+1)
            move_data['flag'].append(self.flag)
            move_data['t'].append(self.game_time)
            move_data['dt'].append(dt)
            move_data['trial_time'].append(self.trial_time)
            move_data['rotation'].append(self.rotation)
            move_data['start_x'].append(start.x*PIXEL2MM)
            move_data['start_y'].append(start.y*PIXEL2MM)
            move_data['cursor_x'].append(cursor.x*PIXEL2MM)
            move_data['cursor_y'].append(cursor.y*PIXEL2MM)
            move_data['hand_x'].append(hand.x*PIXEL2MM)
            move_data['hand_y'].append(hand.y*PIXEL2MM)
            move_data['joystick_axis0'].append(joystick_axis0)
            move_data['joystick_axis1'].append(joystick_axis1)
            move_data['joystick_axis2'].append(joystick_axis2)
            move_data['joystick_axis3'].append(joystick_axis3)
                        
            #Plot cursor
            if CURSOR_VISIBLE:
                self.draw_rectlist.append(pygame.draw.circle(self.screen, cursor.color, cursor.position, cursor.width, 0))
            elif CURSOR_ZOOM:
                if cursor.r < 1:#prevent values less than zero
                    cursor.r = 1
                self.draw_rectlist.append(pygame.draw.circle(self.screen,cursor.color,start.position,int(math.floor(cursor.r)),1))
                #self.draw_rectlist.append(pygame.draw.circle(self.screen, cursor.color, cursor.position, cursor.width, 0))
            elif CURSOR_ENDPOINT_FB:
                self.draw_rectlist.append(pygame.draw.circle(self.screen,cursor.hitcolor, cursor.position_fb, cursor.width, 0))
          
            #Update screen
            ScreenUpdate(self)

if __name__ == '__main__': Game()

