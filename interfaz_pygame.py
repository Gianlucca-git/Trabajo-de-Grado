import pygame
import sys
import pyaudio
import wave
from pygame.locals import *
import threading
from generar import process
## graficar ___
import matplotlib.backends.backend_agg as agg
import scipy.io.wavfile
import numpy as np
import pylab


import time


class interfaz():

    def __init__(self):
        super().__init__()

        # Cargar fondo
        self.fondo = pygame.image.load("iconos/fondo_3.png")

        # Cargar botones
        grabar          = pygame.image.load("botones/grabar_.png")
        parar           = pygame.image.load("botones/parar_.png")
        generar          = pygame.image.load("botones/generar.png")
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
        icono_ondas     = pygame.image.load("iconos/sonido.png")
        icono_basura    = pygame.image.load("iconos/eliminar.png")

        # Cargando inconos
        icono_cargar_1    = pygame.image.load("iconos/carga_1.png")
        icono_cargar_2     = pygame.image.load("iconos/carga_2.png")
        icono_cargar_3     = pygame.image.load("iconos/carga_3.png")
        icono_cargar_4    = pygame.image.load("iconos/carga_4.png")

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
        riff_1   = fuente.render("º  Riff 0 ", 10, (100, 100, 100))
        riff_2   = fuente.render("º  Riff 1 ", 10, (100, 100, 100))
        riff_3   = fuente.render("º  Riff 2 ", 10, (100, 100, 100))
        riff_4   = fuente.render("º  Riff 3 ", 10, (100, 100, 100))
        riff_5   = fuente.render("º  Riff 4 ", 10, (100, 100, 100))
        riff_6   = fuente.render("º  Riff 5 ", 10, (100, 100, 100))
        riff_7   = fuente.render("º  Riff 6 ", 10, (100, 100, 100))
        riff_8   = fuente.render("º  Riff 7 ", 10, (100, 100, 100))
        riff_9   = fuente.render("º  Riff 8 ", 10, (100, 100, 100))
        riff_10  = fuente.render("º  Riff 9 ", 10, (100, 100, 100))
        procesando  = fuente.render("PROCESANDO", 10, (50, 50, 50))

                
        self.dicc_boton = {

            "grabar": {
                "visible" : True,
                "objeto"  : grabar,
                "area"    : (190, 380, 190+110, 380+40)
            },
            "parar": {
                "visible" : False,
                "objeto"  : parar,
                "area"    : (195, 380, 195+110, 380+40)

            },
            "generar": {
                "visible" : False,
                "objeto"  : generar,
                "area"    : (550, 440, 550+123, 440+40)

            },
            "uno": {
                "visible" : False,
                "objeto"  : uno,
                "area"    : (220, 380)
            },
            "dos": {
                "visible" : False,
                "objeto"  : dos,
                "area"    : (220, 380)
            },
            "tres": {
                "visible" : False,
                "objeto"  : tres,
                "area"    : (220, 380)
            },
            "cuatro": {
                "visible" : False,
                "objeto"  : cuatro,
                "area"    : (220, 380)
            },
            "reduccion_uno": {
                "visible" : False,
                "objeto"  : reduccion_uno,
                "area"    : (205, 380)
            },
            "reduccion_dos": {
                "visible" : False,
                "objeto"  : reduccion_dos,
                "area"    : (210, 380)
            },
            "reduccion_tres": {
                "visible" : False,
                "objeto"  : reduccion_tres,
                "area"    : (220, 380)
            }
        }
        self.lis_boton_grab = [self.dicc_boton['grabar'], self.dicc_boton['parar'], self.dicc_boton['generar'], self.dicc_boton['uno'], self.dicc_boton['dos'], self.dicc_boton['tres'],
                               self.dicc_boton['cuatro'], self.dicc_boton['reduccion_uno'], self.dicc_boton['reduccion_dos'], self.dicc_boton['reduccion_tres']]
        self.dicc_cargar = {
            "cargar_1": {
                "visible" : False,
                "objeto"  : icono_cargar_1,
                "area"    : (600, 405, 0, 0)
            },
            "cargar_2": {
                "visible" : False,
                "objeto"  : icono_cargar_2,
                "area"    : (600, 405, 0, 0)
            },
            "cargar_3": {
                "visible" : False,
                "objeto"  : icono_cargar_3,
                "area"    : (600, 405, 0, 0)
            },
            "cargar_4": {
                "visible" : False,
                "objeto"  : icono_cargar_4,
                "area"    : (600, 405, 0, 0)
            },
        }
        self.list_iconos_cargar=[self.dicc_cargar['cargar_1'],self.dicc_cargar['cargar_2'],self.dicc_cargar['cargar_3'],self.dicc_cargar['cargar_4']]

        self.dicc_iconos = {
            "grabar": {
                "visible" : True,
                "objeto"  : icono_grabar,
                "area"    : (275, 390, 0, 0)
            },
            "parar": {
                "visible" : False,
                "objeto"  : icono_parar,
                "area"    : (266, 389, 0, 0)

            }
        }
        self.list_iconos=[self.dicc_iconos['grabar'],self.dicc_iconos['parar']]

        self.dicc_ondas={
            "onda_1": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (170, 175,170+16,175+16)
            },
            "onda_2": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (170, 210,170+16,210+16)
            },
            "onda_3": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (170, 245,170+16,245+16)
            },
            "onda_4": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (170, 280,170+16,280+16)
            },
            "onda_5": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (170, 315,170+16,315+16)
            },
            "onda_6": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (350, 175,350+16,175+16)
            },
            "onda_7": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (350, 210,350+16,210+16)
            },
            "onda_8": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (350, 245,350+16,245+16)
            },
            "onda_9": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (350, 280,350+16,280+16)
            },
            "onda_10": {
                "visible" : False,
                "objeto"  : icono_ondas,
                "area"    : (350, 315,350+16,315+16)
            }
        }
        self.list_ondas = [self.dicc_ondas['onda_1'], self.dicc_ondas['onda_2'], self.dicc_ondas['onda_3'], self.dicc_ondas['onda_4'],
                          self.dicc_ondas['onda_5'], self.dicc_ondas['onda_6'], self.dicc_ondas['onda_7'], self.dicc_ondas['onda_8'], self.dicc_ondas['onda_9'], self.dicc_ondas['onda_10']]
        self.dicc_basura={
            "basura_1": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (210, 175,210+16,175+16)
            },
            "basura_2": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (210, 210,210+16,210+16)
            },
            "basura_3": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (210, 245,210+16,245+16)
            },
            "basura_4": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (210, 280,210+16,280+16)
            },
            "basura_5": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (210, 315,210+16,315+16)
            },
            "basura_6": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (390, 175,390+16,175+16)
            },
            "basura_7": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (390, 210,390+16,210+16)
            },
            "basura_8": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (390, 245,390+16,245+16)
            },
            "basura_9": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (390, 280,390+16,280+16)
            },
            "basura_10": {
                "visible" : False,
                "objeto"  : icono_basura,
                "area"    : (390, 315,390+16,315+16)
            }
        }
        self.list_basura = [self.dicc_basura['basura_1'], self.dicc_basura['basura_2'], self.dicc_basura['basura_3'], self.dicc_basura['basura_4'],
                          self.dicc_basura['basura_5'], self.dicc_basura['basura_6'], self.dicc_basura['basura_7'], self.dicc_basura['basura_8'], self.dicc_basura['basura_9'], self.dicc_basura['basura_10']]

        self.dicc_riff = {
            "riff_1": {
                "visible" : False,
                "texto"   : "Riff_Uno",
                "objeto"  : riff_1,
                "area"    : (95, 175)
            },
            "riff_2": {
                "visible" : False,
                "texto"   : "Riff_Dos",
                "objeto"  : riff_2,
                "area"    : (95, 210)
            },
            "riff_3": {
                "visible" : False,
                "texto"   : "Riff_Tres",
                "objeto"  : riff_3,
                "area"    : (95, 245)
            },
            "riff_4": {
                "visible" : False,
                "texto"   : "Riff_Cuatro",
                "objeto"  : riff_4,
                "area"    : (95, 280)
            },
            "riff_5": {
                "visible" : False,
                "texto"   : "Riff_Cinco",
                "objeto"  : riff_5,
                "area"    : (95, 315)
            },
            "riff_6": {
                "visible" : False,
                "texto"   : "Riff_Seis",
                "objeto"  : riff_6,
                "area"    : (270, 175)
            },
            "riff_7": {
                "visible" : False,
                "texto"   : "Riff_Siete",
                "objeto"  : riff_7,
                "area"    : (270, 210)
            },
            "riff_8": {
                "visible" : False,
                "texto"   : "Riff_Ocho",
                "objeto"  : riff_8,
                "area"    : (270, 245)
            },
            "riff_9": {
                "visible" : False,
                "texto"   : "Riff_Nueve",
                "objeto"  : riff_9,
                "area"    : (270, 280)
            },
            "riff_10": {
                "visible" : False,
                "texto"   : "Riff_Diez",
                "objeto"  : riff_10,
                "area"    : (270, 315)
            },
            "procesando": {
                "visible" : False,
                "texto"   : "procesando",
                "objeto"  : procesando,
                "area"    : (565, 450)
            }
        }
        self.list_riff = [self.dicc_riff['riff_1'], self.dicc_riff['riff_2'], self.dicc_riff['riff_3'], self.dicc_riff['riff_4'],
                          self.dicc_riff['riff_5'], self.dicc_riff['riff_6'], self.dicc_riff['riff_7'], self.dicc_riff['riff_8'], self.dicc_riff['riff_9'], self.dicc_riff['riff_10'], self.dicc_riff['procesando']]

        self.hilo1 = threading.Thread(target=process.main , args=(self.list_riff,))

        self.controlador_gui(True)  ## debe de ir de ultimo...



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

        self.segundo = self.segundo + interfaz.temporizador(0.2) ## contador de 1 segundo

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

    def gui_lista_grabaciones(self,alterar,lista):
        i=0
        while ( i < len(lista)):
            if not lista[i]['visible'] and lista[i]['texto'] != 'procesando':
                if alterar :
                    lista[i]['visible']            = True
                    self.list_basura[i]['visible'] = True
                    self.list_ondas[i]['visible']  = True                   

                return lista[i]['texto']  
            i+=1
        return "limite"

    def iteracion_carga(self):        
        
        if self.segundo == 0:
            self.dicc_cargar['cargar_1']['visible'] = True
            self.dicc_cargar['cargar_2']['visible'] = False 
            self.dicc_cargar['cargar_3']['visible'] = False
            self.dicc_cargar['cargar_4']['visible'] = False        
        elif self.segundo == 1 :
            self.dicc_cargar['cargar_1']['visible'] = False
            self.dicc_cargar['cargar_2']['visible'] = True 
            self.dicc_cargar['cargar_3']['visible'] = False
            self.dicc_cargar['cargar_4']['visible'] = False              
        elif self.segundo == 2 :
            self.dicc_cargar['cargar_1']['visible'] = False
            self.dicc_cargar['cargar_2']['visible'] = False 
            self.dicc_cargar['cargar_3']['visible'] = True
            self.dicc_cargar['cargar_4']['visible'] = False              

        elif self.segundo == 3 :
            self.dicc_cargar['cargar_1']['visible'] = False
            self.dicc_cargar['cargar_2']['visible'] = False 
            self.dicc_cargar['cargar_3']['visible'] = False
            self.dicc_cargar['cargar_4']['visible'] = True
            self.segundo = -1
        self.segundo = self.segundo + interfaz.temporizador(0.3)

    def controlador_gui(self, iniciar):
        
        bandera_procesar = False

        while iniciar:

            self.window.blit(self.fondo, (0, 0))    

            if   self.act_grabar_traslacion:
                 self.accion_grabar_traslacion()
            elif self.act_grabar_conteo:       
                 self.accion_grabar_conteo()                 
            
            elif self.gui_lista_grabaciones(False,self.list_riff)  == "limite":
                    self.dicc_boton ['parar'] ['visible'] = False
                    self.dicc_boton ['grabar']['visible'] = False
                    self.dicc_iconos['parar'] ['visible'] = False
                    self.dicc_iconos['grabar']['visible'] = False
                    self.dicc_boton['generar']['visible'] = True
                    if  bandera_procesar :
                        self.dicc_boton['generar']['visible'] = False
                    self.dibujar(self.lis_boton_grab)
          
            elif self.dicc_boton['parar']['visible'] :         
               
                    self.funcion_grabar_parar(self.gui_lista_grabaciones(True,self.list_riff))
                    # Vovel al estado de Grabacion
                    self.dicc_boton ['parar'] ['visible'] = False
                    self.dicc_boton ['grabar']['visible'] = True
                    self.dicc_iconos['parar'] ['visible'] = False
                    self.dicc_iconos['grabar']['visible'] = True
                    self.dicc_boton['generar']['visible'] = False
            else:
                if not bandera_procesar :
                    self.dicc_boton['generar']['visible'] = self.comprobar_riff()
                self.dibujar(self.lis_boton_grab)
            
            ## CONDICIONES PARA PINTAR LA ITERACION DE LA CARGA
            if bandera_procesar:
                self.dicc_boton['generar']['visible'] = False
                self.dibujar(self.lis_boton_grab)
                self.iteracion_carga()


            ## Dibuje encima
            self.dibujar(self.list_riff)
            self.dibujar(self.list_iconos)
            self.dibujar(self.list_ondas)
            self.dibujar(self.list_basura)


            for event in pygame.event.get():
                #print(str(event)+ '\n')

                #si pulsan la X
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    mouse = event.pos
                    
                    # Area Del Boton Grabar
                    if  self.dicc_boton['grabar']['visible']:
                        if      (mouse[0] > self.dicc_boton['grabar']['area'][0])\
                            and (mouse[0] < self.dicc_boton['grabar']['area'][2])\
                            and (mouse[1] > self.dicc_boton['grabar']['area'][1])\
                            and (mouse[1] < self.dicc_boton['grabar']['area'][3]):                            

                            self.dicc_boton['grabar']['visible'] = False
                            self.dicc_iconos['grabar']['visible'] = False
                            self.dicc_boton['generar']['visible'] = False
                            self.act_grabar_traslacion = True
                            #self.dicc_boton['parar']['visible'] = True
                   
                    # Generar 
                    if  self.dicc_boton['generar']['visible']:
                        if      (mouse[0] > self.dicc_boton['generar']['area'][0])\
                            and (mouse[0] < self.dicc_boton['generar']['area'][2])\
                            and (mouse[1] > self.dicc_boton['generar']['area'][1])\
                            and (mouse[1] < self.dicc_boton['generar']['area'][3]):                            

                            self.dicc_boton['grabar']['visible'] = False
                            self.dicc_iconos['grabar']['visible'] = False
                            self.dicc_boton['generar']['visible'] = False
                            self.dicc_riff['procesando']['visible']= True 
                            bandera_procesar = True
                            

                            self.hilo1.start()


                    # Area de Iconoass Basura (eliminar)
                    indice=0
                    while indice < len(self.list_basura) :
                        # si esta en el area de cualquier icono basura visible 
                        if self.list_basura[indice]['visible']: 
                            if      (mouse[0] > self.list_basura[indice]['area'][0])\
                                and (mouse[0] < self.list_basura[indice]['area'][2])\
                                and (mouse[1] > self.list_basura[indice]['area'][1])\
                                and (mouse[1] < self.list_basura[indice]['area'][3]):

                                self.list_basura [indice] ['visible'] = False
                                self.list_ondas  [indice] ['visible'] = False
                                self.list_riff   [indice] ['visible'] = False

                                self.dicc_boton  ['grabar']['visible'] = True
                                self.dicc_iconos ['grabar']['visible'] = True
                            
                            if      (mouse[0] > self.list_ondas[indice]['area'][0])\
                                and (mouse[0] < self.list_ondas[indice]['area'][2])\
                                and (mouse[1] > self.list_ondas[indice]['area'][1])\
                                and (mouse[1] < self.list_ondas[indice]['area'][3]):

                                self.reproductor( (self.list_riff[indice]['texto']+".wav"), indice)

                        indice+=1
            
            
            self.dibujar(self.list_iconos_cargar)         
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
    
    def funcion_graficar(self,riff_numero):

        fig = pylab.figure(figsize=[2, 2], # Inches
                        dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                        )


        sampleFreq, myRecording = scipy.io.wavfile.read("grabaciones/" +riff_numero)
        sampleDur = len(myRecording)/sampleFreq
        timeX = np.arange(0,sampleDur, 1/sampleFreq)

        ax = fig.gca()
        ax.plot( timeX , myRecording)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()


        #pygame.init()

        #window = pygame.display.set_mode((600, 400), DOUBLEBUF)
        screen = pygame.display.get_surface()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        #screen.blit(surf, (0,0))
        
        pygame.display.flip()
        """
        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
        """
    
    def reproductor(self, riff_numero , indice ):

        #self.funcion_graficar(riff_numero)
        ## REPRODUCTOR ##
        bandera_reproductor= True
        chunk = 1024 
        f = wave.open(("grabaciones/")+riff_numero,'rb')
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
            #print("\n bandera_reproductor ___________________________________")
            """for event in pygame.event.get():    
                    print("\n EVENTO ---------- ")
            
                    if  event.type == MOUSEBUTTONUP:
                        mouse = event.pos                                           
                        if      (mouse[0] > self.list_ondas[indice]['area'][0])\
                            and (mouse[0] < self.list_ondas[indice]['area'][2])\
                            and (mouse[1] > self.list_ondas[indice]['area'][1])\
                            and (mouse[1] < self.list_ondas[indice]['area'][3]):     

                            bandera_reproductor = False
                            break
                        print("\n\n\n MOUSE ", mouse)
            """
            stream.write(data)  
            data = f.readframes(chunk) 
            #bandera_reproductor = False 
        print("\n Reproduccion Terminada")
        #PARAMOS "stream".  
        stream.stop_stream()  
        stream.close()  

        #FINALIZAMOS PyAudio  
        p.terminate()
    
    def comprobar_riff (self):
        for riff in self.list_riff:
            if riff['visible'] and riff['texto'] != 'procesando':
                return True
        return False
interfaz()
