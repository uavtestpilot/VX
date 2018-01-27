
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
  
         view a recording, pick a "Voice" recording to emulate,
         create a new transformed recording, etc...
  NOTE: gui sliders to control pan and pitch probably should be added
'''

# Needed imports *******************************************************************
import ui # To implement a GUI interface
import sound # to play sound files
import time # to shorten the length of certain sound effects
import os # to rename a file

# import wave # not sure yet what its capable of.

# Voice X-formation functions
from VXfunctions import voices2Emulate, originalVoices, XformedVoices, getWaveFile, determineFileName, playClickSound, waveViewTD


path2_originalVoices = './waveFiles/originalVoices/'
global_buttonColor = {} # to store previous button color so that it may be reset
# global record object so that recording doesn't stop when button function returns
global_soundRecorderObj = sound.Recorder(path2_originalVoices + 'temporary.wav')

# GUI functions ********************************************************************

# NOTE v['whatever'] are ui.View type objects!!!!!
 
"""
def textField_dataEntered(sender) :
  # want to get rid of keyboard
  ui.KEYBOARD_ASCII = 1
  print(ui.KEYBOARD_DEFAULT)
  print(ui.KEYBOARD_ASCII) # 1
  print("text entered")
  print(ui.KEYBOARD_NAME_PHONE_PAD)
"""
 
def playButton_tapped(sender):
  if sender.title == "Play":
    if len(v["recordingToPlay_or_Xform"].text) > 0 :
      file = getWaveFile(v["recordingToPlay_or_Xform"].text)
      if file == None: # file entered was not found.
        v['recordingsView'].text = "That file does not exist."
        sound.play_effect('game:Error')
      else: # file exists, so play it.
        playClickSound()
        
        sender.title = "Stop Play"
        global_buttonColor["playButton_prevBkGrnd_color"] = sender.background_color
        sender.background_color = "#ff2b62"
        v["recordingToPlay_or_Xform"].text = file.split('/')[3]
        v['recordingsView'].text = v["recordingToPlay_or_Xform"].text + " being played"
        
        waveViewTD(file) # create an image of the waveform being played
    
        v['waveFormView'].image = ui.Image("waveFormImage.png")
        v['waveFormView'].bring_to_front()
        
        
        # slider comtrol for these values???
        #pan... -1 left ear, 0 both ears, 1 right ear
        
        sound.play_effect(file, volume=2.0, pitch=1.0, pan=0.0, looping=False)   
        soundPlayerObj = sound.Player(file)
        global_buttonColor["playingNowDuration"] = soundPlayerObj.duration
        print(global_buttonColor["playingNowDuration"])
      
     
    else : # user has not entered a file to play yet.
      v['recordingsView'].text = "No file selected."
      sound.play_effect('game:Error')
  else: # sender.title == "Stop Play", so reset button to "Play" state
    v['waveFormView'].send_to_back()
    
    
    sound.stop_all_effects() # stop the main recording being played
    
    playClickSound()
    
    sender.title = "Play"
    sender.background_color = global_buttonColor["playButton_prevBkGrnd_color"]
    v['recordingsView'].text = "" # clear text of what was previously playing.
    
       
             
def recordButton_tapped(sender):
  if sender.title == "Record":
    playClickSound()
    
    sender.title = "Stop Recording"
    
    #v['recordButton'].image = ui.Image("iob:close_24")
    # to use this must save prev. image to restore!
    
    global_buttonColor["recordButton_prevBkGrnd_color"] = sender.background_color
    sender.background_color = "#ff2b62"
    global_soundRecorderObj.record()
  else:
    global_soundRecorderObj.stop() # stop first so key click not recorded
    playClickSound()
    
    # when recording has stopped rename the temporary file to a unique filename
    # this function needs work, so that 1_7_2018...etc is returned as 01_07_2018
    # so that files are sorted correctly when displayed.
    file = determineFileName() 
    path_file = path2_originalVoices + file
    os.rename('./waveFiles/originalVoices/temporary.wav', path_file)
    
    sender.title = "Record"
    sender.background_color = global_buttonColor["recordButton_prevBkGrnd_color"]
 
 
 
def xButton_tapped(sender):
  playClickSound()
  if sender.title == "VX":
    sender.title = "V-Xing!"
    global_buttonColor["xButton_prevBkGrnd_color"] = sender.background_color
    sender.background_color = "#2bacff"
  else:
    sender.title = "VX"
    sender.background_color = global_buttonColor["xButton_prevBkGrnd_color"]


            
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



