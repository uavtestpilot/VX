import os, sound, time

# for waveViewTD()
from PIL import Image
import ImageDraw

path2_voices2emulate = './waveFiles/voices2emulate/'
path2_transformedVoices = './waveFiles/transformedVoices/'
path2_originalVoices = './waveFiles/originalVoices/'



def waveViewTD(waveFile):
  im = Image.new("RGB", (512, 512), "white")
  draw = ImageDraw.Draw(im)
  draw.line((0, 0) + im.size, fill=128)
  draw.line((0, im.size[1], im.size[0], 0), fill=128)
  #draw.text("hello")
  del draw 
  
  im.save("waveFormImage.png")
  #im.show()
  


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
  myTime = time.localtime()
  
  file = "recording_" + str(myTime[1]) + "_" + str(myTime[2]) + "_" + str(myTime[0]) + "_time_" + str(myTime[3]) + ":" + str(myTime[4]) + ":" + str(myTime[5]) + ".wav"
  
  return file
  
  

  


           
      
  

