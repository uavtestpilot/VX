import os, sound, time, wave, struct
from waveGenerator import waveGenerator
#from waveGeneratorOld import waveGeneratorOld

# for waveViewTD()
from PIL import Image
import ImageDraw
import ui

path2_voices2emulate = './waveFiles/voices2emulate/'
path2_transformedVoices = './waveFiles/transformedVoices/'
path2_originalVoices = './waveFiles/originalVoices/'

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
  """
  im = Image.new("RGB", (1012, 596), "white")
  draw = ImageDraw.Draw(im)
  draw.line((0, 0) + im.size, fill=128)
  draw.line((0, im.size[1], im.size[0], 0), fill=128)
  im.save("waveFormImage.png")
  uiImageView.image = ui.Image("waveFormImage.png")
  
  """
  width = 1012
  height = 596
  with ui.ImageContext(1012, 596) as ctx:
    #rect = ui.Path.rounded_rect(x, y, width, height, 10)
    oval = ui.Path.oval(width/2, height/2, 100, 100)
    ui.set_color('red')
    oval.fill()
    #ui.Path.stroke()
    img = ctx.get_image()
 
  uiImageView.image = img
  
  
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



def playClickSound():
  sound.play_effect('game:Click_2')
  time.sleep(0.05)
  sound.stop_all_effects()
 
  
    
  
def voices2Emulate() :
  """"
  return the wave files of the Voices To Emulate that are available.
  """
  
  fileList = os.listdir(path2_voices2emulate)
  
  fileString = "'Voices' to emulate:\n\n"
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
  
 
  
def XformedVoices() :
  """
  return the wave files of your recordings that have been X-formed.
  """
  
  fileString = "Original recordings that have been X-formed:\n\n"
  fileList = os.listdir(path2_transformedVoices)
  if len(fileList) == 0 :
    fileString += "No voice transformations have been created yet."
    return fileString
    
  for file in fileList:
    fileString += file + "\n"
  
  return fileString

  
      
  
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
  
  

  


           
      
  

