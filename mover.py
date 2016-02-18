import os
import shutil
#from shutil import copy2
import tkinter.messagebox

def save_log(caminho,arquivo):
    file = open("log.txt", "a")
    file.write("%s\t%s\n" %(caminho,arquivo))
    file.close


def ler_empresas(arquivo):
    empresas = []
    empresas_f = open(arquivo)
    for line in empresas_f:
        empresas.append(line.rstrip())
    return empresas


def mover(arquivo,apelido,obrigacao,mes,ano,extensao, *complemento):

    servidor = "\\\\10.1.1.254\\c"

    arquivos_movidos = []
    empresas_ncad = []
    
    print(arquivo)
    print(apelido)

    if obrigacao in ['ISS', 'SINTEGRA']:
        novo_arquivo = apelido + "." + obrigacao + "-" + complemento[0] + "." + mes + "." + ano + ".pdf"
    else:
        novo_arquivo = apelido + "." + obrigacao + "." + mes + "." + ano + ".pdf"
    print (novo_arquivo)
    #(apelido,obrigacao,mes,ano,extensao) = arquivo.split('.')
    #diretorio = "Servidor" + "\\" + "PDFs" + "\\" + apelido + "\\" + ano + "\\" + obrigacao
    diretorio = servidor + "\\" + "PDFs" + "\\" + apelido + "\\" + ano + "\\" + obrigacao
    #diretorio_empresa = "Servidor" + "\\" + "PDFs" + "\\" + apelido
    diretorio_empresa = servidor + "\\" + "PDFs" + "\\" + apelido
    #diretorio_empresa_ano = "Servidor" + "\\" + "PDFs" + "\\" + apelido + "\\" + ano
    diretorio_empresa_ano = servidor + "\\" + "PDFs" + "\\" + apelido + "\\" + ano
    #if not os.path.exists(diretorio):
    #os.makedirs(diretorio)

    empresas = ler_empresas("empresas.txt")
    
    if apelido in empresas:
        
        if not os.path.exists(diretorio_empresa):
            obrigacoes_f = open("obrigacoes.txt")
            for line in obrigacoes_f: 
                os.makedirs(diretorio_empresa_ano + "\\" + line.rstrip())
            obrigacoes_f.close()
            
        try:
            if arquivo != novo_arquivo:
                shutil.move(arquivo, novo_arquivo)    
                #arquivo = novo_arquivo

            if novo_arquivo not in os.listdir(diretorio):
                shutil.move(novo_arquivo, diretorio)
                save_log(diretorio,novo_arquivo)
                arquivos_movidos.append(novo_arquivo)
            else:
                shutil.move(novo_arquivo, arquivo)
                tkinter.messagebox.showwarning("Arquivo existente", "Já existe um arquivo com os dados informados.")
        except Exception as ex:
            print("Erro: %s" %ex)
            tkinter.messagebox.showerror("Erro", "Não foi possível mover o arquivo.\n\n %s" % ex)
    else:
            empresas_ncad.append(apelido)
            #tkinter.messagebox.showerror("Erro", "Não foi possível mover arquivos da(s) não cadastrada(s).\n\n%s" % empresas_ncad)

    quantidade = len(arquivos_movidos)
            
    if quantidade > 0:
        tkinter.messagebox.showinfo("Arquivos foram movidos", "%d arquivo(s) movido(s)\n\n%s" % (quantidade,arquivos_movidos))
    else:
        tkinter.messagebox.showinfo("Nada a ser movido", "Nenhum arquivo foi movido.")

    print(empresas_ncad) 
    if len(empresas_ncad) > 0:
        tkinter.messagebox.showerror("Não foi possível mover", "Empresa(s) não cadastrada(s):\n\n%s" % empresas_ncad)


