import pyaudio
import wave
from pynput import keyboard as kb
import os

class  Grabador_Reproductor():

    #Archivo que se generara 
    #NOTA: los archivos con mismo nombre se reemplazan
    archivo = ( input ("Ingrese nombre del archivo : G: ") + ".wav" )

    def controlador():




        bandera= True
        una_vez=True

        with kb.Listener(Grabador_Reproductor.grabar) as escuchador:

            print ('presione la tecla "g" para grabar')
            escuchador.join()
        
        return 0

    def grabar (tecla):
            
            #print ("tecla :" , str(tecla))
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

            #while  not(keyboard.Listener(f).run().):
            #    print(".",end="")
            #    pass 

     
                 

            if (tecla == kb.KeyCode.from_char('g') ):
                    
                    
                
                frames=[]
                #INICIAMOS "pyaudio"
                audio=pyaudio.PyAudio()
                #INICIAMOS GRABACIÓN con metodo audio.open
                stream=audio.open(format=FORMAT,channels=CHANNELS,
                                    rate=RATE, input=True,
                                    frames_per_buffer=CHUNK)
                #print ("Vuelva a presionar  ''Espacio'' para finalizar grabacion. ")
                una_vez=False

                escuchador = kb.Listener(Grabador_Reproductor.pulso)
                escuchador.start()
                
                print ("Vuelva a presionar  ''f'' para finalizar grabacion. ")

                while  escuchador.is_alive():
                        print("GRABANDO...")
                        data=stream.read(CHUNK)
                        frames.append(data)            
     
            #DETENEMOS GRABACIÓN
            stream.stop_stream()
            stream.close()
            audio.terminate()
                    

            #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
            waveFile = wave.open(Grabador_Reproductor.archivo, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            print("grabación terminada")
            return 0

    def pulso(tecla):
        print('Se ha soltado la tecla ' + str(tecla))
        if tecla == kb.KeyCode.from_char('f'):
            return False

Grabador_Reproductor.controlador()