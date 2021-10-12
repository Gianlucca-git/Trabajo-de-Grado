
import essentia

import IPython.display as ipd
import numpy
import numpy as np

import matplotlib.pyplot as plt
from essentia.standard import *
import warnings 
warnings.filterwarnings('ignore')



#CARGO EL ARCHIVO.WAV 

Archivo = 'monos_ebrios.wav'
Audio = MonoLoader(filename=Archivo)()
print("\n\n     EMPIEZA 0  \n\n")

##  FUNCION PARA EXTRAER LOS BEATS POR MINUTOS DEL ARCHIVO  
##  CON ESTO PODREMOS LUEGO VALIDAR LOS COMPACES 


rhythm_extractor = RhythmExtractor2013(method="multifeature")
bpm, beats, b_conf, _, _ = rhythm_extractor(Audio)

print("BPM:", bpm)

print ("Primer Beat en el segundo ->", beats[0] )
print ("Ultimo Beat en el segundo ->", beats[len(beats)-1] )
print("beats Detectados ->", len(beats) )##picos de grafica 

print("Beat positions (sec.):", beats)
print("Beat estimation confidence:", b_conf)

#################################################################

## FUNCION PARA EXTRAER TODOS LOS TIEMPOS Y VALORES DE LAS NOTAS EXISTENTES 
loader = EqloudLoader(filename= Archivo, sampleRate=(48000))

print("\n\nDuracion del audio en total [seg]: {}".format(len(Audio)/44100.0))

pitch_extractor = PredominantPitchMelodia(frameSize=1024, hopSize=512) ## lista de todos los tiempos
pitch_values, pitch_confidence = pitch_extractor(Audio) ## lista de todos los valores en el tiempo

# Pitch is estimated on frames. Compute frame time positions
pitch_times = np.linspace(0.0,len(Audio)/44100.0,len(pitch_values) )


#################################################################

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
t_notas_detectadas = onsets(essentia.array([ pool['features.complex'] ]),[ 1 ])

##tiempos.index (1.4628571428571429)

print (len (pitch_times),"Cantidad de todas las notas detectadas",
len (pitch_values))


################################################################################

import math

## funcion auxiliar para truncar a 7 decimales sin perder o modificar datos relevantes
def trunque (valores, pitch_times ):
    
   
    largo= len(valores)
    i=0
    for v in pitch_times:
 #    tiempos.append( trunque (valores) )
        a=str(v)
        a=a[:largo]
        if (a==valores):
            return i
        
        i+=1
        #print(valores)
    
    return "error" 

#plt.figure(figsize=(16,16))

## FUNCION PARA OBSERVAR LOS VALORES DE LOS TONOS EN UN ARRAY 
#for valores in pitch_values:
 #   print(valores)

## multiplicamos cada valor por 10000000 para no usar round (que aproxima valores por defecto)
## con esto garantizamos trabajar con los suficientes decimales pasados a enteros sin modificar ninguno aproximandolo

tiempos= []
for valores_tiempo in pitch_times:
    tiempos.append(valores_tiempo)
        
    #print(valores_tiempo)

#for valores in tiempos:      
 #   print(valores)
    
#del (pitch_times)

indice_tiempos= []
notas_segun_indice= []
promedio_notas=[]
i= 0

print ("tiempos en segundos en los que ocurren las notas detectadas por libreria")
print()
print (t_notas_detectadas)

print ("\n notas detectadas por libreria ->",len (t_notas_detectadas))

while (len(t_notas_detectadas)!= i):
    
    corte= str(t_notas_detectadas[i]) ## definimos para cortar el string 
    indice_tiempos.append(trunque (corte[:len(corte)-1], pitch_times) )
    valor_de_la_nota= pitch_values[indice_tiempos[i]]
    notas_segun_indice.append(valor_de_la_nota)
    
    
    ## esto es para sacar la media a las nota... se suman las 
    ## 50 notas futuras y se les saca media para aproximar mejor su valor
    
    j=0
    suma=0
    promedio=1
    suma= (float(pitch_values[(indice_tiempos[i])+j]))*1
    
    while(j<10):
                
        if(float (valor_de_la_nota) >70.0):   ### 70 es por la frecuencia mas baja que aceptare 
            
            #print("entro     " , valor_de_la_nota,"  ->>> ", j , "numero ->>>", i )
            valor_de_la_nota= float(pitch_values[(indice_tiempos[i])+j])
            suma=suma+ valor_de_la_nota 
            promedio+=1
            
        else: 
            #print ("else\n\n\n\n")
            valor_de_la_nota= float(pitch_values[(indice_tiempos[i])+j])
            j+=1
        j+=1
        
    valor_de_la_nota=0
    promedio= suma/promedio
    promedio_notas.append(round (promedio ,2))
    
    i+=1

print ()
# ahora ya sabremos en que indice ocurre cada nota  a razon del pitch_time
#
print ("indice de las notas detectadas:\n\n", indice_tiempos)

print ()


print ("Valor de las notas detectadas\nse ve que estan mal!!! \n\n", notas_segun_indice)

print (len (notas_segun_indice))
print ()
print ("promedio de las notas")
print ()
print (promedio_notas)


Mis_notas=[ 164.81 , "error" , 196 , 196 , 196 , 174.61 , 174.61 , 196 , 196,
            "error", 164.81 , "error", 196 , 196 , 196 , 174.61 , 174.61 , "error" ,196 , 196,
            "error" , 164.81  , 196 , 196 , 196 ,"error" , 174.61 , 174.61 ,"error", 196 , 196,
            "error" , 164.81  ,"error", 196 , 196 , 196 , 174.61 , 174.61 , "error", 196 , 196 , 164.81]

## FUNCION PARA OBSERVAR TOOODO

i=0 
for _ in Mis_notas:
    
    print("verdad-> ", Mis_notas[i] , "  detectada-> ", notas_segun_indice[i]," en i_t= ",indice_tiempos[i], "  promedio-> ", promedio_notas[i])
    print()
    if (i==8)or (i==19)or (i==30)or(i==41):
        print("\n\nFINAL DEL COMPAS\n\n") 
    i+=1

redonda=4
blanca =2
negra  =1 
corchea=1/2
semi_corchea= 1/4
fuza= 1/8 


semi_fuza = 1/16

tiempo_real = [fuza ,semi_corchea ,corchea , negra ,  blanca , redonda ] 



t_notas_detectadas_depuradas = []
i,diferencia = 0 , 0  

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
        
    elif (diferencia_promedios_actual < diferencia_promedios_siguiente ):
        
        t_notas_detectadas_depuradas.append(t_notas_detectadas[i])        
        i+=1 
        
    i+=1    

else: t_notas_detectadas_depuradas.append(t_notas_detectadas[i])    
    

    
#print (Notas_detectadas)
print ("notas detectadas ->", len (t_notas_detectadas))

#print (Notas_detectadas_depuradas)
print ("notas detectadas depuradas ->", len (t_notas_detectadas_depuradas))

## notas musicales en el diapason 

mi    = [82.41,164.81,329.63]
fa    = [87.31,174.61,349.23]
fa_s  = [92.50,185.00,369.99]
sol   = [98.00,196.00,392.00]
sol_s = [103.83,207.65,415.30]
la    = [110.00,220.00,440.00]
la_s  = [116.54,233.08,466.00]
si    = [123.47,246.94,493.88]
do    = [130.81,261.63,523.25]
do_s  = [138.59,277.18,554.37]
re    = [146.83,293.66,587.33]
re_s  = [155.56,311.13,622.25]

escala = [ 82.41 , 87.31, 92.50, 98.00,103.83 , 110.00, 116.54,123.47, 130.81,138.59, 146.83, 155.56,
          164.81, 174.61,185.00 , 196.00, 207.65, 220.00, 233.08, 246.94, 261.63,  277.18, 293.66,311.13,
          329.63,349.23,369.99, 392.00, 415.30, 440.00,466.00, 493.88, 523.25, 554.37,  587.33, 622.25 ]

i = 0
notas_finales_reales = []
while (i< len(promedio_notas)):
    j = 1
    while (j < len(escala)):
        
        if (promedio_notas[i]< escala[j-1]):
            
            diferencia_uno= abs (escala[j-1]-promedio_notas[i])
            diferencia_dos= abs (escala[j]-promedio_notas[i])
            
            if (diferencia_uno < diferencia_dos ):
            
                notas_finales_reales.append(escala[j-1])
                j=len(escala)
                
            else: 
                
                notas_finales_reales.append(escala[j])
                j=len(escala)
                
        else: j+=1
    i+=1
    
print (promedio_notas)
print ('')
print (notas_finales_reales)
print ('')
print (Mis_notas)
print ('')
print (escala)

print("\n\n     termina\n\n")
