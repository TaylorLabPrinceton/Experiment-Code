#Load modules
import pygame, sys, os, math, time, datetime
from pygame.locals import *
from Joystick_AimingTargets_GameConstants import*

#================================================================
#These functions are general for the game, define screen, input window, and write files
#They are called within the Game class, which is the main game-loop

#This function paints every thing to the screen and cleans up objects on the screen
def ScreenUpdate(self):
    pygame.display.update(self.draw_rectlist + self.erase_rectlist)
    self.erase_rectlist = self.draw_rectlist
    for rect in self.erase_rectlist:
        self.screen.fill(BACKGROUND_COLOR, rect)
        self.draw_rectlist = []

def ScreenUpdateNoErase(self):
    pygame.display.update(self.draw_noerase_rectlist)

    
    
#This is the game window that prompts the user for the subjec name and trialset  
def GameInputWindow(self,DATA_DIR,TRIALSET_DIR):
    #This makes the initial window to get the trialset and data file name
    STILL_TYPING = True
    GET_SUBJECT = True
    GET_TRIALSET = False
    subject_fname = []
    trialset_fname = []
    font = pygame.font.Font(None, 36)
    text = font.render("Subject Filename: ", 1, (255, 255, 255))
    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
    ScreenUpdate(self)            
    while STILL_TYPING: #Use a while loop to grab the keys that the person presses
        if GET_SUBJECT:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #Reprint the text already on the screen
                    text = font.render("Subject Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
                    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
                    if ((event.key - 48) in range(10)):
                        #They pressed a number
                        subject_fname += (NUMBERS[event.key-48])
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif ((event.key - 97) in range(26)):
                        #If they pressed another letter add it to the filename
                        subject_fname += str(LETTERS[event.key-97])
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_BACKSPACE):
                        #if they hit backspace,remove the last key from the filename
                        subject_fname = subject_fname[:-1]
                        subject_fname = ''.join(subject_fname)
                        subtext = font.render(str(subject_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_RETURN):
                        fname = (DATA_DIR+'/'+str(subject_fname).replace("['","").replace("']","")+".txt")
                        if os.path.isfile(fname):
                            text = font.render("Subject File Already Exists", 1, (255, 0, 0))
                            self.draw_rectlist.append(self.screen.blit(text, (150,300)))
                            self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                            ScreenUpdate(self)
                            time.sleep(1)
                        elif not os.path.isfile(fname):
                            GET_TRIALSET = True
                            GET_SUBJECT = False
                    elif (event.key == K_ESCAPE):
                        pygame.display.quit()   #Closes the display
                        sys.exit()                          #Calls interrupt to end game
        if GET_TRIALSET:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    #Reprint the text already on the screen
                    text = font.render("Subject Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,100)))
                    text = font.render("Trial Set Filename: ", 1, (255, 255, 255))
                    self.draw_rectlist.append(self.screen.blit(text, (50,200)))
                    if ((event.key - 48) in range(10)):
                        #They pressed a number
                        trialset_fname += (NUMBERS[event.key-48])
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif ((event.key - 97) in range(26)):
                        #They pressed a letter
                        trialset_fname += (LETTERS[event.key-97])
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))

                        ScreenUpdate(self)
                    elif (event.key == K_BACKSPACE):
                        #if they hit backspace,remove the last key from the filename
                        trialset_fname = trialset_fname[:-1]
                        trialset_fname = ''.join(trialset_fname)
                        trialtext = font.render(str(trialset_fname),1,(0,0,255))
                        self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                        self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                        ScreenUpdate(self)
                    elif (event.key == K_RETURN):
                        fname = (TRIALSET_DIR+'/'+str(trialset_fname).replace("['","").replace("']","")+".tgt").lower()
                        if not os.path.isfile(fname):
                            text = font.render("File Does Not Exist", 1, (255, 0, 0))
                            self.draw_rectlist.append(self.screen.blit(text, (150,300)))
                            self.draw_rectlist.append(self.screen.blit(trialtext,(350,200)))
                            self.draw_rectlist.append(self.screen.blit(subtext,(350,100)))
                            ScreenUpdate(self)
                        elif os.path.isfile(fname):
                            GET_TRIALSET = False
                            STILL_TYPING = False
                    elif event.key == K_ESCAPE:
                        pygame.display.quit()   #Closes the display
                        sys.exit()                          #Calls interrupt to end game
    #Create file for saving
    data_fname = (str(subject_fname).replace("['","").replace("']","")+".txt")
    self.data_fname = data_fname
    movedata_fname = ("MOVE"+str(subject_fname).replace("['","").replace("']","")+".txt")
    self.movedata_fname = movedata_fname 
    trialset_fname = (str(trialset_fname).replace("['","").replace("']","")+".tgt").lower()
    self.trialset_fname = trialset_fname

def WriteGameData(self,DATA_DIR,history,history_keys,move_data,move_keys):
    #Check to see if path exists, if not make it
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    #Write game data
    data_file = open(DATA_DIR+'/'+self.data_fname,'w')  #The flag 'a' will append and the 'w' will overwrite
    
    #Write header on first trial only
    #if self.trial_num == 0:
    for i in range(len(history_keys)):
        data_file.write(str(history_keys[i])+'\t')
    data_file.write('\n')
    
    #Write abstracted data
    for i in range(len(history['trial_num'])): #This cycles through the number of rows (or trials)
        for j in range(len(history)): #This cycles through the number of variables
            data_file.write(str(history[history_keys[j]][i])+'\t') #You use the keys to select the right variable in the dictionary and then write one variable from it 
        data_file.write('\n')
    data_file.close()
    #Write movement data
    data_file = open(DATA_DIR+'/'+self.movedata_fname,'a')
    
    #Write header on first trial only
    if self.trial_num == 0:
        for i in range(len(move_keys)):
            data_file.write(str(move_keys[i])+'\t')
        data_file.write('\n')
        
    #Write movement data
    for i in range(len(move_data['t'])): #This cycles through the number of rows (or trials)
        for j in range(len(move_data)): #This cycles through the number of variables
            data_file.write(str(move_data[move_keys[j]][i])+'\t') #You use the keys to select the right variable in the dictionary and then write one variable from it 
        data_file.write('\n')
    data_file.close()

    if self.trial_num == self.trialset_len-1:
        pygame.display.quit()   #Closes the display
        sys.exit()                          #Calls interrupt to end game

##    #Put in delay to make sure game gets back up to speed
##    pygame.time.delay(int(DATA_WRITE_DELAY*1000))
#=========================================================================
