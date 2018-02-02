import os, sound, time, wave, struct
from waveGenerator import waveGenerator
from scene import *
#from waveGeneratorOld import waveGeneratorOld

# for waveViewTD()
from PIL import Image
import ImageDraw
import ui

# To keep track of the state of the buttons
g_altButton = {"playButton" : 0, "recordButton" : 0, "originalsButton" : 0, "originalRecordings" : 0, "singersButton" : 0, "XformedButton" : 0}




# paths (directories) to store the wave files created
path2_voices2emulate = './waveFiles/voices2emulate/'
path2_transformedVoices = './waveFiles/transformedVoices/'
path2_originalVoices = './waveFiles/originalVoices/'


 
def recordButton(self): 
  remove_stopRecordButton(self)
  display_recordButton(self)
  
  
def stopRecordButton(self): 
  remove_recordButton(self)
  display_stopRecordButton(self)
 
 
def originalsButton(self):
  remove_clearScreenOriginalsButton(self)
  remove_originalRecordings(self)
  display_originalsButton(self)
 
       
def clearScreenOriginalsButton(self):  
  remove_originalsButton(self)
  display_originalRecordings(self)
  display_clearScreenOriginalsButton(self)


def singersButton(self):
  remove_clearScreenSingersButton(self)
  display_singersButton(self)
  

def clearScreenSingersButton(self):  
  remove_singersButton(self)
  #display_singers2Emulate(self)
  display_clearScreenSingersButton(self)
  
    
def XformedButton(self):
  remove_clearScreenXformedButton(self)
  display_XformedButton(self)

    
def clearScreenXformedButton(self):  
  remove_XformedButton(self)
  #display_XformedRecordings(self)
  display_clearScreenXformedButton(self)
  
      
def playButton(self):
  remove_stopPlayButton(self)
  display_playButton(self)
  
  
def stopPlayButton(self):
  remove_playButton(self)
  display_stopPlayButton(self)


     
def displayAlternateButtons(self, touch):
  """
  play the click sound if a button has been touched, and then display the 
  buttons alternate
  """
  if touch.location in self.playButtonOuter.bbox:
    playClickSound() 
    
    if g_altButton["playButton"] == 0 or g_altButton["playButton"] == 2:
      stopPlayButton(self)
    else:
      playButton(self)
      
  elif touch.location in self.recordButtonOuter.bbox:
    playClickSound() 
    
    if g_altButton["recordButton"] == 0 or  g_altButton["recordButton"] == 2:
      stopRecordButton(self)
    else:
      recordButton(self)
      
  elif touch.location in self.originalsButtonOuter.bbox:
    playClickSound() 
    
    if g_altButton["originalsButton"] == 0 or  g_altButton["originalsButton"] == 2:
      clearScreenOriginalsButton(self)
    else:
      originalsButton(self)
      
  elif touch.location in self.singersButtonOuter.bbox:
    playClickSound() 
    
    if g_altButton["singersButton"] == 0 or  g_altButton["singersButton"] == 2:
      clearScreenSingersButton(self)
    else:
      singersButton(self)
      
  elif touch.location in self.XformedButtonOuter.bbox:
    playClickSound() 
    
    if g_altButton["XformedButton"] == 0 or  g_altButton["XformedButton"] == 2:
      clearScreenXformedButton(self)
    else:
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
 
  
   
     
def determineFileName():
  """
  returns a logical unused fileName to be used for this recording
  """
  myTime = time.localtime() # get local date and time
  
  # prefix info. with a 0 if not a 2 digit number for sorting/display
  if len(str(myTime[1])) == 1:
    myTimeMonth = "0" + str(myTime[1])
  else:
    myTimeMonth = str(myTime[1])
    
  if len(str(myTime[2])) == 1:
    myTimeDay = "0" + str(myTime[2])
  else:
    myTimeDay = str(myTime[2])
    
  if len(str(myTime[3])) == 1:
    myTimeHours = "0" + str(myTime[3])
  else:
    myTimeHours = str(myTime[3])
    
  if len(str(myTime[4])) == 1:
    myTimeMinutes = "0" + str(myTime[4])
  else:
    myTimeMinutes = str(myTime[4])
    
  if len(str(myTime[5])) == 1:
    myTimeSeconds = "0" + str(myTime[5])
  else:
    myTimeSeconds = str(myTime[5])
  
  # now use date and time to create a unique file name.
  file = "recording_" + myTimeMonth + "_" + myTimeDay + "_" + str(myTime[0]) + "_time_" + myTimeHours + ":" + myTimeMinutes + ":" + myTimeSeconds + ".wav"
  
  return file

# list recorded files to play or Xform *********************************************

def singerRecordings() :
  """"
  return the wave files of singer recordings that are available.
  """
  
  fileList = os.listdir(path2_voices2emulate)
  
  fileString = "Singer to emulate recordings:\n\n"
  for file in fileList:
    fileString += file + "\n"
    
  return fileString

  
def originalVoices() :
  """
  return the wave files of the original recordings that have been made so far.
  """
   
  fileList = os.listdir(path2_originalVoices)
  
  fileString = "Original recordings:\n\n"
  for file in fileList:
    fileString += file + "\n"
    
  return fileString
  
  
  
def XformedRecordings() :
  """
  return the wave files of recordings that have been X-formed.
  """
  
  fileString = "X-formed recordings:\n\n"
  fileList = os.listdir(path2_transformedVoices)
  if len(fileList) == 0 :
    fileString += "No Xformations have been created yet."
    return fileString
    
  for file in fileList:
    fileString += file + "\n"
  
  return fileString


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
  

# **********************************************************************************                     
def playClickSound():
  """
  makes the click sound for the buttons when they are touched
  """
  sound.play_effect('game:Click_2')
  time.sleep(0.05)
  sound.stop_all_effects()
 
  
# Singers 2 Emulate Button Logic *************************************************
def remove_clearScreenSingersButton(self):
   # can't remove clear screen button on initialization if it does not exist yet.
  if g_altButton["singersButton"] == 1:
    self.clrSingersButtonOuter.remove_from_parent()
    self.clrSingersButton.remove_from_parent()
    self.clrSingersButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["singersButton"] = 2  


    
def remove_singersButton(self):
  self.singersButtonOuter.remove_from_parent()
  self.singersButton.remove_from_parent()
  self.singersButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["singersButton"] = 1
      
  
def display_singersButton(self): 
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
  
  
  
# Original Recordings Button Logic ************************************************* 
def remove_originalsButton(self):
  self.originalsButtonOuter.remove_from_parent()
  self.originalsButton.remove_from_parent()
  self.originalsButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["originalsButton"] = 1

        
def remove_clearScreenOriginalsButton(self): 
  # can't remove clear screen button on initialization if it does not exist yet.
  if g_altButton["originalsButton"] == 1:
    self.clrOriginalsButtonOuter.remove_from_parent()
    self.clrOriginalsButton.remove_from_parent()
    self.clrOriginalsButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["originalsButton"] = 2  
    
  
  
def display_originalsButton(self):
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


# Record Button Logic **************************************************************
def remove_recordButton(self):
  self.recordButtonOuter.remove_from_parent()
  self.recordButton.remove_from_parent()
  self.recordButtonTitle.remove_from_parent()
  
  # to signify record button to be called next time
  g_altButton["recordButton"] = 1
  
  
  
def remove_stopRecordButton(self):
  # can't remove stop record button on initialization if it does not exist yet.
  if g_altButton["recordButton"] == 1:
    self.stopRecordButtonOuter.remove_from_parent()
    self.stopRecordButton.remove_from_parent()
    self.stopRecordButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["recordButton"] = 2    
         
         
         
def display_stopRecordButton(self):
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
  self.XformedButtonOuter.remove_from_parent()
  self.XformedButton.remove_from_parent()
  self.XformedButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["XformedButton"] = 1
 
       
  
def remove_clearScreenXformedButton(self):
  # can't remove clear screen button on initialization if it does not exist yet.
  if g_altButton["XformedButton"] == 1:
    self.clrXformedButtonOuter.remove_from_parent()
    self.clrXformedButton.remove_from_parent()
    self.clrXformedButtonTitle.remove_from_parent()
    
  # to signify alternate button to be called next time
  g_altButton["XformedButton"] = 2  
  
 
       
def display_clearScreenXformedButton(self):
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
  # can't remove stop play button on initialization if it does not exist yet.
  if g_altButton["playButton"] == 1:
    self.stopPlayButtonOuter.remove_from_parent()
    self.stopPlayButton.remove_from_parent()
    self.stopPlayButtonTitle.remove_from_parent()
    
  # to signify stop play button to be called next time
  g_altButton["playButton"] = 2  
  
  
def remove_playButton(self):
  self.playButtonOuter.remove_from_parent()
  self.playButton.remove_from_parent()
  self.playButtonTitle.remove_from_parent()
  
  # to signify play button to be called next time
  g_altButton["playButton"] = 1
  
  
  
def display_playButton(self):
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


# Original Recordings Listing Logic ************************************************
  
  
def remove_originalRecordings(self):
  # can't remove anything on initialization since it does not exist yet.
  if g_altButton["originalRecordings"] == 1:
    self.originalRecordingsTitle.remove_from_parent()
    for index in range(len(self.originalRecordingsOuter)):
      self.originalRecordingsOuter[index].remove_from_parent()
      self.originalRecordings[index].remove_from_parent()
      
      
def display_originalRecordingsTitle(self):  
  # display listing title 
  self.originalRecordingsTitle = LabelNode()
  self.originalRecordingsTitle.color = "#ff0909"
  self.originalRecordingsTitle.font = ('Papyrus', 40)
  self.originalRecordingsTitle.text = "Original Recordings:"
  self.originalRecordingsTitle.position = (self.size[0]/2, 575)
  self.add_child(self.originalRecordingsTitle)  

 
def display_noOriginalRecordingsCreatedYet(self):
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
  
  return self.originalRecordingsOuter
    
 
 
       
def display_originalRecordings(self):
  # so the remove_originalRecordings function knows it has something to remove
  g_altButton["originalRecordings"] = 1 
  
  display_originalRecordingsTitle(self)  
  
  # return the wave files of the original recordings that have been made so far.
  recordings = os.listdir(path2_originalVoices)
  if len(recordings) == 0 :
    display_noOriginalRecordingsCreatedYet(self)  
    return 
    
  
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
    
    
  
   
    
  

  
  

