"""

import matplotlib.pyplot as plt


sampleFreq, myRecording = scipy.io.wavfile.read("grabaciones/Riff_Uno.wav")
sampleDur = len(myRecording)/sampleFreq
timeX = np.arange(0,sampleDur, 1/sampleFreq)

sampleFreq_2, myRecording_2 = scipy.io.wavfile.read("grabaciones/Riff_Dos.wav")
sampleDur_2 = len(myRecording_2)/sampleFreq_2
timeX_2 = np.arange(0,sampleDur_2, 1/sampleFreq_2)

plt.plot([5,6,7,8,9,10], [5,4,3,2,1,2])
#plt.plot(timeX_2, myRecording_2)
print("COMIENZO")
print (len (timeX_2))
print("COMIENZO 2 ")
print (len (myRecording_2))
print("FIN")
plt.ylabel('x(k)')
plt.xlabel('time[s]')
plt.show()

"""
##import matplotlib
#matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import scipy.io.wavfile
import numpy as np
import pylab

fig = pylab.figure(figsize=[2, 2], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )


sampleFreq, myRecording = scipy.io.wavfile.read("grabaciones/Riff_Uno.wav")
sampleDur = len(myRecording)/sampleFreq
timeX = np.arange(0,sampleDur, 1/sampleFreq)

ax = fig.gca()
ax.plot( timeX , myRecording)

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
raw_data = renderer.tostring_rgb()

import pygame
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((600, 400), DOUBLEBUF)
screen = pygame.display.get_surface()

size = canvas.get_width_height()

surf = pygame.image.fromstring(raw_data, size, "RGB")
screen.blit(surf, (0,0))
pygame.display.flip()

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True 