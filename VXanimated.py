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
  

V. 0.0.4 Used the scene class to create a more visually pleasing gui.
         VXgui.py replaced with VXanimated.py.
         VXgui.pyui no longer needed.
         Initial screen populated with the play and record buttons, and the file listing buttons. Above functionality will need to redone. 02/01/2018
         
  1. list the wave files available to be played. 02/07/2018 
  2. play a recording. 02/07/2018
  3. Make a recording. 02/08/2018
  4. Created a cool X-form "button" 02/09/2018
  5. Now able to access the two selected files from my X-form button. 02/10/2018
     Added more error checking, and the displaying of error messages.
     Re-arranged the button layout.
     
V. 0.0.5 Renamed VXfunctions to VXbuttons, created a new VXfunctions  02/11/2018
         to handle the sound transformation.
  1. 02/12/2108: stereo files now converted to mono before X-formation processing to
     keep things simple! 
  2. Temporary working directory created.  02/14/2018
     Generation and playing of a new Xformed wave file seems to be reliable now...
     at least for a few seconds duration...may have to modify for longer recordings.
     
 
   
 
         
TODO ...............................................................................
Begin exploring various filtering techniques and fourier math concepts in sound manipulation, may need to use some ML technique.

View a waveform/recording in the time domain.

listing of recordings could be better

need and "x" through the "clear screen" buttons.
'''

from scene import *
import sound, random, math

# The buttons and associated logic for them.
from VXbuttons import *
#from VXfunctions import *

"""
 singerRecordings, XformedRecordings, getWaveFile, determineFileName, playClickSound, waveViewTD, displayTitle, displaySunburstSprite, displayButtons, moveSprite, displayAlternateButtons, g_altButton, was_originalRecordingsFileSelected
"""

A = Action
  
class MyScene(Scene):
   
  
  
  def setup(self):
          
    self.background_color = "#1226ff" # set background to a cool blue
    
    displaySunburstSprite(self) # display a neat sprite to play around with
    
    displayTitle(self, "    Voice        X-former") # display program title
    
    # display initial control buttons (record, play, list, display, Xform)
    displayButtons(self)
    
              
    
  
  def did_change_size(self):
    pass
  
  
  
  def update(self):
    if state["stopPlayButton"] == "displayed" and state["song"].playing == False:
      playButton(self) # remove the stopPlay Button and display the Play button
        
    if state["XformingItButton"] == "displayed" and state["song"].playing == False:
      # remove the XformingIt Button and display the Xform button
      XformItButton(self)
      # now play the transformed wave file if it exists
      if state["XformedRecSound"] != None:
        state["XformedRecSound"].play()
      
    
  
  
  
  def touch_began(self, touch):   
    moveSprite(self, touch)# for my amusement
  
    displayAlternateButtons(self, touch) # IF button touched play click sound
    # and display the alternate button symbol, e.g. play -> STOP play and visa versa
    
    if state["originalRecordings"] == "displayed":
      was_originalRecordingsFileSelected(self, touch) # highlight recording if so.
    elif state["singerRecordings"] == "displayed":
      was_singerRecordingsFileSelected(self, touch) # highlight recording if so.
    elif state["XformedRecordings"] == "displayed":
      was_XformedRecordingsFileSelected(self, touch) # highlight recording if so.
    
   
    
    
       
  
  def touch_moved(self, touch):
    pass
  
  
  
  def touch_ended(self, touch):
    pass



if __name__ == '__main__':
  run(MyScene(), show_fps=True)
