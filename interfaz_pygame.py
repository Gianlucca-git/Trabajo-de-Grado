import pygame
import sys
import pyaudio
import wave
from pygame.locals import *

import time


class interfaz():

    def __init__(self):
        super().__init__()

        # Cargar fondo
        self.fondo = pygame.image.load("iconos/fondo.png")

        # Cargar botones
        grabar          = pygame.image.load("botones/grabar_.png")
        parar           = pygame.image.load("botones/parar_.png")
        reduccion_uno   = pygame.image.load("botones/reduccion_uno.png")
        reduccion_dos   = pygame.image.load("botones/reduccion_dos.png")
        reduccion_tres  = pygame.image.load("botones/reduccion_tres.png")
        dos             = pygame.image.load("botones/dos.png")
        uno             = pygame.image.load("botones/uno.png")
        tres            = pygame.image.load("botones/tres.png")
        cuatro          = pygame.image.load("botones/cuatro.png")

        # Cargar iconos
        icono_grabar    = pygame.image.load("iconos/grabar.png")
        icono_parar     = pygame.image.load("iconos/parar.png")

        # VARIABLES GLOBALES
        self.segundo              = 0
        self.act_grabar_conteo    = False  # bandera para hacer el conteo 3,2,1,parar
        # bandera para hacer la traslacion del boton grabar a parar
        self.act_grabar_traslacion = False

        pygame.init()
        self.window = pygame.display.set_mode((800, 560))
        #mensaje a la ventana:
        pygame.display.set_caption("Dolphings Tabs")

        #MENSAJES para imprimir posteriormente
        fuente   = pygame.font.SysFont("ubuntu", 15)
        riff_1   = fuente.render("º    Riff Uno ", 10, (100, 100, 100))
        riff_2   = fuente.render("º    Riff Dos ", 10, (100, 100, 100))
        riff_3   = fuente.render("º    Riff Tres ", 10, (100, 100, 100))
        riff_4   = fuente.render("º    Riff Cuatro ", 10, (100, 100, 100))
        riff_5   = fuente.render("º    Riff Cinco ", 10, (100, 100, 100))
        riff_6   = fuente.render("º    Riff Seis ", 10, (100, 100, 100))
        riff_7   = fuente.render("º    Riff Siete ", 10, (100, 100, 100))
        riff_8   = fuente.render("º    Riff Ocho ", 10, (100, 100, 100))
        riff_9   = fuente.render("º    Riff Nueve ", 10, (100, 100, 100))

        self.dicc_iconos = {
            "grabar": {
                "visible" : True,
                "objeto"  : icono_grabar,
                "area"    : (275, 380, 0, 0)
            },
            "parar": {
                "visible" : False,
                "objeto"  : icono_parar,
                "area"    : (266, 379, 0, 0)

            },
        }
        self.list_iconos=[self.dicc_iconos['grabar'],self.dicc_iconos['parar']]
        
        self.dicc_boton = {

            "grabar": {
                "visible" : True,
                "objeto"  : grabar,
                "area"    : (190, 370, 190+110, 370+40)
            },
            "parar": {
                "visible" : False,
                "objeto"  : parar,
                "area"    : (195, 370, 195+110, 370+40)

            },
            "uno": {
                "visible" : False,
                "objeto"  : uno,
                "area"    : (220, 370)
            },
            "dos": {
                "visible" : False,
                "objeto"  : dos,
                "area"    : (220, 370)
            },
            "tres": {
                "visible" : False,
                "objeto"  : tres,
                "area"    : (220, 370)
            },
            "cuatro": {
                "visible" : False,
                "objeto"  : cuatro,
                "area"    : (220, 370)
            },
            "reduccion_uno": {
                "visible" : False,
                "objeto"  : reduccion_uno,
                "area"    : (205, 370)
            },
            "reduccion_dos": {
                "visible" : False,
                "objeto"  : reduccion_dos,
                "area"    : (210, 370)
            },
            "reduccion_tres": {
                "visible" : False,
                "objeto"  : reduccion_tres,
                "area"    : (220, 370)
            }
        }
        self.lis_boton_grab = [self.dicc_boton['grabar'], self.dicc_boton['parar'], self.dicc_boton['uno'], self.dicc_boton['dos'], self.dicc_boton['tres'],
                               self.dicc_boton['cuatro'], self.dicc_boton['reduccion_uno'], self.dicc_boton['reduccion_dos'], self.dicc_boton['reduccion_tres']]

        self.dicc_riff = {
            "riff_1": {
                "visible" : True,
                "texto"   : "Riff_Uno",
                "objeto"  : riff_1,
                "area"    : (120, 155)
            },
            "riff_2": {
                "visible" : True,
                "texto"   : "Riff_Dos",
                "objeto"  : riff_2,
                "area"    : (120, 175)
            },
            "riff_3": {
                "visible" : False,
                "texto"   : "Riff_Tres",
                "objeto"  : riff_3,
                "area"    : (120, 195)
            },
            "riff_4": {
                "visible" : False,
                "texto"   : "Riff_Cuatro",
                "objeto"  : riff_4,
                "area"    : (120, 215)
            },
            "riff_5": {
                "visible" : True,
                "texto"   : "Riff_Cinco",
                "objeto"  : riff_5,
                "area"    : (120, 235)
            },
            "riff_6": {
                "visible" : True,
                "texto"   : "Riff_Seis",
                "objeto"  : riff_6,
                "area"    : (120, 255)
            },
            "riff_7": {
                "visible" : True,
                "texto"   : "Riff_Siete",
                "objeto"  : riff_7,
                "area"    : (120, 275)
            },
            "riff_8": {
                "visible" : True,
                "texto"   : "Riff_Ocho",
                "objeto"  : riff_8,
                "area"    : (120, 295)
            },
            "riff_9": {
                "visible" : True,
                "texto"   : "Riff_Nueve",
                "objeto"  : riff_9,
                "area"    : (120, 315)
            }
        }
        self.list_riff = [self.dicc_riff['riff_1'], self.dicc_riff['riff_2'], self.dicc_riff['riff_3'], self.dicc_riff['riff_4'],
                          self.dicc_riff['riff_5'], self.dicc_riff['riff_6'], self.dicc_riff['riff_7'], self.dicc_riff['riff_8'], self.dicc_riff['riff_9']]

        self.controlador_gui(True)

    def dibujar(self, lista_botones):

        for diccionario_boton in lista_botones:
            if diccionario_boton['visible']:
                self.window.blit(
                    diccionario_boton['objeto'], diccionario_boton['area'][:2])

    def temporizador(limite):

        tiempo_inicial = time.monotonic()
        tiempo         = 0

        while (tiempo < limite):
            tiempo = time.monotonic() - tiempo_inicial
        return 1

    def accion_grabar_conteo(self):  # hacer el conteo 3,2,1,parar
        #print( "Entre a Accion Grabar ")

        if self.segundo == 0:
            self.dicc_boton['tres']['visible']   = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 1:
            self.dicc_boton['tres']['visible']   = False
            self.dicc_boton['dos']['visible']    = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 2:
            self.dicc_boton['dos']['visible']    = False
            self.dicc_boton['uno']['visible']    = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 3:
            self.dicc_boton['uno']['visible']    = False
            self.dicc_boton['parar']['visible']  = True
            self.dicc_iconos['parar']['visible'] = True
            self.segundo = 0
            self.dibujar(self.lis_boton_grab)
            self.act_grabar_conteo = False

        self.segundo = self.segundo + interfaz.temporizador(1)

    # hacer la traslacion del boton grabar a para
    def accion_grabar_traslacion(self):
        
        self.segundo = self.segundo + interfaz.temporizador(0.02)

        if self.segundo == 1:
            self.dicc_boton['reduccion_uno']['visible']  = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 2:
            self.dicc_boton['reduccion_uno']['visible']  = False
            self.dicc_boton['reduccion_dos']['visible']  = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 3:
            self.dicc_boton['reduccion_dos']['visible']  = False
            self.dicc_boton['reduccion_tres']['visible'] = True
            self.dibujar(self.lis_boton_grab)
        elif self.segundo == 4:
            self.dicc_boton['reduccion_tres']['visible'] = False
            self.dicc_boton['cuatro']['visible']         = True
            self.dibujar(self.lis_boton_grab)
            self.dicc_boton['cuatro']['visible']         = False

            self.act_grabar_traslacion                   = False
            # cambiamos la bandera de conteo para seguir el flujo
            self.act_grabar_conteo                       = True
            self.segundo = 0

    def gui_lista_riff(self,alterar):
        for riff in self.list_riff:
            if not riff['visible'] :
                if alterar :
                    riff['visible'] = True
                return riff['texto']        
        return "limite"

    
    def controlador_gui(self, iniciar):

        while iniciar:

            self.window.blit(self.fondo, (0, 0))             

            if   self.act_grabar_traslacion:
                 self.accion_grabar_traslacion()
            elif self.act_grabar_conteo:                
                 #self.dicc_boton['cuatro']['visible'] = False
                 self.accion_grabar_conteo()                 
            
            elif self.gui_lista_riff(False)  == "limite":
                    self.dicc_boton ['parar'] ['visible'] = False
                    self.dicc_boton ['grabar']['visible'] = False
                    self.dicc_iconos['parar'] ['visible'] = False
                    self.dicc_iconos['grabar']['visible'] = False
                    self.dibujar(self.lis_boton_grab)
          
            elif self.dicc_boton['parar']['visible'] :         
               
                    self.funcion_grabar_parar(self.gui_lista_riff(True))
                    # Vovel al estado de Grabacion
                    self.dicc_boton ['parar'] ['visible'] = False
                    self.dicc_boton ['grabar']['visible'] = True
                    self.dicc_iconos['parar'] ['visible'] = False
                    self.dicc_iconos['grabar']['visible'] = True
            else:
                 self.dibujar(self.lis_boton_grab)
            
            ## Dibuje encima
            self.dibujar(self.list_riff)
            self.dibujar(self.list_iconos)

            for event in pygame.event.get():
                #print(str(event)+ '\n')

                #si pulsan la X
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    mouse = event.pos

                    if      (mouse[0] > self.dicc_boton['grabar']['area'][0])\
                        and (mouse[0] < self.dicc_boton['grabar']['area'][2])\
                        and (mouse[1] > self.dicc_boton['grabar']['area'][1])\
                        and (mouse[1] < self.dicc_boton['grabar']['area'][3])\
                        and self.dicc_boton['grabar']['visible']:

                        self.dicc_boton['grabar']['visible'] = False
                        self.dicc_iconos['grabar']['visible'] = False
                        self.act_grabar_traslacion = True
                        #self.dicc_boton['parar']['visible'] = True

            pygame.display.update()

    def funcion_grabar_parar(self, riff_numero):      

        #formato de los samples 
        FORMAT=pyaudio.paInt16
        #numero de canales 
        CHANNELS=2
        #número de unidades menores de memoria ( 1024 frames )
        CHUNK=1024
        #Almacenar las chunk en 44100 frames por segundo
        RATE=44100

        #Archivo que se generara 
        #NOTA: los archivos con mismo nombre se reemplazan
        archivo = riff_numero +".wav" ##( input ("Ingrese nombre del archivo :   ") + ".wav" )

        frames=[]
        #INICIAMOS "pyaudio"
        audio= pyaudio.PyAudio()
        #INICIAMOS GRABACIÓN con metodo audio.open
        stream=audio.open(format=FORMAT,channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        finalizar = False
        while not finalizar :
                for event in pygame.event.get():                
                    if  event.type == MOUSEBUTTONUP:
                        mouse = event.pos                                           
                        if      (mouse[0] > self.dicc_boton['parar']['area'][0])\
                            and (mouse[0] < self.dicc_boton['parar']['area'][2])\
                            and (mouse[1] > self.dicc_boton['parar']['area'][1])\
                            and (mouse[1] < self.dicc_boton['parar']['area'][3]):                            
                            finalizar = True
                          
                data=stream.read(CHUNK)
                frames.append(data)

        # DETENEMOS GRABACIÓN
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # GUARDAMOS EL ARCHIVO DE AUDIO
        waveFile = wave.open(("grabaciones/")+archivo, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        print("terminada")
interfaz()
