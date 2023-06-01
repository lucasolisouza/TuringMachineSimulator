from colorama import Fore, Back, Style

"""
" Classe que representa a Máquina de Turing e suas
" funções para controlá-la.
"""


class MTuring:
    """
    " Função responsável por iniciar a máquina de Turing.
    " @:param None.
    " @:return None.
    """

    def __init__(self):
        self.tape = list()
        self.tapehead = int()
        self.aux = int()
        self.check = None
        self.prevsState = list()
        self.prevsBloc = list()
        self.estadoAtual = '01'
        self.blocoAtual = 'main'
        self.keywords = ('retorne', 'pare')
        self.transicoes = list()
        self.blocos = dict()
        self.Output = list()

    """
    " Função responsável por realizar a criação dos blocos das transições.
    " @:param Nome do bloco.
    " @:return Boolean(sucesso/falha).
    """

    def criaBloco(self, bloco):
        bloco = str(bloco)
        if bloco in self.blocos:
            return False
        self.blocos[bloco] = list(self.transicoes)
        return True

    """
    " Função responsável por criar a transição.
    " @:param Transição.
    " @:return None.
    """

    def criaTransicao(self, x):
        x = tuple(x)
        #  [ e  ,  a ] = ( b  , d ,  e' ) --> ( e , a , b , d , e' )
        self.transicoes.append(x)

    """
    " Função responsável por limpar a lista de transições.
    " @:param None.
    " @:return None.
    """

    def limpaTransicoes(self):
        self.transicoes.clear()

    """
    " Função responsável por limpar a máquina de Turing.
    " @:param None.
    " @:return None.
    """

    def clear(self):
        self.Output.clear()
        self.blocos.clear()
        self.tape.clear()
        self.prevsBloc.clear()

    """
    " Função responsável por limpar a lista de estados anteriores até a marca
    " de mudança de bloco (#).
    " @:param None.
    " @:return None.
    """

    def remove_items(self):
        while len(self.prevsState) > 0 and self.prevsState[len(self.prevsState) - 1] != '#':
            self.prevsState.pop()
        if len(self.prevsState) > 0 and self.prevsState[len(self.prevsState) - 1] == '#':
            self.prevsState.pop()

    """
    " Função responsável por realizar a defição de cada transição, podendo ser:
    " mudança de bloco, palavra reservada, ou transição entre estados.
    " @:param Trasição.
    " @:return None.
    """

    def Bloc(self, trans):
        self.insertBlocList(self.tape, self.tapehead)
        if self.check is not None and self.check not in self.prevsBloc:
            self.estadoAtual = None
            self.prevsBloc.clear()
            self.prevsState.clear()
            return
        if len(trans) == 3:  # encontrou uma mudança de bloco.
            if trans[2] == self.keywords[1]:  # encontrou o pare.
                self.check = trans[1]
                self.prevsState.append(trans[0])
                self.aux = self.prevsState[-1]
                self.estadoAtual = '01'
                self.prevsBloc.append(trans[1])
                self.blocoAtual = self.prevsBloc[-1]
                self.prevsState.append('#')
                self.FTransition()
            else:
                self.estadoAtual = '01'
                self.prevsState.append(trans[2])
                self.aux = self.prevsState[-1]
                self.blocoAtual = trans[1]
                self.prevsState.append('#')
                self.FTransition()
        else:
            if trans[5] == self.keywords[0]:  # encontrou o retorne.
                self.estadoAtual = self.prevsState[-1]
                self.FTransition()
            else:
                self.FTransition()

    """
    " Função responsável por realizar as ações de cada transição.
    " @:param None.
    " @:return None.
    """

    def FTransition(self):
        # INSERE BLOCO NA LISTA DE ANTERIORES
        if len(self.prevsBloc) == 0 or self.blocoAtual != self.prevsBloc[-1]:
            self.prevsBloc.append(self.blocoAtual)

        # INSERE ESTADO NA LISTA DE ANTERIORES
        if len(self.prevsState) > 0 and self.estadoAtual != self.prevsState[-1]:
            self.prevsState.append(self.estadoAtual)

        self.insertBlocList(self.tape, self.tapehead)

        # PERCORRE O BLOCO ATUAL PARA ACHAR A TRANSIÇÃO
        for x in self.blocos[self.blocoAtual]:
            if self.check is not None and self.check not in self.prevsBloc:
                self.estadoAtual = None
                self.prevsBloc.clear()
                self.prevsState.clear()
                break

            if len(x) == 3 and x[0] == self.estadoAtual:
                self.Bloc(x)
            if x[0] == self.estadoAtual:
                if self.tapehead < 0 or self.tapehead >= len(self.tape):
                    self.swInTape(x)  # altera na fita
                    self.moveTapeH(x)  # move cabeçote
                    if x[5] == self.keywords[0]:  # RETORNA
                        self.estadoAtual = self.aux
                        self.remove_items()
                        self.prevsBloc.pop()
                        self.blocoAtual = self.prevsBloc[-1]
                    else:
                        self.prevsState.append(x[0])
                        self.estadoAtual = x[5]
                    self.Bloc(x)
                elif x[1] == self.tape[self.tapehead] or x[1] == '*':
                    self.swInTape(x)  # altera na fita
                    self.moveTapeH(x)  # move cabeçote
                    if x[5] == self.keywords[0]:  # RETORNA
                        self.estadoAtual = self.aux
                        if len(self.prevsBloc) > 1:
                            self.prevsBloc.remove(self.blocoAtual)
                        self.remove_items()
                        self.blocoAtual = self.prevsBloc[-1]
                        self.Bloc(x)
                    else:
                        self.prevsState.append(x[0])
                        self.estadoAtual = x[5]
                    break
        if self.proxTrans() is not None:
            self.Bloc(self.proxTrans())

    """
    " Função responsável por detectar a próxima transição.
    " @:param None.
    " @:return None.
    """
    def proxTrans(self):
        for x in self.blocos[self.blocoAtual]:
            if len(x) == 3 and x[0] == self.estadoAtual:
                return x
            elif x[0] == self.estadoAtual and ((self.tapehead < 0 or self.tapehead >= len(self.tape)) or (
                    x[1] == self.tape[self.tapehead] or x[1] == '*')):
                return x



    """
    " Função responsável por alterar a fita da máquina.
    " @:param Transição.
    " @:return None.
    """

    def swInTape(self, trans):  # altera na fita
        symbol = trans[3]
        if symbol == '*':
            if self.tapehead < 0:
                self.tape.insert(0, '_')
                self.tapehead = 0
            elif self.tapehead >= len(self.tape):
                self.tape.append('_')
        else:
            if self.tapehead < 0:
                self.tape.insert(0, symbol)
                self.tapehead = 0
            elif self.tapehead >= len(self.tape):
                self.tape.append(symbol)
            else:
                self.tape[self.tapehead] = symbol

    """
    " Função responsável por inserir transições que ocorrem durante a 
    " execução da máquina como forma de histórico, ou seja, a configuração
    " instantânea da máquina.
    " @:param Fita, cabeçote.
    " @:return None.
    """

    def insertBlocList(self, tape, tapehead):
        w = "".join(tape)
        y = (self.blocoAtual, self.estadoAtual, w, tapehead)
        if not self.Output or y != self.Output[-1]:
            self.Output.append(y)

    """
    " Função responsável por realizar o movimento do cabeçote.
    " @:param Transição.
    " @:return None.
    """

    def moveTapeH(self, trans):
        if trans[4] == 'd':
            self.tapehead += 1
        elif trans[4] == 'e':
            self.tapehead -= 1

    """
    " Função responsável por mostrar a configuração instantânea da
    " máquina após a execução como forma de saída.
    " @:param Número de transições que serão mostradas..
    " @:return None.
    """

    def showOut(self, n):
        n = int(n)
        count = int()
        saida = list()
        output = '''
                Configuração Instatânea gerada pela Máquina de Turing.
        Terminologia:  - Cabeçote é representado pela cor roxa.
                       - Quando o cabeçote está em uma posição além da palavra, uma sequência de
                         colchetes ([ ]) aparece para representar o mesmo.
------------------------------------------------------------------------------------------------------
Nº      Bloco                 Estado Atual            Fita
       
{saida}
        
        '''

        def format_out(i, bloco, estadoAtual, w, tapehead):
            f = lambda x: Fore.BLUE + x[tapehead] + Fore.RESET + x[tapehead + 1:]
            fi = lambda x: x + Fore.BLUE + '[ ]' + Fore.RESET
            fii = lambda x: Fore.BLUE + '[ ]' + Fore.RESET + x
            fiii = lambda x: x[:tapehead] + Fore.BLUE + x[tapehead] + Fore.RESET + x[tapehead + 1:]
            if tapehead > len(w) - 1:
                return f'{i: <8}{bloco: <26}{estadoAtual: <20}{fi(w)}'
            elif tapehead < 0:
                return f'{i: <8}{bloco: <26}{estadoAtual: <20}{fii(w)}'
            elif tapehead == 0:
                return f'{i: <8}{bloco: <26}{estadoAtual: <20}{f(w)}'
            else:
                return f'{i: <8}{bloco: <26}{estadoAtual: <20}{fiii(w)}'

        for y in self.Output:
            if n == -1 or count < n:
                saida.append(y)
                count += 1
            else:
                break
        saida = [
            format_out(i, bloco, estadoAtual, w, tapehead)
            for i, (bloco, estadoAtual, w, tapehead) in enumerate(saida, 1)
        ]
        print(output.format(saida='\n'.join(saida)))
        self.Output.clear()


    """
    " Função responsável por receber a palavra que será inserida na fita.
    " @:param None.
    " @:return None.
    """

    def msgIn(self):
        self.tape = list(input("Forneça a palavra inicial: "))
