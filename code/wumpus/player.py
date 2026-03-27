DIRECOES = ['R', 'U', 'L', 'D']
ROSA_DOS_VENTOS = {
    'R': "Leste",
    'U': "Norte",
    'L': "Oeste",
    'D': "Sul"
}

class Jogador:
    def __init__(self, pos_y, qtd_wumpus):
        self.x = 0
        self.y = pos_y
        self.curr = 0
        self.direction = 'R'
        self.dir_index = 0
        self.state = "vivo"
        self.qtd_flechas = qtd_wumpus
        self.percepcao = None

    def _formata_texto(self, string: str) -> str:
        texto = " percebe"
        temp = string.split(" ")
        #print(f"TEMP: {temp}")
        aux = string.replace("a", "") # removemos o "a" de "uma" para ser contabilizado
        aux = aux.split(" ")
        # Encontra a quantidade de percepções
        contador = aux.count("um")
        if (contador == 1):
            return texto + string + "."
        elif (contador == 2):
            primeira_parte = " " + temp[1] + " " + temp[2]
            segunda_parte = " e " + temp[3] + " " + temp[4]
            return texto + primeira_parte + segunda_parte + "."
        else:
            primeira_parte = " " + temp[1] + " " + temp[2]
            segunda_parte = ", " + temp[3] + " " + temp[4]
            terceira_parte = " e " + temp[5] + " " + temp[6]
            return texto + primeira_parte + segunda_parte + terceira_parte + "."

    def _checa_estado(self, tabuleiro) -> str:
        x = self.x
        y = self.y
        tab_state: str = tabuleiro.tab[y][x]
        # ------------------------------------------------------------------------------------
        # SITUAÇÕES FATAIS
        # Wumpus
        if (tab_state.find("W") != -1):
            self.state = "morto"
            self.curr -= 100
            return "O Wumpus te encontra e devora seu pequeno e frágil corpitcho. Você morreu."
        # Abismo
        elif (tab_state.find("P") != -1):
            self.state = "morto"
            self.curr -= 100
            return "Você tropeça e cai em um profundo abismo. Você morreu."
        # ------------------------------------------------------------------------------------
        # SITUAÇÕES COMUNS
        extra_string = ""
        # Fedor
        if (tab_state.find("F") != -1):
            extra_string += " um fedor"
        # Brisa
        if (tab_state.find("B") != -1):
            extra_string += " uma brisa"
        # Ouro
        if (tab_state.find("T") != -1):
            extra_string += " um brilho"
        # ------------------------------------------------------------------------------------
        if extra_string == "":
            return " não percebe nada."
        else:
            extra_string = self._formata_texto(extra_string)
            return extra_string

    def mostra_percepcao(self, tabuleiro) -> str:
        # Checa se o compartimento não contém perigos
        self.percepcao = self._checa_estado(tabuleiro)
        #print(f"PERCEPCAO: {self.percepcao}")
        if (self.state == "morto"):
                return self.percepcao
        else:
            pos_x_convertida = self.x + 1
            pos_y_convertida = tabuleiro.h - self.y
            string_posicao = f"Você está na posição [{pos_x_convertida},{pos_y_convertida}] e"
            return string_posicao + self.percepcao
        
    def andar(self, tabuleiro):
        x = self.x
        y = self.y

        if self.direction == 'R':
            x += 1
        elif self.direction == 'U':
            y -= 1
        elif self.direction == 'L':
            x -= 1
        else: # para baixo
            y += 1
        # Anda na direção da parede
        if (y == tabuleiro.h or y == -1 or x == tabuleiro.c or x == -1):
            print("Você bate na parede e sente um choque.")
        else:
            # Atualiza os tabuleiros
            old_x = 0 + self.x
            old_y = 0 + self.y
            self.x = x
            self.y = y
            self.curr -= 1
            tabuleiro.atualiza_tabuleiros(old_x, old_y, self.x, self.y)
            
    def virar(self, direcao: str) -> str:
        index = self.dir_index
        if (direcao == 'esquerda'):
            if (index == 3):
                index = 0
            else:
                index += 1
        elif (direcao == 'direita'):
            if (index == 0):
                index = 3
            else:
                index -= 1
        else:
            return "Escreva uma direção válida. (esquerda ou direita)"
            
        self.dir_index = index
        self.direction = DIRECOES[index]

        return f"Você vira para a {direcao} e encara o {ROSA_DOS_VENTOS[self.direction]}"

    def pegar_ouro(self, tabuleiro) -> str:
        return tabuleiro.tesouro.checa_encontrado(tabuleiro, self)