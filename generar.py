
import essentia
import math
import IPython.display as ipd
import numpy
import numpy as np
import matplotlib.pyplot as plt
from essentia.standard import CartesianToPolar,FrameGenerator,Onsets,FFT,Windowing,OnsetDetection,MonoLoader,RhythmExtractor2013,EqloudLoader,PredominantPitchMelodia
import warnings 
warnings.filterwarnings('ignore')


class process ():

    def f_audio (riff):
        #CARGO EL ARCHIVO.WAV 
        Archivo = 'grabaciones/' + riff
        Audio = MonoLoader(filename=Archivo)()
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
        return bpm,  len(beats) 
        
    def f_extractor_times_and_notes(Audio,Archivo):

        ## FUNCION PARA EXTRAER TODOS LOS TIEMPOS Y VALORES DE LAS NOTAS EXISTENTES 
        loader = EqloudLoader(filename= Archivo, sampleRate=(48000))
        duracion = format(len(Audio)/44100.0)
        #print("\n\nDuracion del audio en total [seg]: ", duracion) 
        pitch_extractor = PredominantPitchMelodia(frameSize=1024, hopSize=512) ## lista de todos los tiempos
        all_notes, pitch_confidence = pitch_extractor(Audio) ## lista de todos los valores en el tiempo

        # Pitch is estimated on frames. Compute frame time positions
        all_times = np.linspace(0.0,len(Audio)/44100.0,len(all_notes) )
        return {'all_times':all_times,'all_notes':all_notes}
        #print (len (all_times),"nada",len (all_notes))

## funcion auxiliar para truncar a 7 decimales sin perder o modificar datos relevantes
    def trunque (valores, pitch_times ):    
        largo= len(valores)
        i=0
        for v in pitch_times:
            a=str(v)
            a=a[:largo]
            if (a==valores):
                return i            
            i+=1
            #print(valores)        
        return "error"     

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
        tiempos_detectados_essentia = onsets(essentia.array([ pool['features.complex'] ]),[ 1 ])
        #print(tiempos_detectados_essentia)
        return tiempos_detectados_essentia
    ## consiste en sacar el promedio por atras y por delante de una nota
    def primera_depuracion(tiempos_detectados_essentia,all_extractor):
        # FUNCION PARA ASOCIAR EL INDICE DONDE ESTA CADA TIEMPO EN patch_times
        # hay garantia de que los datos de t_notas_detectadas existe en lista tiempos

        indice_tiempos= []
        notas_segun_indice= []
        promedio_notas=[]
        i= 0

        #print ("tiempos en segundos en los que ocurren las notas detectadas por libreria")
        #print()
        #print (tiempos_detectados_essentia)
        #print ("\n notas detectadas por libreria ->",len (tiempos_detectados_essentia))

        while (len(tiempos_detectados_essentia)!= i):
            
            corte= str(tiempos_detectados_essentia[i]) ## definimos para cortar el string 
            indice_tiempos.append(process.trunque (corte[:len(corte)-1], all_extractor['all_times']) )
            valor_de_la_nota= all_extractor['all_notes'][indice_tiempos[i]]
            notas_segun_indice.append(valor_de_la_nota)
            
            
            ## esto es para sacar la media a las nota... se suman las 
            ## 50 notas futuras y se les saca media para aproximar mejor su valor
            
            j=0
            suma=0
            promedio=1
            suma= (float(all_extractor['all_notes'][(indice_tiempos[i])+j]))*1
            
            while(j<10):
                        
                if(float (valor_de_la_nota) >70.0):   ### 70 es por la frecuencia mas baja que aceptare 
                    
                    #print("entro     " , valor_de_la_nota,"  ->>> ", j , "numero ->>>", i )
                    valor_de_la_nota= float(all_extractor['all_notes'][(indice_tiempos[i])+j])
                    suma=suma+ valor_de_la_nota 
                    promedio+=1
                    
                else: 
                    #print ("else\n\n\n\n")
                    valor_de_la_nota= float(all_extractor['all_notes'][(indice_tiempos[i])+j])
                    j+=1
                j+=1
                
            valor_de_la_nota=0
            promedio= suma/promedio
            promedio_notas.append(round (promedio ,2))
            
            i+=1

        #print ()
        # ahora ya sabremos en que indice ocurre cada nota  a razon del pitch_time
        #
        #print ("indice de las notas detectadas:\n\n", indice_tiempos)

        #print ()


        #print ("Valor de las notas detectadas\nse ve que estan mal!!! \n\n", notas_segun_indice)

        #print (len (notas_segun_indice))
        #print ()
        #print ("promedio de las notas")
        #print ()
        #print (promedio_notas)
        return {'promedio_notas':promedio_notas,'notas_segun_indice':notas_segun_indice}    
    
    ##consiste en quitar las notas extremadamente cercanas  
    def segunda_depuracion(promedio_notas,notas_segun_indice,t_notas_detectadas):
        fuza= 1/8 
        semi_fuza = 1/16

        t_notas_detectadas_depuradas = []
        i,diferencia = 0 , 0  
        indices_que_se_mantienen=[]
        indices_que_se_mantienen.append(promedio_notas[i])
        valor_de_notas_depuradas=[]
        valor_de_notas_depuradas.append(promedio_notas[i])

        ##   NOTA : Se añade el primer tiempo en el que la primera nota fue detectada para poder empezar a comparar.


        ###   FUNCION DE DEPURACION  notas·············································································
        while (len(t_notas_detectadas) > (i + 1)  ):
            
            diferencia_tiempos = abs( t_notas_detectadas[i] - t_notas_detectadas[i+1] )
            
            diferencia_promedios_actual= abs(promedio_notas[i]- notas_segun_indice[i])
            ## siguiente es una sola unidad
            diferencia_promedios_siguiente= abs(promedio_notas[i+1]- notas_segun_indice[i+1])
            #    print(diferencia)
            ## CONDICION PARA NOTAS MUY GRABES o muy AGUDAS
            
            #if(promedio_notas[i]<60):
            #print ("errrrrrrrrorrrrr")
            
            if (diferencia_tiempos > fuza ):
                
                t_notas_detectadas_depuradas.append(t_notas_detectadas[i])
                #print ("entre a guardar->  ",t_notas_detectadas_depuradas[i])
                indices_que_se_mantienen.append(i)
                
                valor_de_notas_depuradas.append(promedio_notas[i+1])
                
            elif (diferencia_promedios_actual < diferencia_promedios_siguiente ):
                
                t_notas_detectadas_depuradas.append(t_notas_detectadas[i])  
                indices_que_se_mantienen.append(i)
                
                valor_de_notas_depuradas.append(promedio_notas[i+1])
                
                i+=1 
                
            i+=1    

        else: t_notas_detectadas_depuradas.append(t_notas_detectadas[i])    
            
        #print ("Valor de notas segun los indices que quedaron",valor_de_notas_depuradas)
        return t_notas_detectadas_depuradas,valor_de_notas_depuradas
        
    def riff_a_procesar(list_riff):
        riff_visibles = []
        for riff in list_riff:
            if riff['visible'] and riff ['texto'] != 'procesando':
                riff_visibles.append(riff['texto'])

        #for nombre in riff_visibles:
        process.f_audio('')

    def main(list_riff):
        p = process
        #print (p.riff_a_procesar(list_riff))
        Audio,Archivo = p.f_audio(list_riff)
        p.f_beats_for_minutes(Audio)        
        
        ## primera_depuracion(tiempos_detectados_essentia,all_times,all_notes)
        t_notas_detectadas = p.f_essentia_extract(Audio)
        all_extractor = p.f_extractor_times_and_notes(Audio,Archivo)

        # d_prome_ind = {'promedio_notas':promedio_notas,'notas_segun_indice':notas_segun_indice} 
        d_prome_ind =  p.primera_depuracion(t_notas_detectadas,all_extractor)

        p.segunda_depuracion(d_prome_ind['promedio_notas'],d_prome_ind['notas_segun_indice'],t_notas_detectadas)

        return True

process.main('monos_ebrios.wav')
