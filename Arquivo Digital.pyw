'''
Este programa move os arquivos PDF para um diretório específico no servidor.
Há um padrão para o nome dos arquivos: apelido + "." + obrigacao + "." + mes + "." + ano + ".pdf"

Apelido = Apelido da empresa adotado no sistema da Contmatic.
Obrigação = Nome resumido para a obrigação, por exemplo: ISS, SINTEGRA, NFPAULISTA(Nota Fiscal Pauliista).

Todos as obrigações definidas estão no arquivo "obrigacoes.txt".
Visando a facilidade do programa, as obrigações podem ser selecionadas por setores: Contábil, Fiscal e Pessoal
Essa divisão pode ser vista nos arquivos: obrigacoes_contabil.txt, obrigacoes_fiscal.txt e obrigacoes_pessoal.txt.

28/12/2015    Gustavo     Altera para caixa alta o que foi digitado no campo "Empresa"
28/12/2015    Gustavo     mover.py - Renomeia o arquivo original para o padrão definido.
29/12/2015    Gustavo     consultar.py - Adicionada a função para verificar se um arquivo já foi salvo ou não.
29/12/2015    Gustavo     Setor_Frame posicionado para antes do OptionMenu da obrigação.
30/12/2015    Gustavo     Acrescentada a opção para visualizar arquivo.
30/12/2015    Gustavo     OptionMenu e botão "Visualizar" foram colocados em um único frame.
31/12/2015    Gustavo     Ordenar por ordem alfabética a lista de arquivos a serem movidos.
04/01/2016    Gustavo     Acrescentado os botões de checkbox quando selecionada a opção do setor Fiscal.
20/01/2016    Gustavo     Opções complementares para ISS e SINTEGRA foram incluídas ao tentar mover o arquivo.
20/01/2016    Gustavo     Nova função: limpar(). Limpa o campo empresa e remove o arquivo movido das opções.
20/01/2016    Gustavo     Usando "Toplevel" para a janela das obrigações complementares.
21/01/2016    Gustavo     Definido o diretório "~/Desktop/PDFs" como padrão para a pesquisa dos arquivos a serem movidos.
25/01/2016    Gustavo     Definido o destino dos arquivos para o servidor, na pasta "PDFs-teste". Para o módulo consultar também.
25/01/2016    Gustavo     Função "limpar" testada e aplicada após os arquivos serem movidos.
26/01/2016    Gustavo     Consulta para arquivos do ISS e SINTEGRA foi implementada.
26/01/2016    Gustavo     Ajusta a função "limpar" para quando já não há mais arquivos no diretório.
28/01/2016    Gustavo     Mensagem para quando já existe um arquivo com os mesmos dados informados.
28/01/2016    Gustavo     Corrigida a função "mover": Em casos do arquivo já existir no servidor, o arquivo era removido
                          do diretório do usuário.
28/01/2016    Gustavo     Aviso inicial para caso não haja arquivos PDFs para mover.
28/01/2016    Gustavo     Alterado label "COMPETÊNCIA" para "PERÍODO CALENDÁRIO". Visto com o Puglieri.
03/02/2016    Gustavo     Substuído o destino de "PDFs-teste" para "PDFs".
04/02/2016    Gustavo     Versão 1.01 - O programa é executado apenas com a opção "Consultar", caso não houver arquivos para mover.
05/02/2016    Gustavo     Versão 1.01 - Adicionada uma notificação com a última atualização quando o programa é aberto.
05/02/2016    Gustavo     Versão 1.01 - Criação automática da pasta "PDFs" no Desktop, caso ela ainda não exista.

'''

import glob
from tkinter import ttk
import tkinter.messagebox
from os.path import expanduser

from consultar import *
from mover import *


app = Tk()
app.configure(background="#d7eef4")
app.title('Arquivo Digital - Puglieri Assessoria')
app.wm_iconbitmap('Logo_Puglieri.ico')     #Para Windows
arte_logo = PhotoImage(file="Logo_Arquivo_Digital.ppm")
Logo = Label(app, image=arte_logo)
Logo.pack()


# === Início da estrutura ARQUIVOS (menu de arquivos a serem movidos + opção visualizar) ===
#diretorio_usuario = expanduser("~") + '\\' + 'Desktop'
extensao = '*.[pP][dD][fF]'
diretorio_usuario = expanduser("~") + '\\' + 'Desktop\\' + 'PDFs\\'
if not os.path.exists(diretorio_usuario):
    os.makedirs(diretorio_usuario)
caminho = diretorio_usuario + extensao
arquivos_diretorio = []


for arquivo in glob.glob(caminho):
    #arquivos_diretorio.append(arquivo)
    arquivos_diretorio.append(os.path.basename(arquivo))
    arquivos_diretorio.sort()


if len(arquivos_diretorio) == 0:
    arquivos_diretorio.append("Nenhum")
    tkinter.messagebox.showinfo("Não há arquivos", "Não há arquivos do tipo PDF em:\n\n%s" % (expanduser("~") + "\Desktop\PDFs"))


arquivo = StringVar()


def visualizar():
    #ver_arquivo = arquivo.get()
    ver_arquivo = diretorio_usuario + arquivo.get()
    #os.system("start " + ver_arquivo)
    os.system('"' + ver_arquivo + '"')


Arquivo_Frame = LabelFrame(app, text="Arquivo", labelanchor=N, bg="#d7eef4", relief=RIDGE)
opcoes = arquivos_diretorio
arquivos_menu = ttk.OptionMenu(Arquivo_Frame, arquivo, opcoes[0], *opcoes)
visualizar_arquivo = ttk.Button(Arquivo_Frame, text="Visualizar", command=visualizar)
arquivos_menu.pack(side=LEFT, padx=5)
visualizar_arquivo.pack(side=LEFT, padx=5, pady=10)
Arquivo_Frame.pack(pady=5)
# === Final da estrutura ARQUIVOS ===

# === Apelido da empresa a ser digitado ===
Label(app, text="Empresa", bg="#d7eef4").pack()
empresa = ttk.Entry(app)
empresa.pack()
# === // ===

# === Início da estrutura OBRIGAÇÃO ===
Label(app, text="Obrigação", bg="#d7eef4").pack()


def lista_obrigacoes(arquivo):
    obrigacoes = []
    obrigacoes_lista = open(arquivo)
    for obrigacao in obrigacoes_lista:
        obrigacoes.append(obrigacao.rstrip())
    return obrigacoes


obrigacao = StringVar()
opcoes_obrigacoes = lista_obrigacoes("obrigacoes.txt")


def selecionar_setor(opcao):
    if opcao == 1:
        return "obrigacoes_contabil.txt"
    if opcao == 2:
        return "obrigacoes_fiscal.txt"
    elif opcao == 3:
        return "obrigacoes_pessoal.txt"
    else:
        return "obrigacoes.txt"


def atualizar_obrigacoes():
    # Não está "setando" corretamente a variável obrigação após alterar os setores

    # Reset var and delete all old options
    # obrigacao.set('')
    # Insert list of new options (tk._setit hooks them up to var)
    # opcoes_atualizadas = ('one', 'two', 'three')
    selecionar_obrigacao['menu'].delete(0,END)
    opcoes_atualizadas = lista_obrigacoes(selecionar_setor(setor.get()))
    opcoes_atualizadas.sort()
    obrigacao.set(opcoes_atualizadas[0])

    for item in opcoes_atualizadas:
        selecionar_obrigacao['menu'].add_command(label=item, command=tkinter._setit(obrigacao, item))


selecionar_obrigacao = ttk.OptionMenu(app, obrigacao, opcoes_obrigacoes[0], *opcoes_obrigacoes)
selecionar_obrigacao.pack(pady=3)

Setor_frame = Frame(app, bg="#d7eef4")

setor = IntVar()
setor_contabil = ttk.Radiobutton(Setor_frame, text='Contábil', variable=setor, value=1, command=atualizar_obrigacoes)
setor_fiscal = ttk.Radiobutton(Setor_frame, text='Fiscal', variable=setor, value=2, command=atualizar_obrigacoes)
setor_pessoal = ttk.Radiobutton(Setor_frame, text='Pessoal', variable=setor, value=3, command=atualizar_obrigacoes)

setor_contabil.pack(side=LEFT, pady=3)
setor_fiscal.pack(side=LEFT, pady=3)
setor_pessoal.pack(side=LEFT, pady=3)
Setor_frame.pack(before=selecionar_obrigacao)
# ==== Final da estrutura OBRIGAÇÃO ====


# ==== Início estrutura COMPETÊNCIA ====
Comp_frame = Frame(app, bg="#d7eef4")
Label(Comp_frame, text="PERÍODO CALENDÁRIO", bg="#d7eef4").pack(pady=6)

Mes_frame = Frame(Comp_frame, bg="#d7eef4")
Label(Mes_frame, text="Mês", bg="#d7eef4").pack()

mes = StringVar()
mes.set(None)

opcoes_meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "ANUAL"]
mes_menu = ttk.OptionMenu(Mes_frame, mes, opcoes_meses[0], *opcoes_meses)
mes_menu.pack(padx=3)
Mes_frame.pack(side=LEFT)

Ano_frame = Frame(Comp_frame, bg="#d7eef4")
Label(Ano_frame, text="Ano", bg="#d7eef4").pack()

ano = StringVar()
ano.set(None)

opcoes_anos = [2016, 2015]
ano_menu = ttk.OptionMenu(Ano_frame, ano, opcoes_anos[0], *opcoes_anos)
ano_menu.pack(padx=3)
Ano_frame.pack(side=RIGHT)
Comp_frame.pack(pady=9, padx=9)
# ===== Final da estrutura COMPETÊNCIA ====


def teste_gui():
    new_window = Tk()
    new_window.title('Teste GUI')
    print("Empresa: %s" % obrigacao.get())
    Label(new_window, text='Isso é um teste').pack()


def limpar():
    movido = arquivo.get()
    arquivos_diretorio.remove(movido)
    arquivos_menu['menu'].delete(movido)
    if len(arquivos_diretorio) > 0:
        arquivo.set(arquivos_diretorio[0])
    else:
        arquivo.set("Nenhum")
    empresa.delete(0,END)


def botao_mover():
    # mover(arquivo_selec, empresa.get(), obrigacao_selec, mes_selec, ano_selec, "pdf")
    if obrigacao.get() in ("ISS","SINTEGRA"):
        janela_complementar = Toplevel()
        janela_complementar.title('Complemento')
        janela_complementar.configure(background="#d7eef4")
        janela_complementar.geometry('300x110+200+100')
        Label(janela_complementar, text=obrigacao.get(), bg="#d7eef4").pack(pady = 5)

        opcoes = StringVar()

        if obrigacao.get() == "ISS":
            opcoes_complementares = ["PRESTADOR","TOMADOR"]
        else:
            opcoes_complementares = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
                                     "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SE", "TO"]

        opcoes_compl_menu = ttk.OptionMenu(janela_complementar, opcoes, opcoes_complementares[0], *opcoes_complementares)
        opcoes_compl_menu.pack(pady = 5)

        def continuar():
            mover(diretorio_usuario + arquivo.get(), empresa.get().upper(), obrigacao.get(), mes.get(), ano.get(), "pdf", opcoes.get())
            janela_complementar.destroy()
            if not os.path.exists(diretorio_usuario + arquivo.get()):
                limpar()

        botao_continuar = ttk.Button(janela_complementar, text = "Continuar", command = continuar)
        botao_continuar.pack(pady = 5)

    else:
        mover(diretorio_usuario + arquivo.get(), empresa.get().upper(), obrigacao.get(), mes.get(), ano.get(), "pdf")

    if not os.path.exists(diretorio_usuario + arquivo.get()):
        limpar()


def botao_consultar():
    consultar(empresa.get().upper(), obrigacao.get(), mes.get(), ano.get(), "pdf")


Botoes_Frame = Frame(app, bg="#d7eef4")
if arquivos_diretorio[0] != "Nenhum":
    ttk.Button(Botoes_Frame, text="Mover", command=botao_mover).pack(side=LEFT, padx=5)
ttk.Button(Botoes_Frame, text="Consultar", command=botao_consultar).pack(side=LEFT, padx=5)
Botoes_Frame.pack(pady=15)

# Notificação informando a última atualização
dir_atualizacoes = expanduser("~") + '\\' + '.arquivodigital'

if not os.path.exists(dir_atualizacoes):
    os.makedirs(dir_atualizacoes)

ultima_atualizacao = 'versao_1.01.txt'

if not os.path.exists(dir_atualizacoes + '\\' + ultima_atualizacao):
    atualizacao = 'Versão 1.01\n\n- O programa é executado apenas com a opção "Consultar", caso não houver arquivos para mover.\n' \
                  '- Criação automática da pasta "PDFs" no Desktop, caso ela não exista.'
    update = open(dir_atualizacoes + '\\' + ultima_atualizacao, 'w')
    update.write(atualizacao)
    update.close()
    tkinter.messagebox.showinfo("Atualização", "%s" % atualizacao)


app.mainloop()
