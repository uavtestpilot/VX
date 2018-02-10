import os, sound, time, wave, struct
from waveGenerator import waveGenerator
from scene import *
#from waveGeneratorOld import waveGeneratorOld

# for waveViewTD()
from PIL import Image
import ImageDraw
import ui

        
# To keep track of the state of the buttons, messages, files displayed...etc.
state = {"recordButton" : "notDisplayed", "stopRecordButton" : "notDisplayed", \
         "playButton" : "notDisplayed", "stopPlayButton" : "notDisplayed", \
         
         "originalsButton" : "notDisplayed", \
         "clearScreenOriginalsButton" : "notDisplayed", \
         "originalRecordings" : "notDisplayed", \
         "originalRecording" : "notSelected", \
         "originalRecSelectedIndex" : None, \
         "originalRecordings_Msg" : "notDisplayed", \
                  
         "singersButton" : "notDisplayed", \
         "clearScreenSingersButton" : "notDisplayed", \
         "singerRecordings" : "notDisplayed", \
         "singerRecording" : "notSelected", \
         "singerRecSelectedIndex" : None, \
         "singerRecordings_Msg" : "notDisplayed", \
                  
         "XformedButton" : "notDisplayed", \
         "clearScreenXformedButton" : "notDisplayed", \
         "XformedRecordings" : "notDisplayed", \
         "XformedRecording" : "notSelected", \
         "XformedRecSelectedIndex" : None, \
         "XformedRecordings_Msg" : "notDisplayed", \
         
         "noRecordingSelected_Msg" : "notDisplayed", \
         
         "song" : None}
         
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

record = sound.Recorder(path2_originalVoices + 'temporary.wav')

  
def recordButton(self): 
  global record
  # The "record" button actually consists of the record and stopRecord buttons
  if state["recordButton"] == "notDisplayed":
    display_recordButton(self)
    if state["stopRecordButton"] == "displayed":
      remove_stopRecordButton(self)
      if record.recording:
        record.stop()
        renameRecording()
  elif state["recordButton"] == "displayed":
    display_stopRecordButton(self)
    remove_recordButton(self)
    record.record()
    
 
   
def renameRecording():   
  # when recording has stopped rename the temporary file to a unique filename
  path_file = path2_originalVoices + time.asctime() + '.wav'
  print(path_file)
  os.rename('./waveFiles/originalVoices/temporary.wav', path_file)
    

    
def playButton(self):
  global song
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
    display_noRecordingSelected_Msg(self)
  

      
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
  
    
  
  
def displayButtons(self):
  """
  create and display all initial buttons on startup
  """
  playButton(self) # create and display the play button
  recordButton(self) # create and display the record button
  
  # create and display the list files buttons
  singersButton(self)
  XformedButton(self)
  originalsButton(self)
  
 
  
  
def getWaveFileData(waveFile):
  """
  # read the raw data from the wave file and return it.
  """
  
  # print out wave file info.
  print("\nwave file read:", waveFile)
  
  hand = wave.open(waveFile, "rb")

  print("parameters:", hand.getparams()) # display wave file parameters

  # get data all at once -10 TIMES FASTER THIS WAY!!!
  # but...(run into memory issues this way????)
  
  # YOU ARE HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  bytesObj = hand.readframes(hand.getnframes()) 
  
  # each bytesObj unpacked must have an associated "h"
  if hand.getnchannels() == 1:
    fmt = str(hand.getnframes()) + "h" 
  else:
    fmt = str(4*hand.getnframes()) + "h"
    
  data = struct.unpack(fmt, bytesObj)

  hand.close()  
  
  return data, hand.getnframes()

  
  
  

def waveViewTD(waveFile, uiImageView):
  
 
  data, numFrames = getWaveFileData(waveFile)
 
  print("\nraw data read from wave file:\n")
  print("data[0] =", data[0], "data[1] =", data[1], "data[2] =", data[2], "data[3] =", data[3], "data[4] =", data[4], "data[5] =", data[5],"...", "data[numFrames-3] =",data[numFrames-3], "data[numFrames-2] =", data[numFrames-2], "data[numFrames-1] =",data[numFrames-1])
  

  
  
  # now use the raw data to display the waveform(s)
  
  

  

  
  # create image of waveform for viewing and return it.

  #ui.ImageView.h
  im = Image.new("RGB", (int(uiImageView.width), int(uiImageView.height)), "#f6ff2b")
  draw = ImageDraw.Draw(im)
  draw.line((0, 0) + im.size, fill="black")
  draw.line((0, im.size[1], im.size[0], 0), fill=128)
  im.save("waveFormImage.png")
  uiImageView.image = ui.Image("waveFormImage.png")
  
  
  """
  width = 1012
  height = 596
  with ui.ImageContext(width, height) as ctx:
    rect = ui.Path.rounded_rect(0, 0, width, height, 10)
    ui.set_color('#f8ff55')
    rect.fill()
  
  
    ui.set_color('#000000')
    rect.line_width = 0
    #rect.set_line_dash([1, 0])
    rect.move_to(width/2,height/2)
    rect.line_width = 10
    rect.line_to(width, height/2)
    
    rect.stroke()
    
    img = ctx.get_image()  
 
  uiImageView.image = img
  """
  
  uiImageView.bring_to_front() # now make it visible

  
 
  
   

"""  
path = path2_originalVoices
freq = 200 # Hz
duration = (2 + .005/4) # seconds, 1 cycle in .005 sec. So 400 and 1/4 cyles
volume = 100 # percent
numChan = 1 # of channels (1: mono, 2: stereo)

file = waveGenerator(freq, duration, volume, numChan, path) # generate the wave file
image = None
waveViewTD(file, image) # now display its attributes and display it in the Time Domain
"""





 
  
     
      
  
def getWaveFile(file2find) :
  """
  return a valid wave file if it exists, return None otherwise.
  """
  
  # valid wave files that are available to be played (all directories)
  #fileList = os.listdir(path2_voices2emulate)
  #fileList += os.listdir(path2_originalVoices)
  #fileList += os.listdir(path2_transformedVoices)
       
  # add the .wav extension if user ommited it.
  if not file2find.endswith('.wav') :
    file2find = file2find + '.wav'
      
  if os.path.exists(path2_voices2emulate + file2find):
    return path2_voices2emulate + file2find
  elif os.path.exists(path2_originalVoices + file2find):
    return path2_originalVoices + file2find
  elif os.path.exists(path2_transformedVoices + file2find):
    return path2_transformedVoices + file2find  
  else:
    return None
 
    
     


# list recorded files to play or Xform *********************************************

def displayTitle(self, title):
  self.title = LabelNode('Georgia')
  self.title.text = title
  self.title.position = (self.size[0]/2, self.size[1] - 50)
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
  
 
  
# Singers 2 Emulate Button Logic *************************************************
def remove_clearScreenSingersButton(self):
  state["clearScreenSingersButton"] = "notDisplayed"
  self.clrSingersButtonOuter.remove_from_parent()
  self.clrSingersButton.remove_from_parent()
  self.clrSingersButtonTitle.remove_from_parent()

    
def remove_singersButton(self):
  state["singersButton"] = "notDisplayed"
  self.singersButtonOuter.remove_from_parent()
  self.singersButton.remove_from_parent()
  self.singersButtonTitle.remove_from_parent()
     
  
def display_singersButton(self): 
  state["singersButton"] = "displayed"
  self.singersButtonOuter = SpriteNode('pzl:Blue8')
  self.singersButtonOuter.position = (self.size[0]/2, self.size[1] - 100)
  self.singersButtonOuter.x_scale = 2
  self.add_child(self.singersButtonOuter)
  
  self.singersButton = SpriteNode('iob:ios7_folder_outline_32')
  self.singersButton.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.singersButton)
  
  self.singersButtonTitle = LabelNode('Hoefler Text')
  self.singersButtonTitle.text = "Singers to Emulate"
  self.singersButtonTitle.position = (self.size[0]/2, self.size[1] - 130)
  self.add_child(self.singersButtonTitle)
    
  
def display_clearScreenSingersButton(self):
  state["clearScreenSingersButton"] = "displayed"
  self.clrSingersButtonOuter = SpriteNode('pzl:PaddleRed')
  self.clrSingersButtonOuter.position = (self.size[0]/2, self.size[1] - 100)
  self.clrSingersButtonOuter.x_scale = 1.5
  self.add_child(self.clrSingersButtonOuter)
  
  self.clrSingersButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrSingersButton.position = (self.size[0]/2, self.size[1] - 100)
  self.add_child(self.clrSingersButton)
  
  self.clrSingersButtonTitle = LabelNode('Hoefler Text')
  self.clrSingersButtonTitle.text = "Clear Screen"
  self.clrSingersButtonTitle.position = (self.size[0]/2, self.size[1] - 130)
  self.add_child(self.clrSingersButtonTitle)
    

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
  state["stopRecordButton"] = "displayed"
  self.stopRecordButtonOuter = SpriteNode('pzl:Red8')
  self.stopRecordButtonOuter.position = (100, self.size[1] - 100)
  self.add_child(self.stopRecordButtonOuter)

  self.stopRecordButton = SpriteNode('iob:ios7_mic_off_24')
  self.stopRecordButton.position = (100, self.size[1] - 100)
  self.add_child(self.stopRecordButton)
  
  self.stopRecordButtonTitle = LabelNode('Hoefler Text')
  self.stopRecordButtonTitle.text = "STOP recording"
  self.stopRecordButtonTitle.position = (100, self.size[1] - 130)
  self.add_child(self.stopRecordButtonTitle)
   
  

def display_recordButton(self):
  state["recordButton"] = "displayed"
  self.recordButtonOuter = SpriteNode('pzl:Purple8')
  self.recordButtonOuter.position = (100, self.size[1] - 100)
  self.add_child(self.recordButtonOuter)

  self.recordButton = SpriteNode('iow:ios7_mic_24')
  self.recordButton.position = (100, self.size[1] - 100)
  self.add_child(self.recordButton)
  
  self.recordButtonTitle = LabelNode('Hoefler Text')
  self.recordButtonTitle.text = "record"
  self.recordButtonTitle.position = (100, self.size[1] - 130)
  self.add_child(self.recordButtonTitle) 
  

# Xformed Button Logic *************************************************************  
def remove_XformedButton(self):
  state["XformedButton"] = "notDisplayed"
  self.XformedButtonOuter.remove_from_parent()
  self.XformedButton.remove_from_parent()
  self.XformedButtonTitle.remove_from_parent()
        
  
def remove_clearScreenXformedButton(self):
  state["clearScreenXformedButton"] = "notDisplayed"
  self.clrXformedButtonOuter.remove_from_parent()
  self.clrXformedButton.remove_from_parent()
  self.clrXformedButtonTitle.remove_from_parent()
     
       
def display_clearScreenXformedButton(self):
  state["clearScreenXformedButton"] = "displayed"
  self.clrXformedButtonOuter = SpriteNode('pzl:PaddleRed')
  self.clrXformedButtonOuter.position = (self.size[0] - 275, self.size[1] - 100)
  self.clrXformedButtonOuter.x_scale = 1.5
  self.add_child(self.clrXformedButtonOuter)
  
  self.clrXformedButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrXformedButton.position = (self.size[0] - 275, self.size[1] - 100)
  self.add_child(self.clrXformedButton)
  
  self.clrXformedButtonTitle = LabelNode('Hoefler Text')
  self.clrXformedButtonTitle.text = "Clear Screen"
  self.clrXformedButtonTitle.position = (self.size[0] - 275, self.size[1] - 130)
  self.add_child(self.clrXformedButtonTitle)
 
    
def display_XformedButton(self):
  state["XformedButton"] = "displayed"
  self.XformedButtonOuter = SpriteNode('pzl:Blue8')
  self.XformedButtonOuter.position = (self.size[0] - 275, self.size[1] - 100)
  self.XformedButtonOuter.x_scale = 2
  self.add_child(self.XformedButtonOuter)
  
  self.XformedButton = SpriteNode('iob:ios7_folder_outline_32')
  self.XformedButton.position = (self.size[0] - 275, self.size[1] - 100)
  self.add_child(self.XformedButton)
  
  self.XformedButtonTitle = LabelNode('Hoefler Text')
  self.XformedButtonTitle.text = "X-formed Recordings"
  self.XformedButtonTitle.position = (self.size[0] - 275, self.size[1] - 130)
  self.add_child(self.XformedButtonTitle) 
   
    
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
  state["playButton"] = "displayed"
  self.playButtonOuter = SpriteNode('pzl:Purple8')
  self.playButtonOuter.position = (self.size[0] - 100, self.size[1] - 100)
  self.add_child(self.playButtonOuter)

  self.playButton = SpriteNode('iow:arrow_right_b_24')
  self.playButton.position = (self.size[0] - 100, self.size[1] - 100)
  self.add_child(self.playButton)
  
  self.playButtonTitle = LabelNode('Hoefler Text')
  self.playButtonTitle.text = "play"
  self.playButtonTitle.position = (self.size[0] - 100, self.size[1] - 130)
  self.add_child(self.playButtonTitle) 

  
def display_stopPlayButton(self):
  state["stopPlayButton"] = "displayed"
  self.stopPlayButtonOuter = SpriteNode('pzl:Red8')
  self.stopPlayButtonOuter.position = (self.size[0] - 100, self.size[1] - 100)
  self.add_child(self.stopPlayButtonOuter)

  self.stopPlayButton = SpriteNode('iob:stop_24')
  self.stopPlayButton.position = (self.size[0] - 100, self.size[1] - 100)
  self.add_child(self.stopPlayButton)
  
  self.stopPlayButtonTitle = LabelNode('Hoefler Text')
  self.stopPlayButtonTitle.text = "STOP playing"
  self.stopPlayButtonTitle.position = (self.size[0] - 100, self.size[1] - 130)
  self.add_child(self.stopPlayButtonTitle)


# Original Recordings Button Logic ************************************************* 
def remove_originalsButton(self):
  state["originalsButton"] = "notDisplayed"
  self.originalsButtonOuter.remove_from_parent()
  self.originalsButton.remove_from_parent()
  self.originalsButtonTitle.remove_from_parent()
    
        
def remove_clearScreenOriginalsButton(self): 
  state["clearScreenOriginalsButton"] = "notDisplayed"
  self.clrOriginalsButtonOuter.remove_from_parent()
  self.clrOriginalsButton.remove_from_parent()
  self.clrOriginalsButtonTitle.remove_from_parent()
          
  
def display_originalsButton(self):
  state["originalsButton"] = "displayed"
  self.originalsButtonOuter = SpriteNode('pzl:Blue8')
  self.originalsButtonOuter.position = (275, self.size[1] - 100)
  self.originalsButtonOuter.x_scale = 2
  self.add_child(self.originalsButtonOuter)
  
  self.originalsButton = SpriteNode('iob:ios7_folder_outline_32')
  self.originalsButton.position = (275, self.size[1] - 100)
  self.add_child(self.originalsButton)
  
  self.originalsButtonTitle = LabelNode('Hoefler Text')
  self.originalsButtonTitle.text = "Original recordings"
  self.originalsButtonTitle.position = (275, self.size[1] - 130)
  self.add_child(self.originalsButtonTitle) 
           
    
def display_clearScreenOriginalsButton(self):
  state["clearScreenOriginalsButton"] = "displayed"
  self.clrOriginalsButtonOuter = SpriteNode('pzl:PaddleRed')
  self.clrOriginalsButtonOuter.position = (275, self.size[1] - 100)
  self.clrOriginalsButtonOuter.x_scale = 1.5
  self.add_child(self.clrOriginalsButtonOuter)
  
  self.clrOriginalsButton = SpriteNode('iob:ios7_folder_outline_32')
  self.clrOriginalsButton.position = (275, self.size[1] - 100)
  self.add_child(self.clrOriginalsButton)
   
  self.clrOriginalsButtonTitle = LabelNode('Hoefler Text')
  self.clrOriginalsButtonTitle.text = "Clear Screen"
  self.clrOriginalsButtonTitle.position = (275, self.size[1] - 130)
  self.add_child(self.clrOriginalsButtonTitle) 



# Listing Logic common to all ******************************************************
def display_noRecordingSelected_Msg(self):
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
  
  if state["noRecordingSelected_Msg"] != "displayed" :
    # display error message 
    state["noRecordingSelected_Msg"] = "displayed"
    self.noRecordingSelected_Msg = LabelNode()
    self.noRecordingSelected_Msg.color = "#000000"
    self.noRecordingSelected_Msg.font = ('Symbol', 40)
    self.noRecordingSelected_Msg.text = "-- No Recording Selected To Be Played --"
    self.noRecordingSelected_Msg.position = (self.size[0]/2, 575)
    self.add_child(self.noRecordingSelected_Msg) 
 
       
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
    state["originalRecSelectedIndex"] = None
    for index in range(len(self.originalRecordingsOuter)):
      self.originalRecordingsOuter[index].remove_from_parent()
      self.originalRecordings[index].remove_from_parent()
                        
 
                    
def display_originalRecordings_Msg(self):  
  global state
  
  if state["noRecordingSelected_Msg"] == "displayed" :
    self.noRecordingSelected_Msg.remove_from_parent()
    state["noRecordingSelected_Msg"] = "notDisplayed"   
    
  if state["originalRecordings_Msg"] != "displayed":
    # display recordings listing message
    state["originalRecordings_Msg"] = "displayed"
    self.originalRecordings_Msg = LabelNode()
    self.originalRecordings_Msg.color = "#ff0909"
    self.originalRecordings_Msg.font = ('Papyrus', 40)
    self.originalRecordings_Msg.text = "Original Recordings:"
    self.originalRecordings_Msg.position = (self.size[0]/2, 575)
    self.add_child(self.originalRecordings_Msg)  
    

 
def display_noOriginalRecordingsCreatedYet_Msg(self):
  # display the "error" message
  self.noOriginalRecordings = LabelNode()
  self.noOriginalRecordings.color = "#ff0909"
  self.noOriginalRecordings.font = ('Times New Roman', 60)
  self.noOriginalRecordings.text = "No Original Recordings have been created yet."
  self.noOriginalRecordings.position = (self.size[0]/2, self.size[1]/2)
  self.add_child(self.noOriginalRecordings)  

  
    
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
  self.originalRecordingsOuter[index].anchor_point = (0, 0.5) # lower left
  (X, Y) = self.originalRecordings[index].size
  self.originalRecordingsOuter[index].size = (X + 15, Y)    
  self.originalRecordingsOuter[index].position = (x, y - y_offset)    
  
  self.add_child(self.originalRecordingsOuter[index]) 
  #self.originalRecordingsOuter[index].add_child(self.originalRecordings[index])
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
  y = 525
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
    # passing the buck
    if x + (len(recordings[index]) * xFactor)  > 1000:
      x = 25
      y_offset += 30
            
    displayOriginalsRecordings(self, recordings, index, x, x_offset, y, y_offset)
      
    x += (len(recordings[index]) * xFactor)

        
    
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
    self.XformedRecordings_Msg.position = (self.size[0]/2, 575)
    self.add_child(self.XformedRecordings_Msg)  
    

 
def display_noXformedRecordingsCreatedYet_Msg(self):
  # display the "error" message
  self.noXformedRecordings = LabelNode()
  self.noXformedRecordings.color = "#ff0909"
  self.noXformedRecordings.font = ('Times New Roman', 60)
  self.noXformedRecordings.text = "No Xformed Recordings have been created yet."
  self.noXformedRecordings.position = (self.size[0]/2, self.size[1]/2)
  self.add_child(self.noXformedRecordings)  

  
    
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
  y = 525
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
    # passing the buck
    if x + (len(recordings[index]) * xFactor)  > 1000:
      x = 25
      y_offset += 30
      
    displayXformedsRecordings(self, recordings, index, x, x_offset, y, y_offset)
      
    x += (len(recordings[index]) * xFactor)

    
            
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
    state["singerRecSelectedIndex"] = None
    for index in range(len(self.singerRecordingsOuter)):
      self.singerRecordingsOuter[index].remove_from_parent()
      self.singerRecordings[index].remove_from_parent()
                        
 
                    
def display_singerRecordings_Msg(self):  
  global state
  
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
    self.singerRecordings_Msg.position = (self.size[0]/2, 575)
    self.add_child(self.singerRecordings_Msg)  
    

 
def display_noSingerRecordingsCreatedYet_Msg(self):
  # display the "error" message
  self.noSingerRecordings = LabelNode()
  self.noSingerRecordings.color = "#ff0909"
  self.noSingerRecordings.font = ('Times New Roman', 60)
  self.noSingerRecordings.text = "No Singer Recordings have been created yet."
  self.noSingerRecordings.position = (self.size[0]/2, self.size[1]/2)
  self.add_child(self.noSingerRecordings)  

  
    
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
  y = 525
  y_offset = 0
  xFactor = 12
  
  for index in range(len(recordings)):
    # passing the buck
    if x + (len(recordings[index]) * xFactor)  > 1000:
      x = 25
      y_offset += 30
      
    displaySingersRecordings(self, recordings, index, x, x_offset, y, y_offset)
      
    x += (len(recordings[index]) * xFactor)
    
    
       
   

