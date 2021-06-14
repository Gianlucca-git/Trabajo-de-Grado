from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('iconos/d_textura.png', 10, 0, 25)

        # Arial bold 15
        self.set_font('Arial', 'B', 11)
        # Move to the right
        self.cell(35)
        # Title
        self.cell(10, 25, 'DOLPHings Tabs!', 30, 30, 'C')
        # Line break
        self.ln(0)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    
    
class armar_pdf():

    def escribir(list_diccionario):
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        for dicc in list_diccionario:
            
            pdf.cell(0, 10, ' Nombre: '+dicc['Riff']+'.               Duración: '+ str(dicc['Duracion'])+' seg.               BPM :'+str(dicc['BPM']), 0, 1)
            i=0
            while i < ( len(dicc['Respuesta'][0]) -10 ):

                pdf.cell(0, 5, 'e         || ----- ' + str(dicc['Respuesta'][0][i])+ ' ----- ' +str(dicc['Respuesta'][0][i+1])+ ' ----- '+str(dicc['Respuesta'][0][i+2])+ ' ----- '+str(dicc['Respuesta'][0][i+3])+ ' ----- '+ str(dicc['Respuesta'][0][i+4])+ ' ----- ' + str(dicc['Respuesta'][0][i+5])+ ' ----- '+ str(dicc['Respuesta'][0][i+6])+ ' ----- '+ str(dicc['Respuesta'][0][i+7])+ ' ----- '+ str(dicc['Respuesta'][0][i+8])+ ' ----- ' + str(dicc['Respuesta'][0][i+9])+ ' ----- | ' , 0, 1)
                pdf.cell(0, 5, 'B        || ----- ' + str(dicc['Respuesta'][1][i])+ ' ----- ' + str(dicc['Respuesta'][1][i+1])+ ' ----- '+str(dicc['Respuesta'][1][i+2])+ ' ----- '+str(dicc['Respuesta'][1][i+3])+ ' ----- '+ str(dicc['Respuesta'][1][i+4])+ ' ----- ' + str(dicc['Respuesta'][1][i+5])+ ' ----- '+ str(dicc['Respuesta'][1][i+6])+ ' ----- '+ str(dicc['Respuesta'][1][i+7])+ ' ----- '+ str(dicc['Respuesta'][1][i+8])+ ' ----- ' + str(dicc['Respuesta'][1][i+9])+ ' ----- | ' , 0, 1)
                pdf.cell(0, 5, 'G        || ----- ' + str(dicc['Respuesta'][2][i])+ ' ----- ' + str(dicc['Respuesta'][2][i+1])+ ' ----- '+str(dicc['Respuesta'][2][i+2])+ ' ----- '+ str(dicc['Respuesta'][2][i+3])+ ' ----- '+ str(dicc['Respuesta'][2][i+4])+ ' ----- ' + str(dicc['Respuesta'][2][i+5])+ ' ----- '+ str(dicc['Respuesta'][2][i+6])+ ' ----- '+ str(dicc['Respuesta'][2][i+7])+ ' ----- '+ str(dicc['Respuesta'][2][i+8])+ ' ----- ' + str(dicc['Respuesta'][2][i+9])+ ' ----- | ' , 0, 1)
                pdf.cell(0, 5, 'D        || ----- ' + str(dicc['Respuesta'][3][i])+ ' ----- ' + str(dicc['Respuesta'][3][i+1])+ ' ----- '+str(dicc['Respuesta'][3][i+2])+ ' ----- '+str(dicc['Respuesta'][3][i+3])+ ' ----- '+ str(dicc['Respuesta'][3][i+4])+ ' ----- ' + str(dicc['Respuesta'][3][i+5])+ ' ----- '+ str(dicc['Respuesta'][3][i+6])+ ' ----- '+ str(dicc['Respuesta'][3][i+7])+ ' ----- '+ str(dicc['Respuesta'][3][i+8])+ ' ----- ' + str(dicc['Respuesta'][3][i+9])+ ' ----- | ' , 0, 1)
                pdf.cell(0, 5, 'A        || ----- ' + str(dicc['Respuesta'][4][i])+ ' ----- ' + str(dicc['Respuesta'][4][i+1])+ ' ----- '+str(dicc['Respuesta'][4][i+2])+ ' ----- '+ str(dicc['Respuesta'][4][i+3])+ ' ----- '+ str(dicc['Respuesta'][4][i+4])+ ' ----- ' + str(dicc['Respuesta'][4][i+5])+ ' ----- '+ str(dicc['Respuesta'][4][i+6])+ ' ----- '+ str(dicc['Respuesta'][4][i+7])+ ' ----- '+ str(dicc['Respuesta'][4][i+8])+ ' ----- ' + str(dicc['Respuesta'][4][i+9])+ ' ----- | ' , 0, 1)
                pdf.cell(0, 8, 'E        || ----- ' + str(dicc['Respuesta'][5][i])+ ' ----- ' + str(dicc['Respuesta'][5][i+1])+ ' ----- '+str(dicc['Respuesta'][5][i+2])+ ' ----- '+ str(dicc['Respuesta'][5][i+3])+ ' ----- '+ str(dicc['Respuesta'][5][i+4])+ ' ----- ' + str(dicc['Respuesta'][5][i+5])+ ' ----- '+ str(dicc['Respuesta'][5][i+6])+ ' ----- '+ str(dicc['Respuesta'][5][i+7])+ ' ----- '+ str(dicc['Respuesta'][5][i+8])+ ' ----- ' + str(dicc['Respuesta'][5][i+9])+ ' ----- | ' , 0, 1)
                    
                pdf.cell(0, 15, 'Error  || ----- ' + str(dicc['Respuesta'][6][i])+ ' ----- ' + str(dicc['Respuesta'][6][i+1])+ ' ----- '+ str(dicc['Respuesta'][6][i+2])+ ' ----- '+ str(dicc['Respuesta'][6][i+3])+ ' ----- '+ str(dicc['Respuesta'][6][i+4])+ ' ----- ' + str(dicc['Respuesta'][6][i+5])+ ' ----- '+ str(dicc['Respuesta'][6][i+6])+ ' ----- '+ str(dicc['Respuesta'][6][i+7])+ ' ----- '+ str(dicc['Respuesta'][6][i+8])+ ' ----- ' + str(dicc['Respuesta'][6][i+9])+  ' ----- | ' , 0, 1)
                i+=10

            numero = abs (i - len(dicc['Respuesta'][0]) )
            e=''
            B=''
            G=''
            D=''
            A=''
            E=''
            Error=''

            j=0
            while j< numero:  ## while para concatenar los ultimos 
                e = e + str(dicc['Respuesta'][0][i+j]) + ' ----- '
                B = B + str(dicc['Respuesta'][1][i+j]) + ' ----- '
                G = G + str(dicc['Respuesta'][2][i+j]) + ' ----- '
                D = D + str(dicc['Respuesta'][3][i+j]) + ' ----- '
                A = A + str(dicc['Respuesta'][4][i+j]) + ' ----- '
                E = E + str(dicc['Respuesta'][5][i+j]) + ' ----- '
                Error = Error + str(dicc['Respuesta'][6][i+j]) + ' ----- '
                j +=1


            pdf.cell(0, 5, 'e          || ----- ' + e  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'B         || ----- ' + B  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'G         || ----- ' + G  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'D         || ----- ' + D  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'A         || ----- ' + A  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'E         || ----- ' + E  + ' ----- | ' , 0, 1)
            pdf.cell(0, 5, 'Error    || ----- ' +  Error + ' ----- | ' , 0, 1)




        pdf.output('TablaturaDolphings.pdf', 'F')

    def dicc_to_pdf(list_diccionario):
        
        for dicc in list_diccionario:
            i=0
            tabs=[[],[],[],[],[],[],[]]
            while i <  len(dicc['Respuesta']):

                if dicc['Respuesta'][i][0] == 'primera':
                    tabs[0].append(dicc['Respuesta'][i][1])
                    tabs[1].append('--')
                    tabs[2].append('--')
                    tabs[3].append('--')
                    tabs[4].append('--')
                    tabs[5].append('--')
                    tabs[6].append('--')
                elif dicc['Respuesta'][i][0] == 'segunda':
                    tabs[0].append('--')
                    tabs[1].append(dicc['Respuesta'][i][1])
                    tabs[2].append('--')
                    tabs[3].append('--')
                    tabs[4].append('--')
                    tabs[5].append('--')
                    tabs[6].append('--')
                elif dicc['Respuesta'][i][0] == 'tercera':
                    tabs[0].append('--')
                    tabs[1].append('--')
                    tabs[2].append(dicc['Respuesta'][i][1])
                    tabs[3].append('--')
                    tabs[4].append('--')
                    tabs[5].append('--')
                    tabs[6].append('--')
                elif dicc['Respuesta'][i][0] == 'cuarta':
                    tabs[0].append('--')
                    tabs[1].append('--')
                    tabs[2].append('--')
                    tabs[3].append(dicc['Respuesta'][i][1])
                    tabs[4].append('--')
                    tabs[5].append('--')
                    tabs[6].append('--')
                elif dicc['Respuesta'][i][0] == 'quinta':
                    tabs[0].append('--')
                    tabs[1].append('--')
                    tabs[2].append('--')
                    tabs[3].append('--')
                    tabs[4].append(dicc['Respuesta'][i][1])
                    tabs[5].append('--')
                    tabs[6].append('--')
                elif dicc['Respuesta'][i][0] == 'sexta':
                    tabs[0].append('--')
                    tabs[1].append('--')
                    tabs[2].append('--')
                    tabs[3].append('--')
                    tabs[4].append('--')
                    tabs[5].append(dicc['Respuesta'][i][1])
                    tabs[6].append('--')
                else:
                    tabs[0].append('--')
                    tabs[1].append('--')
                    tabs[2].append('--')
                    tabs[3].append('--')
                    tabs[4].append('--')
                    tabs[5].append('--')
                    tabs[6].append('X')

                i+=1
            dicc['Respuesta'].clear()
            dicc['Respuesta'].extend (tabs)
            tabs.clear()
        return (list_diccionario)
        

    def main (list_diccionario):
        ##list_diccionario= [{'Riff': 'Riff_Uno', 'Respuesta': [['cuarta', '8'], ['segunda', 8], ['error', 'X'], ['sexta', 0], ['primera', 18], ['primera', 17], ['error', 'X'], ['error', 'X'], ['error', 'X'], ['error', 'X'], ['error', 'X'], ['error', 'X'], ['primera', 18], ['error', 'X'], ['primera', 17], ['segunda', 15], ['sexta', 15], ['error', 'X'], ['sexta', 0], ['error', 'X'], ['sexta', 0]], 'Duracion': 10, 'BPM': 100}, {'Riff': 'monos_ebrios', 'Respuesta': [['sexta', '9'], ['quinta', 9], ['quinta', 10], ['quinta', 10], ['quinta', 8], ['quinta', 8], ['quinta', 9], ['quinta', 10], ['quinta', 9], ['quinta', 9], ['quinta', 10], ['quinta', 10], ['quinta', 8], ['quinta', 8], ['quinta', 9], ['quinta', 10], ['quinta', 8], ['quinta', 10], ['quinta', 9], ['quinta', 10], ['quinta', 8], ['quinta', 8], ['quinta', 10], ['quinta', 10], ['quinta', 8], ['quinta', 10], ['quinta', 10], ['quinta', 10], ['quinta', 8], ['quinta', 8], ['quinta', 10], ['quinta', 10], ['quinta', 8]], 'Duracion': 10, 'BPM': 100}]
        armar_pdf.escribir( armar_pdf.dicc_to_pdf(list_diccionario))

##armar_pdf.main()