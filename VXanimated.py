'''

   
This is the starting point of this program: Voice X-former (VX).

This program transforms ones voice to be as one desires.

i.e this program will be able to transform your "singing" voice into another singer's voice.

It also allows you to mathmatically manipulate sound at the individual sinewave level that combine to compose the sound.

It also produces self hypnosis (Dream Weaver) "tapes" using the user's own voice. 

Created by Charles C. Geeting
Created for Electric Universe, LLC
Created between 12/13/2017 and ...  (Version ?)

 # ********************************************************************************* 
V. 0.0.1 Play a wave file. 01/01/2018
V. 0.0.2 Record a sound and create a wave file. 01/09/2018
V. 0.0.3 Create a GUI that allows you to: 
  1. list the wave files available to be played. 01/13/2018 
  2. play a recording. 01/14/2018
  3. Make a recording. 01/15/2018
  
  To do...
  4. View a waveform/recording in the time domain  
         pick a "Voice" recording to emulate,
         create a new transformed recording, etc...
  NOTE: gui sliders to control pan and pitch probably should be added

  
    
# **********************************************************************************       
Redo!...decided to use the scene class to create a more visually pleasing gui
so VXgui.py replaced with VXanimated.py, VXgui.pyui no longer needed.

V. 0.0.1 Initial screen populated with the play and record buttons, and the 
         file listing buttons. 02/01/2018
  
'''

from scene import *
import sound, random, math

# Voice X-formation functions
from VXfunctions import singerRecordings, XformedRecordings, getWaveFile, determineFileName, playClickSound, waveViewTD, displayTitle, displaySunburstSprite, displayButtons, moveSprite, displayAlternateButtons

A = Action

  
class MyScene (Scene):
   
  def setup(self):
      
    self.background_color = "#1226ff" # set background to a cool blue
    
    displaySunburstSprite(self) # display a neat sprite to play around with
    
    displayTitle(self, "Voice X-former") # display program title
    
    # display initial control buttons (record, play, list, display, Xform)
    displayButtons(self)
    
       
    
  
  def did_change_size(self):
    pass
  
  
  
  def update(self):
    pass
  
  
  
  def touch_began(self, touch):
    
    moveSprite(self, touch)
  
    displayAlternateButtons(self, touch) # IF button touched play click sound
    # and display the alternate button symbol, e.g. play -> STOP play and visa versa
   
    
    
       
  
  def touch_moved(self, touch):
    pass
  
  
  
  def touch_ended(self, touch):
    pass



if __name__ == '__main__':
  run(MyScene(), show_fps=True)
