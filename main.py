from  PyPDF2 import PdfReader, PdfWriter
import random
import re
padrao_cpf = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')
cpf_final = ""
with open('Informes 2024', 'rb') as arq:
    read_pdf = PdfReader(arq)
    
    texto = ""
    pagum = ""
    pag_ant = ""
    ultpag = ""

    def newPdf(p1, p2, tipo):
        if (tipo == 'uni'):

            # Pegar a linha que tem o CPF da pessoa
            txt = p1.extract_text()
            linha = 0
            for t in txt.split("\n"):
                if (linha == 14):
                    cpf_extraido = padrao_cpf.findall(t)
                    print(cpf_extraido)
                linha += 1 
            cpf_final = [re.sub(r'\D', '', cpf) for cpf in cpf_extraido]

            # agrupar as paginas
            writer = PdfWriter()
            for p in [p1,p2]:
                writer.add_page(p)

            # Criar o pedf
            with open(f"{cpf_final[0]}.pdf", "wb") as out_pdf:
                writer.write(out_pdf)
            
        else:
            writer = PdfWriter()
            
            # Pegar a linha que tem o CPF da pessoa
            txt = p1.extract_text()
            linha = 0
            for t in txt.split("\n"):
                if (linha == 14):
                    cpf_extraido = padrao_cpf.findall(t)
                    print(cpf_extraido)
                linha += 1 
            cpf_final = [re.sub(r'\D', '', cpf) for cpf in cpf_extraido]

            # Adiciona a pagina ao criador de PDF
            writer.add_page(p1)
            
            with open(f"{cpf_final[0]}.pdf", "wb") as out_pdf:
                writer.write(out_pdf)
                
    for pag in read_pdf.pages:
        texto = pag.extract_text()
        ultima_linha = len(texto.split("\n"))
        texto_pag = texto.split("\n")[ultima_linha-1]


        if (texto_pag == "Pág. 1" and len(pagum) == 0):
            pagum = pag
        elif (texto_pag == "Pág. 1" and len(pagum) > 0):
            newPdf(pagum, None, 'sep')
            ultpag = pag
            pagum = ""
        elif (texto_pag == "Pág. 1" and len(ultpag) > 0):
            newPdf(ultpag, None, 'sep')
            ultpag = ""
        elif (texto_pag == "Pág. 2" and len(ultpag) > 0):
            newPdf(ultpag, pag, 'uni')
            pagum = ""
            ultpag = ""
        elif (texto_pag == "Pág. 2" and len(pagum) > 0):
            newPdf(pagum, pag, 'uni')
            pagum = "" 
