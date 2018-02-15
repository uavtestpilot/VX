import os, sound, time, wave, struct
from waveGenerator import waveGenerator
from scene import *



# for waveViewTD()
from PIL import Image
import ImageDraw
import ui

        
# To keep track of the state of the buttons, messages, files displayed...etc.
state = {"recordButton" : "notDisplayed", "stopRecordButton" : "notDisplayed", \
         "playButton" : "notDisplayed", "stopPlayButton" : "notDisplayed", \
         "XformItButton" : "notDisplayed", "XformingItButton" : "notDisplayed", \
         
         "originalsButton" : "notDisplayed", \
         "clearScreenOriginalsButton" : "notDisplayed", \
         "originalRecordings" : "notDisplayed", \
         "originalRecording" : "notSelected", \
         "originalRecSelectedIndex" : None, \
         "originalRecordings_Msg" : "notDisplayed", \
         "noOriginalRecordings_Msg" : "notDisplayed", \
                  
         "singersButton" : "notDisplayed", \
         "clearScreenSingersButton" : "notDisplayed", \
         "singerRecordings" : "notDisplayed", \
         "singerRecording" : "notSelected", \
         "singerRecSelectedIndex" : None, \
         "singerRecordings_Msg" : "notDisplayed", \
         "noSingerRecordings_Msg" : "notDisplayed", \
                  
         "XformedButton" : "notDisplayed", \
         "clearScreenXformedButton" : "notDisplayed", \
         "XformedRecordings" : "notDisplayed", \
         "XformedRecording" : "notSelected", \
         "XformedRecSelectedIndex" : None, \
         "XformedRecordings_Msg" : "notDisplayed", \
         "noXformedRecordings_Msg" : "notDisplayed", \
         
         "noRecordingSelected_Msg" : "notDisplayed", \
         
         "song" : None, \
         "originalRecSound" : None, \
         "singerRecSound" : None, \
         "XformedRecSound" : None}
         
"""
"*Button" : ["notDisplayed"/"displayed"]
"*Recording" : ["selected"/"notSelected"] ...an individual recording
"*Recordings" : ["displayed"/"notDisplayed"] ...the recordings as a group
"*Index" : [None/integerNumber] ...the index of a selected recording in the    
                                   recordings list
song : [None/sound.Player() object]
"""




# paths (directories) to store the wave files created
path2_voices2emulate = './waveFiles/voices2emulate/'
path2_transformedVoices = './waveFiles/transformedVoices/'
path2_originalVoices = './waveFiles/originalVoices/'

path2_temp = './waveFiles/temp/' # user won't see or access this one

record = sound.Recorder(path2_temp + 'temporary.wav')

# Voice X-formation functions, import must be done here so it has access to above
from VXfunctions import XformRecording

  
      
def recordButton(self): 
  global record
  # The "record" button actually consists of the record and stopRecord buttons
  if state["recordButton"] == "notDisplayed":
    display_recordButton(self)
    if state["stopRecordButton"] == "displayed":
      remove_stopRecordButton(self)
      record.stop()
      renameRecording()
  elif state["recordButton"] == "displayed":
    display_stopRecordButton(self)
    remove_recordButton(self)
    record.record()
    
 
   
def renameRecording():   
  # when recording has stopped rename the temporary file to a unique filename
  path_file = path2_originalVoices + time.asctime() + '.wav'
  os.rename('./waveFiles/temp/temporary.wav', path_file)

    
            
def XformItButton(self):
  if state["XformItButton"] == "notDisplayed":
    display_XformItButton(self)
    if state["XformingItButton"] == "displayed":
      remove_XformingItButton(self) 
  elif state["XformItButton"] == "displayed" and \
       state["singerRecSelectedIndex"] != None and \
       state["originalRecSelectedIndex"] != None: 
    display_XformingItButton(self)
    remove_XformItButton(self)   
    state["XformedRecSound"] = XformRecording(self) # played by update method
  elif state["XformItButton"] == "displayed" :
    display_noRecordingSelected_Msg(self, True)

    
    
def playButton(self):
  # The "play" button actually consists of the play and stopPlay buttons
  if state["playButton"] == "notDisplayed":
    display_playButton(self)
    if state["stopPlayButton"] == "displayed":
      remove_stopPlayButton(self)
      state["song"].stop() 
      state["song"] = None  
  elif state["playButton"] == "displayed" and \
       (state["originalRecording"] == "selected" or \
       state["singerRecording"] == "selected" or \
       state["XformedRecording"] == "selected") :
    playRecording(self)  
  elif state["playButton"] == "displayed" :
    display_noRecordingSelected_Msg(self, False)
  

      
def playRecording(self):
  display_stopPlayButton(self)
  remove_playButton(self)
  if state["originalRecording"] == "selected" :
    path = path2_originalVoices
    file = path + self.originalRecordings[state["originalRecSelectedIndex"]].text
  elif state["singerRecording"] == "selected" :
    path = path2_voices2emulate
    file = path + self.singerRecordings[state["singerRecSelectedIndex"]].text
  else :
    path = path2_transformedVoices
    file = path + self.XformedRecordings[state["XformedRecSelectedIndex"]].text  
  
  state["song"] = sound.Player(file)
  state["song"].play()

    
          
def originalsButton(self):
  # The "originals" button actually consists of the originals and clearScreenOriginals buttons
  if state["originalsButton"] == "notDisplayed":
    display_originalsButton(self)
    if state["clearScreenOriginalsButton"] == "displayed":
      remove_clearScreenOriginalsButton(self)
      if state["originalRecordings"] == "displayed" :
        remove_originalRecordings(self)
  elif state["originalsButton"] == "displayed":
    remove_originalsButton(self)
    display_clearScreenOriginalsButton(self)
    display_originalRecordings(self)
    
    if state["clearScreenSingersButton"] == "displayed":
      remove_clearScreenSingersButton(self)
      display_singersButton(self)
      if state["singerRecordings"] == "displayed" :
        remove_singerRecordings(self)      
    elif state["clearScreenXformedButton"] == "displayed":
      remove_clearScreenXformedButton(self)
      display_XformedButton(self)
      if state["XformedRecordings"] == "displayed" :
        remove_XformedRecordings(self)



def singersButton(self):
  # The "singers" button actually consists of the singers and clearScreenSingers buttons
  if state["singersButton"] == "notDisplayed":
    display_singersButton(self)
    if state["clearScreenSingersButton"] == "displayed":
      remove_clearScreenSingersButton(self)
      if state["singerRecordings"] == "displayed" :
        remove_singerRecordings(self)
  elif state["singersButton"] == "displayed":
    remove_singersButton(self)
    display_clearScreenSingersButton(self)
    display_singerRecordings(self)
    
    if state["clearScreenOriginalsButton"] == "displayed":
      remove_clearScreenOriginalsButton(self)
      display_originalsButton(self)
      if state["originalRecordings"] == "displayed" :
        remove_originalRecordings(self)      
    elif state["clearScreenXformedButton"] == "displayed":
      remove_clearScreenXformedButton(self)
      display_XformedButton(self)
      if state["XformedRecordings"] == "displayed" :
        remove_XformedRecordings(self)


        
def XformedButton(self):
  # The "Xformed" button actually consists of the Xformed and clearScreenXformed buttons
  if state["XformedButton"] == "notDisplayed":
    display_XformedButton(self)
    if state["clearScreenXformedButton"] == "displayed":
      remove_clearScreenXformedButton(self)
      if state["XformedRecordings"] == "displayed" :
        remove_XformedRecordings(self)
  elif state["XformedButton"] == "displayed":
    remove_XformedButton(self)
    display_clearScreenXformedButton(self)
    display_XformedRecordings(self)    
    
    if state["clearScreenSingersButton"] == "displayed":
      remove_clearScreenSingersButton(self)
      display_singersButton(self)
      if state["singerRecordings"] == "displayed" :
        remove_singerRecordings(self)      
    elif state["clearScreenOriginalsButton"] == "displayed":
      remove_clearScreenOriginalsButton(self)
      display_originalsButton(self)
      if state["originalRecordings"] == "displayed" :
        remove_originalRecordings(self)


     
def displayAlternateButtons(self, touch):
  """
  play the click sound if a button has been touched, and then display the appropriate button
  """
  if touch.location in self.playButtonOuter.bbox:
    sound.play_effect('drums:Drums_01')
    playButton(self)     
  elif touch.location in self.recordButtonOuter.bbox:
    sound.play_effect('drums:Drums_01')
    recordButton(self)      
  elif touch.location in self.originalsButtonOuter.bbox:
    sound.play_effect('drums:Drums_01')
    originalsButton(self)     
  elif touch.location in self.singersButtonOuter.bbox: 
    sound.play_effect('drums:Drums_01')
    singersButton(self)     
  elif touch.location in self.XformedButtonOuter.bbox: 
    sound.play_effect('drums:Drums_01')
    XformedButton(self)
  elif touch.location in self.XformItButtonOuter.bbox: 
    # only want user to be able to activate button in one "direction"...
    # the previous button state returns when its done processing the files
    if state["XformItButton"] == "displayed": 
      XformItButton(self)
  
    
  
  
def displayButtons(self):
  """
  create and display all initial buttons on startup
  """
  playButton(self) # create and display the play button
  recordButton(self) # create and display the record button
  XformItButton(self) # create and display the X-form button
  
  # create and display the file listing buttons
  singersButton(self)
  XformedButton(self)
  originalsButton(self)
  sound.play_effect('digital:PowerUp10') # sound for initial startup of program
  
  
 
  
  


# list recorded files to play or Xform *********************************************

def displayTitle(self, title):
  self.title = LabelNode()
  self.title.text = title
  self.title.font = ('Zapfino', 45)
  self.title.color = "#ff3c00"
  self.title.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.title)
   
    
def displaySunburstSprite(self):
  self.spriteNode = SpriteNode('shp:aura')
  self.spriteNode.position = self.size/2
  self.add_child(self.spriteNode)
  
  
def moveSprite(self, touch):
  x, y = touch.location
  slideTime = 0.5 # seconds
  move_action = Action.move_to(x, y, slideTime, TIMING_SINODIAL)
  self.spriteNode.run_action(move_action)


    
# Record Button Logic **************************************************************
def remove_recordButton(self):
  state["recordButton"] = "notDisplayed"
  self.recordButtonOuter.remove_from_parent()
  self.recordButton.remove_from_parent()
  self.recordButtonTitle.remove_from_parent()
  
  
def remove_stopRecordButton(self):
  state["stopRecordButton"] = "notDisplayed"
  self.stopRecordButtonOuter.remove_from_parent()
  self.stopRecordButton.remove_from_parent()
  self.stopRecordButtonTitle.remove_from_parent()
            
         
def display_stopRecordButton(self):
  x = 100
  y = self.size[1] - 100
  state["stopRecordButton"] = "displayed"
  self.stopRecordButtonOuter = SpriteNode('pzl:Red8')
  self.stopRecordButtonOuter.position = (x, y)
  self.add_child(self.stopRecordButtonOuter)

  self.stopRecordButton = SpriteNode('iob:ios7_mic_off_24')
  self.stopRecordButton.position = (x, y)
  self.add_child(self.stopRecordButton)
  
  self.stopRecordButtonTitle = LabelNode('Hoefler Text')
  self.stopRecordButtonTitle.text = "STOP recording"
  self.stopRecordButtonTitle.position = (x, y - 30)
  self.add_child(self.stopRecordButtonTitle)
   
  

def display_recordButton(self):
  x = 100
  y = self.size[1] - 100
  state["recordButton"] = "displayed"
  self.recordButtonOuter = SpriteNode('pzl:Purple8')
  self.recordButtonOuter.position = (x, y)
  self.add_child(self.recordButtonOuter)

  self.recordButton = SpriteNode('iow:ios7_mic_24')
  self.recordButton.position = (x, y)
  self.add_child(self.recordButton)
  
  self.recordButtonTitle = LabelNode('Hoefler Text')
  self.recordButtonTitle.text = "record"
  self.recordButtonTitle.position = (x, y - 30)
  self.add_child(self.recordButtonTitle) 
   
   
   
# Play Button Logic ****************************************************************
def remove_stopPlayButton(self):
  state["stopPlayButton"] = "notDisplayed"
  self.stopPlayButtonOuter.remove_from_parent()
  self.stopPlayButton.remove_from_parent()
  self.stopPlayButtonTitle.remove_from_parent()
     
  
def remove_playButton(self):
  state["playButton"] = "notDisplayed"
  self.playButtonOuter.remove_from_parent()
  self.playButton.remove_from_parent()
  self.playButtonTitle.remove_from_parent()

   
def display_playButton(self):
  x = self.size[0] - 100
  y = self.size[1] - 100
  state["playButton"] = "displayed"
  self.playButtonOuter = SpriteNode('pzl:Purple8')
  self.playButtonOuter.position = (x, y)
  self.add_child(self.playButtonOuter)

  self.playButton = SpriteNode('iow:arrow_right_b_24')
  self.playButton.position = (x, y)
  self.add_child(self.playButton)
  
  self.playButtonTitle = LabelNode('Hoefler Text')
  self.playButtonTitle.text = "play"
  self.playButtonTitle.position = (x, y - 30)
  self.add_child(self.playButtonTitle) 

  
def display_stopPlayButton(self):
  x = self.size[0] - 100
  y = self.size[1] - 100
  state["stopPlayButton"] = "displayed"
  self.stopPlayButtonOuter = SpriteNode('pzl:Red8')
  self.stopPlayButtonOuter.position = (x, y)
  self.add_child(self.stopPlayButtonOuter)

  self.stopPlayButton = SpriteNode('iob:stop_24')
  self.stopPlayButton.position = (x, y)
  self.add_child(self.stopPlayButton)
  
  self.stopPlayButtonTitle = LabelNode('Hoefler Text')
  self.stopPlayButtonTitle.text = "STOP playing"
  self.stopPlayButtonTitle.position = (x, y - 30)
  self.add_child(self.stopPlayButtonTitle)


    
# Singers 2 Emulate Button Logic *************************************************    
def remove_singersButton(self):
  if state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()   
    
  state["singersButton"] = "notDisplayed"
  self.singersButtonOuter.remove_from_parent()
  self.singersButton.remove_from_parent()
  self.singersButtonTitle.remove_from_parent()

     
               
def remove_clearScreenSingersButton(self):
  if state["noSingerRecordings_Msg"] == "displayed":
    self.noSingerRecordings_Msg.remove_from_parent()
    state["noSingerRecordings_Msg"] = "notDisplayed"
  elif state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()  
    
  state["clearScreenSingersButton"] = "notDisplayed"
  self.clrSingersButtonOuter.remove_from_parent()
  self.clrSingersButton.remove_from_parent()
  self.clrSingersButtonTitle.remove_from_parent()
  
    
        
def display_singersButton(self): 
  x = self.size[0] - 100
  y = self.size[1]/2
  state["singersButton"] = "displayed"
  self.singersButtonOuter = SpriteNode('pzl:Blue8')
  self.singersButtonOuter.position = (x, y)
  self.singersButtonOuter.x_scale = 2
  self.add_child(self.singersButtonOuter)
  
  self.singersButton = SpriteNode('iob:ios7_folder_outline_32')
  self.singersButton.position = (x, y)
  self.add_child(self.singersButton)
  
  self.singersButtonTitle = LabelNode('Hoefler Text')
  self.singersButtonTitle.text = "Singers to Emulate"
  self.singersButtonTitle.position = (x, y - 30)
  self.add_child(self.singersButtonTitle)
    
  
def display_clearScreenSingersButton(self):
  x = self.size[0] - 100
  y = self.size[1]/2
  state["clearScreenSingersButton"] = "displayed"
  self.clrSingersButtonOuter = SpriteNode('pzl:PaddleRed')
  self.clrSingersButtonOuter.position = (x, y)
  self.clrSingersButtonOuter.x_scale = 1.5
  self.add_child(self.clrSingersButtonOuter)
  
  self.clrSingersButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrSingersButton.position = (x, y)
  self.add_child(self.clrSingersButton)
  
  self.clrSingersButtonTitle = LabelNode('Hoefler Text')
  self.clrSingersButtonTitle.text = "Clear Screen"
  self.clrSingersButtonTitle.position = (x, y - 30)
  self.add_child(self.clrSingersButtonTitle)
    


# Xformed Button Logic *************************************************************  
def remove_XformedButton(self):
  if state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()    
    
  state["XformedButton"] = "notDisplayed"
  self.XformedButtonOuter.remove_from_parent()
  self.XformedButton.remove_from_parent()
  self.XformedButtonTitle.remove_from_parent()

                
  
def remove_clearScreenXformedButton(self):
  if state["noXformedRecordings_Msg"] == "displayed":
    self.noXformedRecordings_Msg.remove_from_parent()
    state["noXformedRecordings_Msg"] = "notDisplayed"
  elif state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()    
  
  state["clearScreenXformedButton"] = "notDisplayed"
  self.clrXformedButtonOuter.remove_from_parent()
  self.clrXformedButton.remove_from_parent()
  self.clrXformedButtonTitle.remove_from_parent()
     
 
             
def display_clearScreenXformedButton(self):
  x = self.size[0] - 100
  y = 235
  state["clearScreenXformedButton"] = "displayed"
  self.clrXformedButtonOuter = SpriteNode('pzl:PaddleRed')
  #self.clrXformedButtonOuter.position = (self.size[0] - 275, self.size[1] - 100)
  self.clrXformedButtonOuter.position = (x, y)
  self.clrXformedButtonOuter.x_scale = 1.5
  self.add_child(self.clrXformedButtonOuter)
  
  self.clrXformedButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrXformedButton.position = (x, y)
  self.add_child(self.clrXformedButton)
  
  self.clrXformedButtonTitle = LabelNode('Hoefler Text')
  self.clrXformedButtonTitle.text = "Clear Screen"
  self.clrXformedButtonTitle.position = (x, y - 30)
  self.add_child(self.clrXformedButtonTitle)
 
    
def display_XformedButton(self):
  x = self.size[0] - 100
  y = 235
  state["XformedButton"] = "displayed"
  self.XformedButtonOuter = SpriteNode('pzl:Blue8')
  self.XformedButtonOuter.position = (x, y)
  self.XformedButtonOuter.x_scale = 2
  self.add_child(self.XformedButtonOuter)
  
  self.XformedButton = SpriteNode('iob:ios7_folder_outline_32')
  self.XformedButton.position = (x, y)
  self.add_child(self.XformedButton)
  
  self.XformedButtonTitle = LabelNode('Hoefler Text')
  self.XformedButtonTitle.text = "X-formed Recordings"
  self.XformedButtonTitle.position = (x, y - 30)
  self.add_child(self.XformedButtonTitle) 
   
    

# Original Recordings Button Logic ************************************************* 
def remove_originalsButton(self):
  if state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()   
    
  state["originalsButton"] = "notDisplayed"
  self.originalsButtonOuter.remove_from_parent()
  self.originalsButton.remove_from_parent()
  self.originalsButtonTitle.remove_from_parent()
    
        
def remove_clearScreenOriginalsButton(self): 
  if state["noOriginalRecordings_Msg"] == "displayed":
    self.noOriginalRecordings_Msg.remove_from_parent()
    state["noOriginaldRecordings_Msg"] = "notDisplayed"
  elif state["noRecordingSelected_Msg"] == "displayed":
    state["noRecordingSelected_Msg"] = "notDisplayed"
    self.noRecordingSelected_Msg.remove_from_parent()    
    
  state["clearScreenOriginalsButton"] = "notDisplayed"
  self.clrOriginalsButtonOuter.remove_from_parent()
  self.clrOriginalsButton.remove_from_parent()
  self.clrOriginalsButtonTitle.remove_from_parent()
          
  
def display_originalsButton(self):
  x = self.size[0] - 100
  #y = self.size[1] - 200
  y = 520
  state["originalsButton"] = "displayed"
  self.originalsButtonOuter = SpriteNode('pzl:Blue8')
  #self.originalsButtonOuter.position = (275, self.size[1] - 100)
  self.originalsButtonOuter.position = (x, y)
  self.originalsButtonOuter.x_scale = 2
  self.add_child(self.originalsButtonOuter)
  
  self.originalsButton = SpriteNode('iob:ios7_folder_outline_32')
  self.originalsButton.position = (x, y)
  self.add_child(self.originalsButton)
  
  self.originalsButtonTitle = LabelNode('Hoefler Text')
  self.originalsButtonTitle.text = "Original Recordings"
  self.originalsButtonTitle.position = (x, y - 30)
  self.add_child(self.originalsButtonTitle) 
           
    
def display_clearScreenOriginalsButton(self):
  x = self.size[0] - 100
  #y = self.size[1] - 200
  y = 520
  state["clearScreenOriginalsButton"] = "displayed"
  self.clrOriginalsButtonOuter = SpriteNode('pzl:PaddleRed')
  self.clrOriginalsButtonOuter.position = (x, y)
  self.clrOriginalsButtonOuter.x_scale = 1.5
  self.add_child(self.clrOriginalsButtonOuter)
  
  self.clrOriginalsButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrOriginalsButton.position = (x, y)
  self.add_child(self.clrOriginalsButton)
   
  self.clrOriginalsButtonTitle = LabelNode('Hoefler Text')
  self.clrOriginalsButtonTitle.text = "Clear Screen"
  self.clrOriginalsButtonTitle.position = (x, y - 30)
  self.add_child(self.clrOriginalsButtonTitle) 



# Listing Logic common to all ******************************************************
def display_noRecordingSelected_Msg(self, Xform):
  global state
  sound.play_effect('game:Ding_3')
   
  if state["originalRecordings_Msg"] == "displayed" :
    self.originalRecordings_Msg.remove_from_parent()
    state["originalRecordings_Msg"] = "notDisplayed"    
  elif state["singerRecordings_Msg"] == "displayed" :
    self.singerRecordings_Msg.remove_from_parent()
    state["singerRecordings_Msg"] = "notDisplayed"
  elif state["XformedRecordings_Msg"] == "displayed" :
    self.XformedRecordings_Msg.remove_from_parent()
    state["XformedRecordings_Msg"] = "notDisplayed"
  elif state["noXformedRecordings_Msg"] == "displayed" :
    self.noXformedRecordings_Msg.remove_from_parent()
    state["noXformedRecordings_Msg"] = "notDisplayed"
  elif state["noSingerRecordings_Msg"] == "displayed" :
    self.noSingerRecordings_Msg.remove_from_parent()
    state["noSingerRecordings_Msg"] = "notDisplayed"
  elif state["noOriginalRecordings_Msg"] == "displayed" :
    self.noOriginalRecordings_Msg.remove_from_parent()
    state["noOriginalRecordings_Msg"] = "notDisplayed"
  
  if state["noRecordingSelected_Msg"] != "displayed" :
    # display error message 
    x = self.size[0]/2
    y = self.size[1] - 200
    
    state["noRecordingSelected_Msg"] = "displayed"
    self.noRecordingSelected_Msg = LabelNode()
    self.noRecordingSelected_Msg.color = "#000000"
    self.noRecordingSelected_Msg.font = ('Symbol', 40)
    if Xform:
      self.noRecordingSelected_Msg.text = "X-form Needs 2 Recordings To Be Selected"
    else:
      self.noRecordingSelected_Msg.text = "-- No Recording Selected To Be Played --"
    #self.noRecordingSelected_Msg.position = (self.size[0]/2, 575)
    self.noRecordingSelected_Msg.position = (x, y)
    self.add_child(self.noRecordingSelected_Msg) 
  else:
    # add_child only once, but change message as necessary
    if Xform:
      self.noRecordingSelected_Msg.text = "X-form Needs 2 Recordings To Be Selected"
    else:
      self.noRecordingSelected_Msg.text = "-- No Recording Selected To Be Played --"
 
       
# Original Recordings Listing Logic ************************************************ 
def remove_originalRecordings(self):
  global state
  if state["originalRecordings_Msg"] == "displayed" :
    self.originalRecordings_Msg.remove_from_parent()
    state["originalRecordings_Msg"] = "notDisplayed"   
  else:
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"
    
  if state["originalRecordings"] == "displayed":   
    
    state["originalRecordings"] = "notDisplayed"
    state["originalRecording"] = "notSelected"
    #state["previous_originalIndex"] = state["originalRecSelectedIndex"]
    #state["originalRecSelectedIndex"] = None
    for index in range(len(self.originalRecordingsOuter)):
      self.originalRecordingsOuter[index].remove_from_parent()
      self.originalRecordings[index].remove_from_parent()
                        
 
                    
def display_originalRecordings_Msg(self):  
  global state
  x = self.size[0]/2
  y = self.size[1] - 200
  if state["noRecordingSelected_Msg"] == "displayed" :
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"   
    
  if state["originalRecordings_Msg"] != "displayed":
    # display recordings listing message
    state["originalRecordings_Msg"] = "displayed"
    self.originalRecordings_Msg = LabelNode()
    self.originalRecordings_Msg.color = "#ff0909"
    #self.originalRecordings_Msg.color = "#ffffff"
    
    self.originalRecordings_Msg.font = ('Papyrus', 40)
    self.originalRecordings_Msg.text = "Original Recordings:"
    #self.originalRecordings_Msg.position = (self.size[0]/2, 575)
    self.originalRecordings_Msg.position = (x, y)
    self.add_child(self.originalRecordings_Msg)  
    

 
def display_noOriginalRecordingsCreatedYet_Msg(self):
  # display the "error" message
  x = self.size[0]/2
  y = self.size[1] - 200
  state["noOriginalRecordings_Msg"] = "displayed"
  self.noOriginalRecordings_Msg = LabelNode()
  self.noOriginalRecordings_Msg.color = "#ff0909"
  self.noOriginalRecordings_Msg.font = ('Times New Roman', 60)
  self.noOriginalRecordings_Msg.text = "No Original Recordings created yet."
  self.noOriginalRecordings_Msg.position = (x, y)
  self.add_child(self.noOriginalRecordings_Msg)  

  
    
def displayOriginalsRecordings(self, recordings, index, x, x_offset, y, y_offset):
  # name of file to be displayed
  self.originalRecordings.append(LabelNode())
  self.originalRecordings[index].font = ('American Typewriter', 15)
  self.originalRecordings[index].text = recordings[index]
  self.originalRecordings[index].color = "black"
  self.originalRecordings[index].anchor_point = (0, 0.5) # lower left
  #self.originalRecordings[index].anchor_point = (0.5, 0.5) # lower left
  self.originalRecordings[index].position = (x + 7, y - y_offset)
   
  # the "container" around the filename for easy highlighting by the user
  self.originalRecordingsOuter.append(SpriteNode('pzl:Button1'))
  #self.originalRecordingsOuter.append(SpriteNode('pzl:Yellow8'))
  self.originalRecordingsOuter[index].anchor_point = (0, 0.5) # lower left
  #self.originalRecordingsOuter[index].color = "#7bffa9"
  (X, Y) = self.originalRecordings[index].size
  self.originalRecordingsOuter[index].size = (X + 15, Y)    
  self.originalRecordingsOuter[index].position = (x, y - y_offset)    
  #ground = Node(parent=self)
  self.add_child(self.originalRecordingsOuter[index])
  #ground = Node(parent=self.originalRecordingsOuter[index])
  #originalRecordingsOuter[index].add_child(self.originalRecordings[index])
  self.add_child(self.originalRecordings[index]) #text on top of "button"
 
    
          
def was_originalRecordingsFileSelected(self, touch):
  orgRecOut = self.originalRecordingsOuter
  
  for index in range(len(orgRecOut)): 
    # if file selected highlight it.
    if touch.location in orgRecOut[index].bbox:
      sound.play_effect('8ve:8ve-tap-double')
      if index == state["originalRecSelectedIndex"]:
        return # same file has already been selected
      state["originalRecPrevColor"] = orgRecOut[index].color
      orgRecOut[index].color = "yellow"
      state["originalRecNewColor"] = orgRecOut[index].color
      orgRecOut[index].scale = 1.1
      (X, Y) = orgRecOut[index].position 
      orgRecOut[index].position = (X - 10, Y)
  
      # so I know which recording to play if the play button is selected.
      state["originalRecSelectedIndex"] = index 
      state["originalRecording"] = "selected"
      
      if state["noRecordingSelected_Msg"] == "displayed":
        display_originalRecordings_Msg(self)      
      
      # if a file is selected make sure any previous selected file is unselected
      for index in range(len(orgRecOut)):
        if orgRecOut[index].color == state["originalRecNewColor"] and \
           index != state["originalRecSelectedIndex"]:
          orgRecOut[index].color = state["originalRecPrevColor"]
          orgRecOut[index].scale = 1
          (X, Y) = orgRecOut[index].position 
          orgRecOut[index].position = (X + 10, Y)
          break      
          
      break
 
         
       
def display_originalRecordings(self): 
  global state
  # return the wave files of the original recordings that have been made so far.
  recordings = os.listdir(path2_originalVoices)
  if len(recordings) == 0 :
    display_noOriginalRecordingsCreatedYet_Msg(self)  
    return 
  
  display_originalRecordings_Msg(self)      
  state["originalRecordings"] = "displayed"
  self.originalRecordings = list()
  self.originalRecordingsOuter = list()
  x = 25
  x_offset = 0
  y = 520
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
  
    if x + (len(recordings[index]) * xFactor)  > 900:
      x = 25
      y_offset += 30
     
            
    displayOriginalsRecordings(self, recordings, index, x, x_offset, y, y_offset)
    
    (X, Y) = self.originalRecordingsOuter[index].size
    x += X + 15
    
    

        
    
# Xformed Recordings Listing Logic ************************************************ 
def remove_XformedRecordings(self):
  global state
  if state["XformedRecordings_Msg"] == "displayed" :
    self.XformedRecordings_Msg.remove_from_parent()
    state["XformedRecordings_Msg"] = "notDisplayed"   
  else: 
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"   

        
  if state["XformedRecordings"] == "displayed":
    
    state["XformedRecordings"] = "notDisplayed"
    state["XformedRecording"] = "notSelected"
    state["XformedRecSelectedIndex"] = None
    for index in range(len(self.XformedRecordingsOuter)):
      self.XformedRecordingsOuter[index].remove_from_parent()
      self.XformedRecordings[index].remove_from_parent()
                        
 
                    
def display_XformedRecordings_Msg(self):  
  global state
  x = self.size[0]/2
  y = self.size[1] - 200
  
  if state["noRecordingSelected_Msg"] == "displayed" :
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"   
    
  if state["XformedRecordings_Msg"] != "displayed":
    # display recordings listing message
    state["XformedRecordings_Msg"] = "displayed"
    self.XformedRecordings_Msg = LabelNode()
    self.XformedRecordings_Msg.color = "#ff0909"
    self.XformedRecordings_Msg.font = ('Papyrus', 40)
    self.XformedRecordings_Msg.text = "X-formed Recordings:"
    self.XformedRecordings_Msg.position = (x, y)
    self.add_child(self.XformedRecordings_Msg)  
    

 
def display_noXformedRecordingsCreatedYet_Msg(self):
  # display the "error" message
  x = self.size[0]/2
  y = self.size[1] - 200
  state["noXformedRecordings_Msg"] = "displayed"
  self.noXformedRecordings_Msg = LabelNode()
  self.noXformedRecordings_Msg.color = "#ff0909"
  self.noXformedRecordings_Msg.font = ('Times New Roman', 40)
  self.noXformedRecordings_Msg.text = "No X-formed Recordings created yet."
  self.noXformedRecordings_Msg.position = (x, y)
  self.add_child(self.noXformedRecordings_Msg)

  
    
def displayXformedsRecordings(self, recordings, index, x, x_offset, y, y_offset):
  # name of file to be displayed
  self.XformedRecordings.append(LabelNode())
  self.XformedRecordings[index].font = ('American Typewriter', 15)
  self.XformedRecordings[index].text = recordings[index]
  self.XformedRecordings[index].color = "black"
  self.XformedRecordings[index].anchor_point = (0, 0.5) # lower left
  #self.XformedRecordings[index].anchor_point = (0.5, 0.5) # lower left
  self.XformedRecordings[index].position = (x + 7, y - y_offset)
   
  # the "container" around the filename for easy highlighting by the user
  self.XformedRecordingsOuter.append(SpriteNode('pzl:Button1'))
  self.XformedRecordingsOuter[index].anchor_point = (0, 0.5) # lower left
  (X, Y) = self.XformedRecordings[index].size
  self.XformedRecordingsOuter[index].size = (X + 15, Y)    
  self.XformedRecordingsOuter[index].position = (x, y - y_offset)    
  
  self.add_child(self.XformedRecordingsOuter[index]) 
  #self.XformedRecordingsOuter[index].add_child(self.XformedRecordings[index])
  self.add_child(self.XformedRecordings[index]) #text on top of "button"
 
    
          
def was_XformedRecordingsFileSelected(self, touch):
  orgRecOut = self.XformedRecordingsOuter
  
  for index in range(len(orgRecOut)): 
    # if file selected highlight it.
    if touch.location in orgRecOut[index].bbox:
      sound.play_effect('8ve:8ve-tap-double')
      if index == state["XformedRecSelectedIndex"]:
        return # same file has already been selected
      state["XformedRecPrevColor"] = orgRecOut[index].color
      orgRecOut[index].color = "yellow"
      state["XformedRecNewColor"] = orgRecOut[index].color
      orgRecOut[index].scale = 1.1
      (X, Y) = orgRecOut[index].position 
      orgRecOut[index].position = (X - 10, Y)
  
      # so I know which recording to play if the play button is selected.
      state["XformedRecSelectedIndex"] = index 
      state["XformedRecording"] = "selected"
      
      if state["noRecordingSelected_Msg"] == "displayed":
        display_XformedRecordings_Msg(self)      
      
      # if a file is selected make sure any previous selected file is unselected
      for index in range(len(orgRecOut)):
        if orgRecOut[index].color == state["XformedRecNewColor"] and \
           index != state["XformedRecSelectedIndex"]:
          orgRecOut[index].color = state["XformedRecPrevColor"]
          orgRecOut[index].scale = 1
          (X, Y) = orgRecOut[index].position 
          orgRecOut[index].position = (X + 10, Y)
          break      
          
      break
 
         
       
def display_XformedRecordings(self): 
  global state
  # return the wave files of the Xformed recordings that have been made so far.
  recordings = os.listdir(path2_transformedVoices)
  if len(recordings) == 0 :
    display_noXformedRecordingsCreatedYet_Msg(self)  
    return 
  
  display_XformedRecordings_Msg(self)      
  state["XformedRecordings"] = "displayed"
  self.XformedRecordings = list()
  self.XformedRecordingsOuter = list()
  x = 25
  x_offset = 0
  y = 520
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
    # passing the buck
    if x + (len(recordings[index]) * xFactor)  > 900:
      x = 25
      y_offset += 30
      
    displayXformedsRecordings(self, recordings, index, x, x_offset, y, y_offset)
    
    (X, Y) = self.XformedRecordingsOuter[index].size
    x += X + 15
      

    
            
# Singer Recordings Listing Logic ************************************************** 
def remove_singerRecordings(self):
  global state
  if state["singerRecordings_Msg"] == "displayed" :
    self.singerRecordings_Msg.remove_from_parent()
    state["singerRecordings_Msg"] = "notDisplayed"   
  else:
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"
    
  if state["singerRecordings"] == "displayed":
    
    state["singerRecordings"] = "notDisplayed"
    state["singerRecording"] = "notSelected"
    #state["previous_singerIndex"] = state["singerRecSelectedIndex"]
    #state["singerRecSelectedIndex"] = None
    for index in range(len(self.singerRecordingsOuter)):
      self.singerRecordingsOuter[index].remove_from_parent()
      self.singerRecordings[index].remove_from_parent()
      
    
                        
 
                    
def display_singerRecordings_Msg(self):  
  global state
  x = self.size[0]/2
  y = self.size[1] - 200
  
  if state["noRecordingSelected_Msg"] == "displayed" :
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"   
    
  if state["singerRecordings_Msg"] != "displayed":
    # display recordings listing message
    state["singerRecordings_Msg"] = "displayed"
    self.singerRecordings_Msg = LabelNode()
    self.singerRecordings_Msg.color = "#ff0909"
    self.singerRecordings_Msg.font = ('Papyrus', 40)
    self.singerRecordings_Msg.text = "Singers To Emulate:"
    self.singerRecordings_Msg.position = (x, y)
    self.add_child(self.singerRecordings_Msg)  
    

 
def display_noSingerRecordingsCreatedYet_Msg(self):
  # display the "error" message
  x = self.size[0]/2
  y = self.size[1] - 200
  state["noSingerRecordings_Msg"] =  "displayed"
  self.noSingerRecordings_Msg = LabelNode()
  self.noSingerRecordings_Msg.color = "#ff0909"
  self.noSingerRecordings_Msg.font = ('Times New Roman', 60)
  self.noSingerRecordings_Msg.text = "No Singer Recordings created yet."
  #self.noSingerRecordings.position = (self.size[0]/2, self.size[1]/2)
  self.noSingerRecordings_Msg.position = (x, y)
  self.add_child(self.noSingerRecordings_Msg)  

  
    
def displaySingersRecordings(self, recordings, index, x, x_offset, y, y_offset):
  # name of file to be displayed
  self.singerRecordings.append(LabelNode())
  self.singerRecordings[index].font = ('American Typewriter', 15)
  self.singerRecordings[index].text = recordings[index]
  self.singerRecordings[index].color = "black"
  self.singerRecordings[index].anchor_point = (0, 0.5) # lower left
  #self.singerRecordings[index].anchor_point = (0.5, 0.5) # lower left
  self.singerRecordings[index].position = (x + 7, y - y_offset)
   
  # the "container" around the filename for easy highlighting by the user
  self.singerRecordingsOuter.append(SpriteNode('pzl:Button1'))
  self.singerRecordingsOuter[index].anchor_point = (0, 0.5) # lower left
  (X, Y) = self.singerRecordings[index].size
  self.singerRecordingsOuter[index].size = (X + 15, Y)    
  self.singerRecordingsOuter[index].position = (x, y - y_offset)    
  
  self.add_child(self.singerRecordingsOuter[index]) 
  #self.singerRecordingsOuter[index].add_child(self.singerRecordings[index])
  self.add_child(self.singerRecordings[index]) #text on top of "button"
 
    
          
def was_singerRecordingsFileSelected(self, touch):
  orgRecOut = self.singerRecordingsOuter
  
  for index in range(len(orgRecOut)): 
    # if file selected highlight it.
    if touch.location in orgRecOut[index].bbox:
      sound.play_effect('8ve:8ve-tap-double')
      if index == state["singerRecSelectedIndex"]:
        return # same file has already been selected
      state["singerRecPrevColor"] = orgRecOut[index].color
      orgRecOut[index].color = "yellow"
      state["singerRecNewColor"] = orgRecOut[index].color
      orgRecOut[index].scale = 1.1
      (X, Y) = orgRecOut[index].position 
      orgRecOut[index].position = (X - 10, Y)
  
      # so I know which recording to play if the play button is selected.
      state["singerRecSelectedIndex"] = index 
      state["singerRecording"] = "selected"
      
      if state["noRecordingSelected_Msg"] == "displayed":
        display_singerRecordings_Msg(self)      
      
      # if a file is selected make sure any previous selected file is unselected
      for index in range(len(orgRecOut)):
        if orgRecOut[index].color == state["singerRecNewColor"] and \
           index != state["singerRecSelectedIndex"]:
          orgRecOut[index].color = state["singerRecPrevColor"]
          orgRecOut[index].scale = 1
          (X, Y) = orgRecOut[index].position 
          orgRecOut[index].position = (X + 10, Y)
          break      
          
      break
 
         
       
def display_singerRecordings(self): 
  global state
  # return the wave files of the singer recordings that have been made so far.
  recordings = os.listdir(path2_voices2emulate)
  if len(recordings) == 0 :
    display_noSingerRecordingsCreatedYet_Msg(self)  
    return 
  
  display_singerRecordings_Msg(self)      
  state["singerRecordings"] = "displayed"
  self.singerRecordings = list()
  self.singerRecordingsOuter = list()
  x = 25
  x_offset = 0
  y = 520
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
    # passing the buck
    if x + (len(recordings[index]) * xFactor)  > 900:
      x = 25
      y_offset += 30
      
    displaySingersRecordings(self, recordings, index, x, x_offset, y, y_offset)
    
    (X, Y) = self.singerRecordingsOuter[index].size
    x += X + 15
      
    

# XformIt Button Logic *************************************************************
def remove_XformingItButton(self):
  state["XformingItButton"] = "notDisplayed"
  self.XformingItButtonOuter.remove_from_parent()
  self.XformingItButton.remove_from_parent()
  self.XformingItButtonTitle.remove_from_parent()
     
  
def remove_XformItButton(self):
  state["XformItButton"] = "notDisplayed"
  self.XformItButtonOuter.remove_from_parent()
  self.XformItButton.remove_from_parent()
  self.XformItButtonTitle.remove_from_parent()

   
def display_XformItButton(self):
  state["XformItButton"] = "displayed"
  self.XformItButtonOuter = SpriteNode('emj:Black_Circle')
  self.XformItButtonOuter.scale = 2
  #self.XformItButtonOuter.position = (self.size[0]/2, self.size[1]/2)
  self.XformItButtonOuter.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.XformItButtonOuter)

  self.XformItButton = SpriteNode('iow:ios7_bolt_outline_32')
  self.XformItButton.position = (self.size[0]/2, self.size[1] - 125)
  self.add_child(self.XformItButton)
  
  self.XformItButtonTitle = LabelNode('Papyrus')
  self.XformItButtonTitle.text = "X-form"
  self.XformItButtonTitle.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.XformItButtonTitle) 

  
def display_XformingItButton(self):
  state["song"] = sound.Player('digital:Laser4')
  state["song"].play()
  state["XformingItButton"] = "displayed"
  self.XformingItButtonOuter = SpriteNode('emj:Black_Circle')
  self.XformingItButtonOuter.scale = 2.1
  self.XformingItButtonOuter.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.XformingItButtonOuter)

  self.XformingItButton = SpriteNode('shp:aura')
  self.XformingItButton.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.XformingItButton)
  
  self.XformingItButtonTitle = LabelNode('Hoefler Text')
  self.XformingItButtonTitle.text = "X-forming"
  self.XformingItButtonTitle.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.XformingItButtonTitle)
    
       
   

