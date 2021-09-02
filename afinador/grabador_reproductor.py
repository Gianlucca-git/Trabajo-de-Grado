import wave
import pyaudio
import time


def grabar(bandera,numero_riff):

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
        archivo = "Riff_"+ (str(numero_riff)) +".wav" ##( input ("Ingrese nombre del archivo :   ") + ".wav" )

        ##while  (bandera):

            ##intext = ( input ("Escriba  ''iniciar'' para grabar :   ") )
            ##if (intext  == "iniciar" ):
                ##bandera = False


        if True:
                
                
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
                #print("GRABANDO...")
                while (tiempo < 10 ):
                        
                        tiempo = time.monotonic() - tiempo_inicial 
                        data=stream.read(CHUNK)
                        frames.append(data)
                
        #print("grabación terminada")


        #DETENEMOS GRABACIÓN
        stream.stop_stream()
        stream.close()
        audio.terminate()

        #CREAMOS/GUARDAMOS EL ARCHIVO DE AUDIO
        waveFile = wave.open(("grabaciones/")+archivo, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


def reproductor(bandera_reproductor,archivo):
        ## REPRODUCTOR ##
        chunk = 1024 

        f = wave.open(("grabaciones/")+archivo,'rb')


        #INICIAMOS PyAudio.
        p = pyaudio.PyAudio()  

        #ABRIMOS STREAM
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)

        #LEEMOS INFORMACIÓN  
        data = f.readframes(chunk)  
        print(" QUE MIERDAS ")
        #REPRODUCIMOS "stream"  
        while data:  
                stream.write(data)  
                data = f.readframes(chunk)  

        #PARAMOS "stream".  
        stream.stop_stream()  
        stream.close()  

        #FINALIZAMOS PyAudio  
        p.terminate()
        print(" Termino ")  



##grabar(True)
reproductor(True, "Riff_Uno.wav")