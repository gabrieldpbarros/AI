from board import Tabuleiro
from player import Jogador

ACOES = [
    "[1] Virar para a esquerda",
    "[2] Virar para a direita",
    "[3] Andar",
    "[4] Atirar flecha",
    "[5] Pegar ouro",
    "[6] Sair da caverna"
]

class Jogo:
    def __init__(self, altura: int, comprimento: int):
        self.tabuleiro = Tabuleiro(altura, comprimento)
        self.jogador = Jogador(altura - 1, self.tabuleiro.qtd_wumpus)
        self.estado = "encerrado"
        self.qtd_acoes = 0

        self.tabuleiro.cria_tabuleiro()

    def _finaliza_jogo(self):
        self.estado = "encerrado"
        print("FIM DE JOGO.")
        print(f"Pontuação final: {self.jogador.curr}")

    def _acao(self, acao: int):
        if acao not in [0, 1, 2, 3, 4, 5, 6]:
            print("Insira uma ação válida.")

        self.qtd_acoes += 1
        if acao == 1:
            print(self.jogador.virar('esquerda'))
        elif acao == 2:
            print(self.jogador.virar('direita'))
        elif acao == 3:
            print(self.jogador.andar(self.tabuleiro))
        elif acao == 4:
            pass
        elif acao == 5:
            print(self.jogador.pegar_ouro(self.tabuleiro))
        else:
            pass

    def comeca_jogo(self):
        self.estado = "iniciado"
        self.tabuleiro._imprime_tabuleiro()
        print("BEM-VINDO AO MUNDO DO WUMPUS!")
        print("Seu objetivo é encontrar o tesouro escondido nesta caverna.")
        print("Tome cuidado com os Wumpus e abismos que a caverna abriga!")

        while(self.estado == "iniciado"):
            self.tabuleiro.mostra_tabuleiro_conhecido()
            print(self.jogador.mostra_percepcao(self.tabuleiro))
            if (self.jogador.state == "morto"):
                self._finaliza_jogo()
                break
            
            if (self.jogador.qtd_flechas > 0):
                print(f"Você tem {self.jogador.qtd_flechas} flecha(s)")
            print("O que deseja fazer?")
            for string in ACOES:
                print(f" - {string}")
            acao = int(input())
            self._acao(acao)
        
        entrada = input("\nDeseja começar um novo jogo (S/N)?\n")
        while(entrada not in ['S', 'N']):
            entrada = input("Insira uma resposta válida (S/N): ")
        if (entrada == 'S'):
            self.tabuleiro.reinicia_tabuleiro(self.jogador)
            # Cria novo jogador
            self.jogador = Jogador(self.tabuleiro.h - 1, self.tabuleiro.qtd_wumpus)
            self.comeca_jogo()
        else:
            print("Encerrando sessão.")
            exit(0)


new_game = Jogo(10, 10)
new_game.comeca_jogo()