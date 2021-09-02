
import essentia
import math
import IPython.display as ipd
import numpy
from tablatura import tab
import numpy as np
import matplotlib.pyplot as plt
from essentia.standard import CartesianToPolar,FrameGenerator,Onsets,FFT,Windowing,OnsetDetection,MonoLoader,RhythmExtractor2013,EqloudLoader,PredominantPitchMelodia
import warnings 
warnings.filterwarnings('ignore')


class process ():
    
    escala = [ 82.41 , 87.31, 92.50, 98.00,103.83 , 110.00, 116.54,123.47, 130.81,138.59,
                146.83, 155.56,164.81, 174.61,185.00 , 196.00, 207.65, 220.00, 233.08, 246.94, 261.63,
                277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00,466.00, 493.88,
                523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00,
                932.33, 987.77 ]

    def f_audio (riff):
        Archivo = 'grabaciones/' + riff
        Audio = MonoLoader(filename=Archivo)()
        #print ('CARGO EL ARCHIVO.WAV') 
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
        
    def f_extractor_times_and_notes(Audio,Archivo):

        ## FUNCION PARA EXTRAER TODOS LOS TIEMPOS Y VALORES DE LAS NOTAS EXISTENTES 
        loader = EqloudLoader(filename= Archivo, sampleRate=(48000))
        duracion = format(len(Audio)/44100.0)
        #print("\n\nDuracion del audio en total [seg]: ", duracion) 
        pitch_extractor = PredominantPitchMelodia(frameSize=1024, hopSize=512) ## lista de todos los tiempos
        all_notes, pitch_confidence = pitch_extractor(Audio) ## lista de todos los valores en el tiempo

        # Pitch is estimated on frames. Compute frame time positions
        all_times = np.linspace(0.0,len(Audio)/44100.0,len(all_notes) )
        return {'all_times':all_times,'all_notes':all_notes, 'Duracion': duracion}
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
        u= all_extractor['all_notes'][-1]
        all_extractor['all_notes'] = numpy.append(all_extractor['all_notes'],[u,u,u,u,u,u,u,u,u,u,u,u])
        #print ("tiempos en segundos en los que ocurren las notas detectadas por libreria")
        #print()
        #print (tiempos_detectados_essentia)
        #print ("\n notas detectadas por libreria ->",len (tiempos_detectados_essentia))

        while ( i < len(tiempos_detectados_essentia) ):
            
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

        #print('promedio_notas', len(promedio_notas))
        #print('notas_segun_indice', len(notas_segun_indice))
        #print('t_notas_detectadas', len(t_notas_detectadas))

        t_notas_detectadas_depuradas = []
        i,diferencia = 0 , 0  
        indices_que_se_mantienen=[]
        indices_que_se_mantienen.append(promedio_notas[i])
        valor_de_notas_depuradas=[]
        valor_de_notas_depuradas.append(promedio_notas[i])

        ##   NOTA : Se añade el primer tiempo en el que la primera nota fue detectada para poder empezar a comparar.


        ###   FUNCION DE DEPURACION  notas·············································································
        while (len(t_notas_detectadas) > (i+1)  ):
            
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
        else: 
            #print (" PUTO VALOR DE i ->" , i )

            t_notas_detectadas_depuradas.append(t_notas_detectadas[i-1])    
            
        #print ("Valor de notas segun los indices que quedaron",valor_de_notas_depuradas)
        return valor_de_notas_depuradas
    
    ## FUNCION PARA APROXIMAR LAS NOTAS DEPURADAS A NOTAS REALES SEGUN LA ESCALA MUSICAL DE LA GUITARRA
    def tercera_depuracion(valor_de_notas_depuradas):
    
        valor_definitivo_notas = []
        i=0
        diferencia_uno=0
        diferencia_dos=-1
        #print (valor_de_notas_depuradas)
        # NOTA: el 3157894791 es un error por encima o por debajo de la escala
        while (i < len(valor_de_notas_depuradas)):
            
            j=0
            bandera= True
            if (valor_de_notas_depuradas[i]<process.escala[j]): ## si se sale de la escala le asigno un valor muy grande
                valor_definitivo_notas.append(3157894791)
                j=1
                
            while(j< len(process.escala)and(bandera)):        

                if ( process.escala[j] <= valor_de_notas_depuradas[i]):
                    j+=1
                else:
                    bandera=False    
            
            
            if bandera: ## condicion por si la nota sobrepasa la escala
                valor_definitivo_notas.append(3157894791)
            else:
                
                diferencia_uno= abs (valor_de_notas_depuradas[i]-process.escala[j-1])
                diferencia_dos= abs (process.escala[j]-valor_de_notas_depuradas[i])

                if (diferencia_uno<diferencia_dos): ## condicion para mirar que valor de la escala se ajusta mas
                    valor_definitivo_notas.append(process.escala[j-1])
                else : 
                    valor_definitivo_notas.append(process.escala[j]) 
            
            i+=1
        return valor_definitivo_notas

    def riff_a_procesar(list_riff):
        riff_visibles = []
        for riff in list_riff:
            if riff['visible'] and riff ['texto'] != 'procesando':
                riff_visibles.append(riff['texto'])
        
        return riff_visibles

    def controlador(riff):
        p = process
        
        Audio,Archivo = p.f_audio(riff)
        # p.f_beats_for_minutes(Audio)        
        
        ## primera_depuracion(tiempos_detectados_essentia,all_times,all_notes)
        t_notas_detectadas = p.f_essentia_extract(Audio)
        #print ('t_notas_detectadas ', t_notas_detectadas)
        all_extractor = p.f_extractor_times_and_notes(Audio,Archivo)

        # comentario -> d_prome_ind = {'promedio_notas':promedio_notas,'notas_segun_indice':notas_segun_indice} 
        d_prome_ind =  p.primera_depuracion(t_notas_detectadas,all_extractor)

        valor_de_notas_depuradas = p.segunda_depuracion(d_prome_ind['promedio_notas'],d_prome_ind['notas_segun_indice'],t_notas_detectadas)
        return  { 'Respuesta': (tab().main(p.tercera_depuracion(valor_de_notas_depuradas))), 'Duracion': all_extractor['Duracion'] , 'BPM':p.f_beats_for_minutes(Audio) }
        #print(p.tercera_depuracion(valor_de_notas_depuradas))
    
    def main(list_of_dicc_riff):
        riff_procesar = process.riff_a_procesar(list_of_dicc_riff)
        diic_de_respuesta=[]
        for nombre in riff_procesar:
            #print ("NOMBRE ->> ", nombre)
            d = process.controlador(nombre+'.wav')
            diic_de_respuesta.append({
                'Riff': nombre,
                'Respuesta': d['Respuesta'],
                'Duracion': d['Duracion'] ,
                'BPM': d['BPM'] }
                )
        return diic_de_respuesta


"""
print ("TERMINO EXITOSAMENTE", process.main([{
                "visible" : True,
                'texto'   : "Riff_Uno"               

            },
            {
                "visible" : False,
                'texto'   : "Riff_Dos"
            },
            {
                "visible" : True,
                'texto'   : "monos_ebrios"
       }]))
"""
