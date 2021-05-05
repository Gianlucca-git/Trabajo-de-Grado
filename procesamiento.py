
import essentia

import IPython.display as ipd
import numpy
import numpy as np

import matplotlib.pyplot as plt
from essentia.standard import *
import warnings 
warnings.filterwarnings('ignore')


class Procesamiento():

    def f_audio ():

        #CARGO EL ARCHIVO.WAV 
        Archivo = 'grabaciones/monos_ebrios.wav'
        Audio = MonoLoader(filename=Archivo)()
        print("\n\n     EMPIEZA   \n\n")
        return Audio,Archivo
        

    def f_beats_for_minutes(Audio):

        ##  FUNCION PARA EXTRAER LOS BEATS POR MINUTOS DEL ARCHIVO  
        ##  CON ESTO PODREMOS LUEGO VALIDAR LOS COMPACES 

        rhythm_extractor = RhythmExtractor2013(method="multifeature")
        bpm, beats, b_conf, _, _ = rhythm_extractor(Audio)

        #print("BPM:", bpm)
        #print ("Primer Beat en el segundo ->", beats[0] )
        #print ("Ultimo Beat en el segundo ->", beats[len(beats)-1] )
        #print("beats Detectados ->", len(beats) )##picos de grafica 
        #print("Beat positions (sec.):", beats)
        #print("Beat estimation confidence:", b_conf)
        return bpm
        #################################################################

    def f_extractor_times_and_notes(Audio,Archivo):

        ## FUNCION PARA EXTRAER TODOS LOS TIEMPOS Y VALORES DE LAS NOTAS EXISTENTES 
        loader = EqloudLoader(filename= Archivo, sampleRate=(48000))
        #duracion = format(len(Audio)/44100.0)
        #print("\n\nDuracion del audio en total [seg]: ", duracion) 

        pitch_extractor = PredominantPitchMelodia(frameSize=1024, hopSize=512) ## lista de todos los tiempos
        pitch_values, pitch_confidence = pitch_extractor(Audio) ## lista de todos los valores en el tiempo

        # Pitch is estimated on frames. Compute frame time positions
        pitch_times = np.linspace(0.0,len(Audio)/44100.0,len(pitch_values) )

    
    def f_essentia_extract(Audio):
        ##    METODOS DE LIBRERIA QUE DETECTAN DONDE OCURRE CADA NOTA RESPECTO AL TIEMPO   

        od2 = OnsetDetection(method='complex')
        # Let's also get the other algorithms we will need, and a pool to store the results
        w = Windowing(type = 'hann')
        fft = FFT() # this gives us a complex FFT
        c2p = CartesianToPolar() # and this turns it into a pair (magnitude, phase)
        pool = essentia.Pool()

        # Computing onset detection functions.
        for frame in FrameGenerator(Audio, frameSize = 1024, hopSize = 512):
            mag, phase, = c2p(fft(w(frame)))
            pool.add('features.complex', od2(mag, phase))

        ## inicio de cada "nota"
        onsets = Onsets()
        l_tiempos_detectados_essentia = onsets(essentia.array([ pool['features.complex'] ]),[ 1 ])
        print(l_tiempos_detectados_essentia)

    def main():
        P = Procesamiento
        Audio, Archivo = P.f_audio()
        #P.f_beats_for_minutes(Audio)
        #P.f_extractor_times_and_notes(Audio,Archivo)
        P.f_essentia_extract(Audio)

Procesamiento.main()