
'''

   
This is the starting point of this program: Voice X-former (VX).

This program transforms ones voice to be as one desires.

i.e this program will be able to transform your "singing" voice into another singer's voice.

It also allows you to mathmatically manipulate sound at the individual sinewave level that combine to compose the sound.

It also produces self hypnosis (Dream Weaver) "tapes" using the user's own voice. 

Created by Charles C. Geeting
Created for Electric Universe, LLC
Created between 12/13/2017 and ...  (Version ?)
 
V. 0.0.1 Play a wave file. 01/01/2018
V. 0.0.2 Record a sound and create a wave file. 01/09/2018
V. 0.0.3 Create a GUI that allows you to: 
  1. list the wave files available to be played. 01/13/2018
  2. play a recording. 01/14/2018
  3. Make a recording. 01/15/2018
  4. View a waveform/recording in the time domain.
  
         pick a "Voice" recording to emulate,
         create a new transformed recording, etc...
  NOTE: gui sliders to control pan and pitch probably should be added
'''

# Needed imports *******************************************************************
import ui # To implement a GUI interface
import sound # to play sound files
import time # to shorten the length of certain sound effects
import os # to rename a file
import asyncio
# import wave # not sure yet what its capable of.

# Voice X-formation functions
from VXfunctions import voices2Emulate, originalVoices, XformedVoices, getWaveFile, determineFileName, playClickSound, waveViewTD


path2_originalVoices = './waveFiles/originalVoices/'
global_prevValues = {} # to store previous image values so that they may be reset

# global objects so that playing and recording won't stop when button func. returns
global_soundRecorderObj = sound.Recorder(path2_originalVoices + 'temporary.wav')
global_soundPlayerObj = None 

# GUI functions ********************************************************************

# NOTE v['whatever'] are ui.View type objects!!!!!
 

def textField_dataEntered(sender) :
  # want to get rid of keyboard at this point
  pass
  
   
# not working correctly, do not call
def restorePlayButton():
  while True:
    if global_soundPlayerObj.playing == False :
      v['waveFormView'].send_to_back()
      v['playButton'].title = "Play"
      v['playButton'].image = global_prevValues["playButton_image"]
      v['playButton'].background_color = global_prevValues['playButton_prevBkGrnd_color'] 
      break
    
      
  

 
def playButton_tapped(sender):
  # so sound will play when playButton_tapped function returns, if not a global it is destroyed otherwise, maybe using asyncio would get it to work too.
  global global_soundPlayerObj
  
  if sender.title == "Play":
    if len(v["recordingToPlay_or_Xform"].text) > 0 :
      file = getWaveFile(v["recordingToPlay_or_Xform"].text)
      if file == None: # file entered was not found.
        v['recordingsView'].text = "That file does not exist."
        sound.play_effect('game:Error')
      else: # file exists, so play it.
        playClickSound()
        
        sender.title = "Stop Play"
        global_prevValues["playButton_image"] = sender.image
        sender.image = ui.Image("iob:stop_24")
        
        global_prevValues["playButton_prevBkGrnd_color"] = sender.background_color
        sender.background_color = "#ff2b62"
        v["recordingToPlay_or_Xform"].text = file.split('/')[3]
        v['recordingsView'].text = v["recordingToPlay_or_Xform"].text + " being played"
        
        # create the waveform image from the sound file and display it (Time Domain)
        # pass the wave file to read, and the imageView area to display it in
        waveViewTD(file, v['waveFormView'])
        print("type:", type(v['waveFormView']))   
        
        global_soundPlayerObj = sound.Player(file)
        global_soundPlayerObj.play()
        #asyncio(restorePlayButton()) #does not work right
        
           
    else : # user has not entered a file to play yet.
      v['recordingsView'].text = "No file selected."
      sound.play_effect('game:Error')
  else: # sender.title == "Stop Play", so reset button to "Play" state
    v['waveFormView'].send_to_back()
      
    if global_soundPlayerObj.playing:
      global_soundPlayerObj.stop()
    
    playClickSound()
    
    sender.title = "Play"
    sender.image = global_prevValues["playButton_image"]
    sender.background_color = global_prevValues["playButton_prevBkGrnd_color"]
    v['recordingsView'].text = "" # clear text of what was previously playing.
    
       
             
def recordButton_tapped(sender):
  if sender.title == "Record":
    playClickSound()
    
    sender.title = "Stop Recording"
    
    global_prevValues["recordButton_prevBkGrnd_color"] = sender.background_color
    sender.background_color = "#ff2b62"
    global_soundRecorderObj.record()
  else:
    global_soundRecorderObj.stop() # stop first so key click not recorded
    playClickSound()
    
    # when recording has stopped rename the temporary file to a unique filename
    file = determineFileName() 
    path_file = path2_originalVoices + file
    os.rename('./waveFiles/originalVoices/temporary.wav', path_file)
    
    sender.title = "Record"
    sender.background_color = global_prevValues["recordButton_prevBkGrnd_color"]
 
 
 
def xButton_tapped(sender):
  playClickSound()
  if sender.title == "VX":
    sender.title = "V-Xing!"
    global_prevValues["xButton_prevBkGrnd_color"] = sender.background_color
    sender.background_color = "#2bacff"
  else:
    sender.title = "VX"
    sender.background_color = global_prevValues["xButton_prevBkGrnd_color"]


            
def listButton_tapped(sender):
  # List the  wave files in the various directories that are available.
  playClickSound()
  if sender.name == "listOriginalButton" :
    v['recordingsView'].text = originalVoices()
  elif sender.name == "listVoicesButton" :
    v['recordingsView'].text = voices2Emulate() 
  else :
    v['recordingsView'].text = XformedVoices()
  


v = ui.load_view('VXgui.pyui')
#v['xButton'].font = ("Times New Roman", 50) 
v.name = 'Voice X-former' # program title
v.background_color = "#e0e0e0" #(0.0, 1.0, 0.0, 1.0) # (r, g, b, alpha)
v.present('fullscreen')




