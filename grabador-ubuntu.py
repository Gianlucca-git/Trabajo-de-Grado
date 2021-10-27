import wave
import keyboard
import os
import pyaudio
import time


#DEFINIMOS PARAMETROS
#procesamiento de sonido:

#formato de los samples 
FORMAT=pyaudio.paInt16
#numero de canales 
CHANNELS=2
#número de unidades menores de memoria ( 1024 frames )
CHUNK=1024
#Almacenar las chunk en 44100 frames por segundo
RATE=44100
#tiempo en segundos
duracion=10
#Archivo que se generara 
#NOTA: los archivos con mismo nombre se reemplazan
archivo = ( input ("Ingrese nombre del archivo :   ") + ".wav" )


una_vez=True

bandera= True
while  (bandera):

    intext = ( input ("Escriba  ''iniciar'' para grabar :   ") )
    if (intext  == "iniciar" ):
        bandera = False


if una_vez:
        
        
        frames=[]
        #INICIAMOS "pyaudio"
        audio=pyaudio.PyAudio()
        #INICIAMOS GRABACIÓN con metodo audio.open
        stream=audio.open(format=FORMAT,channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
        #print ("Vuelva a presionar  ''Espacio'' para finalizar grabacion. ")
        una_vez=False
        
        #while  not(keyboard.press_and_release('space')):
        tiempo_inicial = time.monotonic() 
        tiempo= 0
        print("GRABANDO...")
        while (tiempo < 10 ):
                
                tiempo = time.monotonic() - tiempo_inicial 
                data=stream.read(CHUNK)
                frames.append(data)
        
print("grabación terminada")


#DETENEMOS GRABACIÓN
stream.stop_stream()
stream.close()
audio.terminate()

#CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
waveFile = wave.open(archivo, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()


## REPRODUCTOR ##
chunk = 1024 

f = wave.open(archivo,'rb')


#INICIAMOS PyAudio.
p = pyaudio.PyAudio()  

#ABRIMOS STREAM
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)

#LEEMOS INFORMACIÓN  
data = f.readframes(chunk)  

#REPRODUCIMOS "stream"  
while data:  
    stream.write(data)  
    data = f.readframes(chunk)  

#PARAMOS "stream".  
stream.stop_stream()  
stream.close()  

#FINALIZAMOS PyAudio  
p.terminate()  




