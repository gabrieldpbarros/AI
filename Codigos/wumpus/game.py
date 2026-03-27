from board import Tabuleiro
from player import Jogador

LISTA_ACOES = [
    "Virar para a esquerda",
    "Virar para a direita",
    "Andar",
    "Atirar flecha",
    "Pegar ouro",
    "Sair da caverna"
]

class Jogo:
    def __init__(self, altura: int, comprimento: int):
        self.tabuleiro = Tabuleiro(altura, comprimento)
        self.jogador = Jogador(altura - 1)
        self.qtd_acoes = 0

    def _finaliza_jogo(self):
        pass

    def _acao(self, acao: str):
        if acao not in LISTA_ACOES:
            print("Insira uma ação válida.")

        if acao == "Virar para a esquerda":
            print(self.jogador.virar('esquerda'))
        elif acao == "Virar para a direita":
            print(self.jogador.virar('direita'))
        elif acao == "Andar":
            print(self.jogador.andar(self.tabuleiro))
        elif acao == "Atirar flecha":
            pass
        elif acao == "Pegar ouro":
            print(self.jogador.pegar_ouro(self.tabuleiro))
        else:
            pass

    def comeca_jogo(self):
        self.tabuleiro.tab_conhecido[self.tabuleiro.h - 1][0] = "A"
        print("BEM-VINDO AO MUNDO DO WUMPUS!")
        print("Seu objetivo é encontrar o tesouro escondido nesta caverna.")
        print("\nTome cuidado com os Wumpus e abismos que a caverna abriga!")

        while(self.jogador.state == "vivo"):
            print(self.jogador.mostra_percepcao(self.tabuleiro))
            self.tabuleiro.mostra_tabuleiro_conhecido()
            print("O que deseja fazer?")
            for string in LISTA_ACOES:
                print(f" - {string}")
            acao = input()
            self._acao(acao)

new_game = Jogo(4, 4)
new_game.comeca_jogo()