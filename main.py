# programa NÃO suportará erros do usuário;
import re
import sys
import MT


"""
" Função responsável por receber o comando (r, v, s) e 
" o caminho do arquivo.
" @:param None.
" @:return instrução passada pelo usuário.
"""
def msgFile():
    file = str(input("simturing "))
    return file


"""
" Função responsável por mostrar o cabeçalho do programa.
" @:param None.
" @:return None.
"""
def msgHead():
    print("\t\t\tSimulador de Máquina de Turing ver 1.0 - IFMG 2023.\n"
          "\tDesenvolvido como trabalho prático para a disciplina de Teoria da Computação.\n"
          "\tAutor: Lucas de Oliveira Souza Barbosa.\n")


"""
" Função responsável por dividir a execução do programa de acordo
" com a opção escolhida pelo usuário.
" @:param None.
" @:return None.
"""
def doAll():
    mch = MT.MTuring()
    mod = msgFile().split()
    if mod[0] == '-r':
        mch = execFile(mch, mod[1])
    elif mod[0] == '-v':
        mch = execFile(mch, mod[1])
    elif mod[0] == '-s':
        mch = execFile(mch, mod[2])
    msgHead()
    mch.msgIn()
    instantSetup(mch, mod)


"""
" Função responsável por extrair as informações do arquivo txt.
" @:param máquina de Turing vazia, lista com o caminho do arquivo.
" @:return máquina de Turing preenchida.
"""
def execFile(mch, mod):
    mch.clearListTransitions()
    bloco = ''
    with open(mod, "r") as reader:
        for line in reader:
            x = line.split()
            #DETECTA BLOCOS
            if re.search(r'bloco', line.strip()):
                bloco = x[1]
            #DETECTA COMENTÁRIOS
            elif re.search(r'^;', line.strip()):
                continue
            #DETECTA TRANSIÇÕES
            elif re.search(r'\d*\s.\s--\s.\s.\s\d*', line.strip()):
                mch.setTransition(tuple(x))
            #DETECTA FECHAMENTO DO BLOCO
            elif re.search(r'fim\s;\s\d*', line.strip()):
                mch.setBloc(bloco)
                mch.clearListTransitions()
            #DETECTA MUDANÇA DE BLOCO
            elif re.search(r'\W*\s\D*\s\W*', line.strip()):
                mch.setTransition(tuple(x))
    return mch


"""
" Função responsável por mostrar a sáida de acordo
" com a opção escolhida do usuário.
" @:param máquina de Turing vazia, lista com a opção escolhida.
" @:return None.
"""
def instantSetup(mch, mod):
    # usada para carregar um número maior como entrada, não convencional
    #sys.setrecursionlimit(10**5)
    mch.FTransition()
    if mod[0] == '-r':
        w = "".join(mch.tape)
        print("\nTape: " + w)
    elif mod[0] == '-v':
        mch.showOut(-1)
    elif mod[0] == '-s':
        mch.showOut(mod[1])
    mch.clear()


#chama-se tal função para dar início a execução do programa.
doAll()
