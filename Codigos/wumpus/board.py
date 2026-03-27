import random
from gold import Ouro
from pit import Abismo
from wumpus import Wumpus

# FORMULAS
ABISMOS = 3 / 16
WUMPUS = 1 / 16

class Tabuleiro:
    def __init__(self, altura: int, comprimento: int):
        if (altura < 4):
            raise ValueError("Altura DEVE ser maior que 4")
        if (comprimento < 4):
            raise ValueError("Comprimento DEVE ser maior que 4")
        
        self.h = int(altura)
        self.c = int(comprimento)
        self.area = altura * comprimento
        self.tab = [[""] * comprimento for _ in range(altura)]
        self.tab_conhecido = [["?"] * comprimento for _ in range(altura)]

        # Eventos
        self.qtd_abismos = round(ABISMOS * self.area)
        self.qtd_wumpus = round(WUMPUS * self.area)
        self.total_eventos = self.qtd_abismos + self.qtd_wumpus + 1 # tesouro também é um "evento"
        self.abismos = []
        self.wumpus = []
        self.tesouro = None

    # Método interno
    def _sorteia_posicoes(self):
        # Define a altura ao redor do player
        y_prox = self.h - 2
        # Definie posições arbitrárias
        posicoes_eventos = []
        total_eventos = self.total_eventos

        for _ in range(total_eventos):
            rand_x = random.randint(0, self.comprimento)
            rand_y = random.randint(0, self.altura)
            # Evita a criação de eventos ao redor do spawn do player
            while (rand_x <= 1 and rand_y >= y_prox):
                rnd_add = random.randint(1, 2)
                if rnd_add == 1:
                    rand_x = random.randint(0, self.comprimento)
                else:
                    rand_y = random.randint(0, self.altura)
            # Evita a criação de eventos em posições já sorteadas
            while([rand_y, rand_x] in posicoes_eventos):
                rnd_add = random.randint(1, 2)
                if rnd_add == 1:
                    rand_x = random.randint(0, self.comprimento)
                else:
                    rand_y = random.randint(0, self.altura)

            posicoes_eventos.append([rand_y, rand_x])

        return posicoes_eventos

    def cria_tabuleiro(self):
        posicoes = self._sorteia_posicoes()

        # Cria os abismos
        for i in range(self.qtd_abismos):
            x = posicoes[i][1]
            y = posicoes[i][0]
            new_abismo = Abismo(x, y)
            self.abismos.append(new_abismo)
            # Atualiza o tabuleiro
            new_abismo.cria_abismo(self.tab)
            # Remove a posição do vetor de posições
            posicoes.pop(i)
        
        # Cria o(s) Wumpus
        for i in range(self.qtd_wumpus):
            x = posicoes[i][1]
            y = posicoes[i][0]
            new_wumpus = Wumpus(x, y)
            self.wumpus.append(new_wumpus)
            # Atualiza o tabuleiro
            new_wumpus.cria_wumpus(self.tab)
            # Remove a posição do vetor de posições
            posicoes.pop(i)

        # Cria o tesouro
        x = posicoes[0][1]
        y = posicoes[0][0]
        self.tesouro = Ouro(x, y)
        # Atualiza o tabuleiro
        self.tab = self.tesouro.cria_tesouro(self.tab)
        # Limpa o vetor
        posicoes.clear()

    def mostra_tabuleiro_conhecido(self):
        for i in range(self.h):
            print(self.tab_conhecido[i])