# coding: utf-8

import math, wave, array, numpy, sound

gobalWaveGen_soundPlayerObj = None

def waveGenerator(freq, duration, volume, numChan, path) :
  """
  generate and save to a file a sine wave with the specified parameters
  NOT SURE IF STEREO IS IMPLEMENTED CORRECTLY...BUT IT SOUNDS O.K.
  
  path = 'path2saveFileAt'
  duration = # seconds
  freq = # of cycles per second (Hz)
  volume = percent
  numChan = # of channels (1: mono, 2: stereo)
  """
  
  global gobalWaveGen_soundPlayerObj
  
  frameRate = 44100.0 # i.e. samples per second (44.1K standard)

  sampleWidth = 2 * numChan # 2 bytes per channnel
  
  numberOfBits = sampleWidth * 8 
  numFramesPerCyc = (frameRate/freq)
  
  numFrames = int(frameRate * duration * numChan)
  
  # faster data point calculations this way
  peakValue = (math.pow(2, numberOfBits)/2 - 1) * float(volume)/100  
  th = numpy.linspace(0, 2 * numpy.pi * freq * duration, numFrames, endpoint=False)

  if numChan == 2:
    data = (peakValue * numpy.sin(th)).astype(numpy.int32)
    fileName = path + str(freq) + "HzStereo.wav"    
  else:
    data = (peakValue * numpy.sin(th)).astype(numpy.int16)
    fileName = path + str(freq) + "HzMono.wav"
  
  
  f = wave.open(fileName, 'wb')    
  f.setparams((numChan, sampleWidth, frameRate, numFrames, 'NONE', 'not compressed'))
  f.writeframes(data.tostring())
  f.close()
  
  
  #gobalWaveGen_soundPlayerObj = sound.Player(fileName)
  #gobalWaveGen_soundPlayerObj.play()
  
  # display raw data
  """
  print()
  print("raw data written to wave file:\n")
  print("data[0] =", data[0], "data[1] =", data[1], "data[2] =", data[2], "data[3] =", data[3], "data[4] =", data[4], "data[5] =", data[5],"...", "data[numFrames-3] =",data[numFrames-3], "data[numFrames-2] =", data[numFrames-2], "data[numFrames-1] =",data[numFrames-1])
  
  print("\n",data[0].tostring(), data[1].tostring(), data[2].tostring(), "...", data[numFrames-3].tostring(), data[numFrames-2].tostring(), data[numFrames-1].tostring())
  """
  
  
  return fileName

"""
path2_originalVoices = './waveFiles/originalVoices/'
path = path2_originalVoices
freq = 440 # Hz
duration = 2 # seconds
volume = 100 # percent
numChan = 2 # of channels (1: mono, 2: stereo)

waveGenerator(freq, duration, volume, numChan, path) # generate the wave file
"""
