import VXbuttons
from VXbuttons import *
import sound, time
import audioop, numpy




# Voice X-formation functions
def XformRecording(self):   
  
  originalRec, singerRec = getWaveFiles(self) # get the wave files the user selected
  
  # now get the raw data from each of them, 
  # convert to mono if stereo before returning the data
  originalData = getWaveFileData(originalRec)
  print("\noriginal data", originalData[0:10], "...", originalData[-10:]) 
  
  singerData = getWaveFileData(singerRec)
  print("\nsinger data", singerData[0:10], "...", singerData[-10:])
  
  # YOU ARE HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  XformedData = processData(originalData, singerData)
  print("\nXformed data", XformedData[0:10], "...", XformedData[-10:])
  
  fileName = None
  XformedRec = writeWaveFile(XformedData, path2_transformedVoices, fileName)  
  
  return sound.Player(XformedRec)




def processData(original, singer):
  
  XformedData = list()
  for index in range(44100):
    XformedData.append(singer[index]) 
  
  return XformedData




def writeWaveFile(XformedData, path2_transformedVoices, fileName):
  if fileName == None:
    path_file = path2_transformedVoices + time.asctime() + '.wav'
  else :
    path_file = path2_transformedVoices + fileName 
    
  hand = wave.open(path_file, 'wb')  
  hand.setparams((1, 2, 44100, len(XformedData), 'NONE', 'not compressed'))

  data = numpy.array(XformedData, numpy.int16)
 
  hand.writeframes(data)    
  hand.close()
  
  return path_file # return the Xformed recording to be played
  
    

     
def getWaveFileData(waveFile):
  # read the raw data from the wave file and return it.
  
  hand = wave.open(waveFile, "rb")
    
  # get data all at once -10 TIMES FASTER THIS WAY!!!
  # but...(run into memory issues this way????)
  bytesObj = hand.readframes(hand.getnframes()) 
  if hand.getnchannels() == 2:
    # convert stereo bytesObj into a mono bytesObj
    bytesObj = audioop.tomono(bytesObj, 2, 1, 1)
      
  data = unpackData(hand.getnframes(), bytesObj)         
  hand.close()    
  return data




def unpackData(nframes, bytesObj):
  # each bytesObj unpacked must have an associated "h"
  try:
    data = struct.unpack(str(nframes) + "h", bytesObj)
  except :
    try:
      data = struct.unpack(str(2*nframes) + "h", bytesObj)
    except :
      try:
        data = struct.unpack(str(3*nframes) + "h", bytesObj)
      except :
        try:
          data = struct.unpack(str(4*nframes) + "h", bytesObj)
        except :
          print("unpackData - nothing worked!")
          data = list()
  return data




def mono(file):
  fileName = file.split("/").pop()
  return path2_temp + "mono_" + fileName
 
  
    
  
     
def getWaveFiles(self): 
  originalRec = path2_originalVoices + self.originalRecordings[state["originalRecSelectedIndex"]].text
  
  singerRec = path2_voices2emulate + self.singerRecordings[state["singerRecSelectedIndex"]].text
  
  return originalRec, singerRec

    
 
    
# Old logic for viewing the waveform, never fully implemented ********************** 
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

"""
  for unpacking 1 frame at a time
  try:
    data = struct.unpack("h"), bytesObj)
    print("h")
  except :
    try:
      data = struct.unpack("hh", bytesObj)
      print("hh")
    except :
      try:
        data = struct.unpack("hhh", bytesObj)
        print("hhh")
      except :
        try:
          data = struct.unpack("hhhh", bytesObj)
          print("hhhh")
        except :
          print("nothing worked!")
"""         
# ********************************************************************************* 
 
    
     

