class tab():

    def __init__(self):
        super().__init__()
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

        self.cuerdas = {
                    
        'sexta' : [82.41 , 87.31, 92.50, 98.00,103.83 , 110.00, 116.54,123.47, 130.81,138.59, 146.83, 155.56,164.81, 174.61,185.00 , 196.00, 207.65, 220.00, 233.08, 246.94],
        
        'quinta' :[110.00, 116.54,123.47, 130.81,138.59, 146.83, 155.56,164.81, 174.61,185.00 , 196.00, 207.65, 220.00, 233.08, 246.94, 261.63,  277.18, 293.66,311.13,329.63],
        
        'cuarta' : [146.83, 155.56,164.81, 174.61,185.00 , 196.00, 207.65, 220.00, 233.08, 246.94, 261.63,
                        277.18, 293.66,311.13,329.63,349.23,369.99, 392.00, 415.30, 440.00],
        'tercera' : [196.00, 207.65, 220.00, 233.08, 246.94, 261.63,
                        277.18, 293.66,311.13,329.63,349.23,369.99, 392.00, 415.30, 440.00,466.00, 493.88,
                        523.25, 554.37,  587.33],
        'segunda' : [ 246.94, 261.63,
                        277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00,466.00, 493.88,
                        523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99],
        'primera' : [329.63, 349.23, 369.99, 392.00, 415.30, 440.00,466.00, 493.88,
                        523.25, 554.37, 587.33, 622.25, 659.26, 698.46, 739.99, 783.99, 830.61, 880.00,
                        932.33, 987.77]
        }
        self.diapason = ['sexta','quinta','cuarta','tercera','segunda','primera']
        self.tablatura=[]
        self.notas_buscadas = 0
        #self.main()
        
    def primera_nota(self,notas,notas_buscadas):
        if notas != []:
             
            limite_diapason = 9
            bandera =False
            añadio = True
            self.notas_buscadas = notas_buscadas
            nota= notas[0] ## tomamos la primera nota para empezar a buscar donde poncharla en la tab
            if nota<= 987.77 and nota>=82.41 : ## si la nota esta en el diapason

                for cuerda in self.diapason:
                    i= 0
                    if cuerda == 'tercera':
                        limite_diapason =11
                    if cuerda == 'segunda ':
                        limite_diapason = 15
                    if cuerda == 'primera':
                        limite_diapason = 19
                
                    while i <= limite_diapason :    
                            
                        if nota == self.cuerdas[cuerda][i]:
                            self.tablatura.append([cuerda , str(i)])
                            bandera = True
                            añadio  = True
                            break
                        elif  cuerda == 'primera':
                            limite_diapason=19    
                        
                        else: 
                            añadio = False
                        i+=1

                    if bandera: ## condicion para terminar de buscar
                        break

            else:
                self.tablatura.append(['error' , 'X'])
                self.primera_nota(notas[1:],notas_buscadas +1) 
            if not añadio : 
                self.tablatura.append(['error' , 'X'])
                self.primera_nota(notas[1:],notas_buscadas +1)
            
            return True
        else: 
            return False

    def f_escoger_candidata(self, nota_anterior,candidatas):
        nota_ganadora= 0 
        pivote_cuerda = self.diapason.index(nota_anterior[0]) +1  ## muestre el indice donde esta la cuerda de la nota anterior 
        pivote_valor = int (nota_anterior[1]) ## da el indice donde esta la nota 
        suma = 8000

        for nota in candidatas:
            actual_cuerda = self.diapason.index(nota[0]) +1  ## muestre el indice donde esta la cuerda de la nota anterior 
            actual_valor = nota[1] ## da el indice donde esta la nota 

            suma_aux = abs ((pivote_cuerda - actual_cuerda) * (1.2) )+  abs (pivote_valor - actual_valor )

            if suma >= suma_aux :
                suma = suma_aux
                nota_ganadora = nota

        return nota_ganadora

    def armar_tab (self,notas,nota_anterior ):
        
        # print('nota_anterior ',nota_anterior)
        if notas == []:
            # print (" IF 1", notas)
            return 0
        else:            
            ## condicion para verificar si la nota es valida o no
            ## aprovechando el metodo de la primera_nota 
            ## que debe resivir un arreglo, por lo tanto le envio un arreglo de uno 
            if not self.primera_nota([notas[0]],1) :
               return 0
            nota_actual = self.tablatura.pop()
            if nota_actual[0] == 'error' : ## si la nota es un error, anexela y sigamos con la siguiente en la otra iteracion
                self.tablatura.append(nota_actual)


            ## LOGICA PARA INSERTAR LA NOTA MAS CERCANA ----------------------------------------
            else:

                if nota_actual == nota_anterior :  ## si sigue tocando la misma nota
                    self.tablatura.append(nota_actual)
                else :
                    candidatas= [] ## BUSCAMOS TODOS LOS CANDIDATOS 
                    for cuerda in self.diapason:
                        n_traste = 0   
                        for nota in self.cuerdas[cuerda] :
                            ## si el valor de la nota actual es igual a nota de la cuarda del primer for 
                            if self.cuerdas[nota_actual[0]][int (nota_actual[1])] == nota:
                                candidatas.append([cuerda, n_traste])
                                break
                            if self.cuerdas[nota_actual[0]][int (nota_actual[1])] < nota:
                                break
                            n_traste +=1
                    #print()
                    #print(candidatas)
                    nota_actual = self.f_escoger_candidata(nota_anterior,candidatas)
                    self.tablatura.append(nota_actual)
                    #print()
                        
            ## Fin LOGICA -----------------------------------------------------------------------
            #print  ('nota_actual ' , nota_actual)
 
                
            if nota_actual[0] != 'error': ## condicion para mantener la nota anterior y actual actualizadas
                nota_anterior  =  nota_actual       
            self.armar_tab(notas[1:],nota_anterior)

    def main(self, notas):              
        
        self.primera_nota(notas,1) ## modifica la tablatura hasta encontrar una primera nota
        self.armar_tab(notas[self.notas_buscadas:], self.tablatura[len(self.tablatura) -1] ) 
        #print ( "FINAL ->>> ", self.tablatura)
        return self.tablatura

# caso de prueba completo
#tab().main([233.27, 388.9, 0.0, 959.7, 890.27, 1081.74, 1066.41, 1096.6, 1015.16, 1111.09, 1088.59, 947.62, 1038.8, 898.42, 598.66, 200.87, 0.0, 0.0])
    #[00 ,123.47,4,4,261.63 , 349.23, 196.0, 174.61, 174.61, 185.0, 196.0, 185.0, 185.0, 196.0, 196.0, 174.61, 174.61, 185.0, 196.0, 174.61, 196.0, 185.0, 196.0, 174.61, 174.61, 196.0, 196.0, 174.61, 196.0, 196.0, 196.0, 174.61, 174.61, 196.0, 196.0, 174.61])
# caso de prueba de las notas mas cercanas 
    # tab().f_escoger_candidata(['sexta', '7'], [['quinta', 15], ['cuarta', 10], ['tercera', 5], ['segunda', 0]])