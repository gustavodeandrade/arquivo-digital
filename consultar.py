import os
import glob
from tkinter import *
import tkinter.messagebox

servidor = "\\\\10.1.1.254\\c"

def ver_consulta(arquivo):
    os.system('"' + arquivo + '"')

def consultar(apelido,obrigacao,mes,ano,extensao):
    arquivo_gerado = apelido + "." + obrigacao + "." + mes + "." + ano + ".pdf"
    diretorio_empresa = servidor + "\\" + "PDFs" + "\\" + apelido + "\\" + ano + "\\" + obrigacao + "\\"

    caminho_completo =  diretorio_empresa + arquivo_gerado

    if obrigacao in ("ISS", "SINTEGRA"):
        arq_gerados = apelido + "." + obrigacao + "-*" + "." + mes + "." + ano + ".pdf"
        lista = []

        for arq_encontrado in glob.glob(diretorio_empresa + "\\" + arq_gerados):
            lista.append(os.path.basename(arq_encontrado))

        if len(lista) > 0:
            if tkinter.messagebox.askyesno("Consulta", "Arquivo(s) salvo(s):\n\n%s\n\nDeseja vê-lo(s)?" % lista):
                return os.system("start " + diretorio_empresa)
        else:
            tkinter.messagebox.showinfo("Consulta", "Não há arquivo(s) salvo(s).")

    elif os.path.exists(caminho_completo):
        #print("O arquivo já existe")
        #tkinter.messagebox.showinfo("Consulta", "O arquivo já foi salvo")
        if tkinter.messagebox.askyesno("Consulta", "O arquivo já foi salvo. Deseja vê-lo?"):
            return ver_consulta(caminho_completo)
    else:
        #print("Esse arquivo ainda não existe")
        tkinter.messagebox.showinfo("Consulta", "Esse arquivo ainda não foi salvo")
