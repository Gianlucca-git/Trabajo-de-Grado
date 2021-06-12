import sounddevice as sd
import numpy as np
import scipy.fftpack
import os
import matplotlib.pyplot as plt
import copy

## https://www.chciken.com/digital/signal/processing/2020/05/13/guitar-tuner.html
class c_tunner ():
    # General settings
    SAMPLE_FREQ = 48000 # sample frequency in Hz
    WINDOW_SIZE = 48000 # window size of the DFT in samples
    WINDOW_STEP = 12000 # step size of window
    WINDOW_T_LEN = WINDOW_SIZE / SAMPLE_FREQ # length of the window in seconds
    SAMPLE_T_LENGTH = 1 / SAMPLE_FREQ # length between two samples in seconds
    NUM_HPS = 8 #max number of harmonic product spectrums
    DELTA_FREQ = (SAMPLE_FREQ/WINDOW_SIZE) # frequency step width of the interpolated DFT
    windowSamples = [0 for _ in range(WINDOW_SIZE)]
    noteBuffer = ["1","2","3"]

    # This function finds the closest note for a given pitch
    # Returns: note (e.g. a, g#, ..), pitch of the tone
    CONCERT_PITCH = 440
    ALL_NOTES = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
    def find_closest_note(pitch):
      i = int( np.round( np.log2( pitch/c_tunner.CONCERT_PITCH )*12 ) )
      clostestNote = c_tunner.ALL_NOTES[i%12] + str(4 + np.sign(i) * int( (9+abs(i))/12 ) )
      closestPitch = c_tunner.CONCERT_PITCH*2**(i/12)
      return clostestNote, closestPitch

    hannWindow = np.hanning(WINDOW_SIZE)
    def callback(indata, frames, time, status):
      #global windowSamples, lastNote
      if status:
        print(status)
      if any(indata):
        windowSamples = np.concatenate((c_tunner.windowSamples,indata[:, 0])) # append new samples
        windowSamples = windowSamples[len(indata[:, 0]):] # remove old samples

        signalPower = (np.linalg.norm(windowSamples, ord=2)**2) / len(windowSamples)
        if signalPower < 5e-7:
          os.system('cls' if os.name=='nt' else 'clear')
          print("Closest note: ...")
          return

        hannSamples = windowSamples * c_tunner.hannWindow
        magnitudeSpec = abs( scipy.fftpack.fft(hannSamples)[:len(hannSamples)//2] )

        #supress mains hum
        for i in range(int(62/c_tunner.DELTA_FREQ)):
          magnitudeSpec[i] = 0

        #Calculate average energy per frequency for the octave bands
        octaveBands = [50,100,200,400,800,1600,3200,6400,12800,25600]
        for j in range(len(octaveBands)-1):
          indStart = int(octaveBands[j]/c_tunner.DELTA_FREQ)
          indEnd = int(octaveBands[j+1]/c_tunner.DELTA_FREQ)
          indEnd = indEnd if len(magnitudeSpec) > indEnd else len(magnitudeSpec)
          avgEnergPerFreq = 1*(np.linalg.norm(magnitudeSpec[indStart:indEnd], ord=2)**2) / (indEnd-indStart)
          avgEnergPerFreq = avgEnergPerFreq**0.5
          for i in range(indStart, indEnd):
            magnitudeSpec[i] = magnitudeSpec[i] if magnitudeSpec[i] > avgEnergPerFreq else 0  #suppress white noise

        #Interpolate spectrum
        magSpecIpol = np.interp(np.arange(0, len(magnitudeSpec), 1/c_tunner.NUM_HPS), np.arange(0, len(magnitudeSpec)), magnitudeSpec)
        magSpecIpol = magSpecIpol / np.linalg.norm(magSpecIpol, ord=2) #normalize it

        hpsSpec = copy.deepcopy(magSpecIpol)

        for i in range(c_tunner.NUM_HPS):
          tmpHpsSpec = np.multiply(hpsSpec[:int(np.ceil(len(magSpecIpol)/(i+1)))], magSpecIpol[::(i+1)])
          if not any(tmpHpsSpec):
            break
          hpsSpec = tmpHpsSpec

        maxInd = np.argmax(hpsSpec)
        maxFreq = maxInd * (c_tunner.SAMPLE_FREQ/c_tunner.WINDOW_SIZE) / c_tunner.NUM_HPS

        closestNote, closestPitch = c_tunner.find_closest_note(maxFreq)
        maxFreq = round(maxFreq, 1)
        closestPitch = round(closestPitch, 1)

        c_tunner.noteBuffer.insert(0,closestNote) #note that this is a ringbuffer
        c_tunner.noteBuffer.pop()

        majorityVote = max(set(c_tunner.noteBuffer), key = c_tunner.noteBuffer.count)

        if c_tunner.noteBuffer.count(majorityVote) > 1:
          detectedNote = majorityVote
        else:
          return
        #os.system('cls' if os.name=='nt' else 'clear')
        print(f"Closest note: {closestNote} {maxFreq}/{closestPitch}")

      else:
        print('no input')
    def main ():

      try:
        print("Starting HPS guitar tuner...")
        with sd.InputStream(channels=1, callback=c_tunner.callback,
          blocksize = c_tunner.WINDOW_STEP,
          samplerate = c_tunner.SAMPLE_FREQ):
          while True:
            response = input()
            if response in ('', 'q', 'Q'):
              break
      except Exception as e:
          print(str(e))

