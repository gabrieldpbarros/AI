from game.board import Tabuleiro
from game.player import Jogador
from game.dfs import DFS

ACOES = [
    "[1] Iniciar agente"
]
TESOURO_E_SAIDA = 1
TESOURO_APENAS = 2

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
        if acao not in [1]:
            print("Insira uma ação válida.")
            return

        self.qtd_acoes += 1
        if acao == 1:
            dfs = DFS(self.tabuleiro, self.jogador)
            rota = dfs.obter_rota()
            if rota:
                self._executa_rota(rota)
                self._retorna_saida(rota)
            else:
                print("\n[DFS] Nenhuma rota segura encontrada para o tesouro.")
                self._finaliza_jogo()

    def _executa_rota(self, rota):
        # OBS: Escrito com ajuda de um LLM
        # Começa a partir de 1 pois o índice 0 é a posição atual do jogador
        for i in range(1, len(rota)):
            alvo_x, alvo_y = rota[i]
            
            # Identifica a direção desejada para o próximo bloco
            if alvo_x > self.jogador.x:
                dir_desejada = 'R'
            elif alvo_x < self.jogador.x:
                dir_desejada = 'L'
            elif alvo_y > self.jogador.y:
                dir_desejada = 'D'
            elif alvo_y < self.jogador.y:
                dir_desejada = 'U'
            else:
                continue

            # Vira o jogador até estar alinhado com a direção desejada
            while self.jogador.direction != dir_desejada:
                idx_atual = self.jogador.dir_index
                idx_desejado = ['R', 'U', 'L', 'D'].index(dir_desejada)
                
                # Lógica para escolher a virada mais rápida (esquerda vs direita)
                if (idx_desejado - idx_atual) % 4 == 1:
                    print(self.jogador.virar('esquerda'))
                else:
                    print(self.jogador.virar('direita'))
                self.qtd_acoes += 1
            
            # Anda para o bloco
            self.jogador.andar(self.tabuleiro)
            self.qtd_acoes += 1
            print(f"O agente andou para [{self.jogador.x + 1},{self.tabuleiro.h - self.jogador.y}].")
            print(self.jogador.mostra_percepcao(self.tabuleiro))
            self.tabuleiro.mostra_tabuleiro_conhecido()
            
        # Pega o ouro ao chegar no fim da rota
        print(self.jogador.pegar_ouro(self.tabuleiro))
        self.qtd_acoes += 1

    def _retorna_saida(self, rota):
        for i in range(len(rota) - 1, -1, -1):
            alvo_x, alvo_y = rota[i]
            
            # Identifica a direção desejada para o próximo bloco
            if alvo_x > self.jogador.x:
                dir_desejada = 'R'
            elif alvo_x < self.jogador.x:
                dir_desejada = 'L'
            elif alvo_y > self.jogador.y:
                dir_desejada = 'D'
            elif alvo_y < self.jogador.y:
                dir_desejada = 'U'
            else:
                continue

            # Vira o jogador até estar alinhado com a direção desejada
            while self.jogador.direction != dir_desejada:
                idx_atual = self.jogador.dir_index
                idx_desejado = ['R', 'U', 'L', 'D'].index(dir_desejada)
                
                # Lógica para escolher a virada mais rápida (esquerda vs direita)
                if (idx_desejado - idx_atual) % 4 == 1:
                    print(self.jogador.virar('esquerda'))
                else:
                    print(self.jogador.virar('direita'))
                self.qtd_acoes += 1
            
            # Anda para o bloco
            self.jogador.andar(self.tabuleiro)
            self.qtd_acoes += 1
            print(f"O agente andou para [{self.jogador.x + 1},{self.tabuleiro.h - self.jogador.y}].")
            print(self.jogador.mostra_percepcao(self.tabuleiro))
            self.tabuleiro.mostra_tabuleiro_conhecido()
        
        if self.jogador.sai_caverna(self.tabuleiro) == TESOURO_E_SAIDA:
            self._finaliza_jogo()

    def comeca_jogo(self):
        self.estado = "iniciado"
        #self.tabuleiro._imprime_tabuleiro()
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
        
        #entrada = input("\nDeseja começar um novo jogo (S/N)?\n")
        #while(entrada not in ['S', 'N', 's', 'n']):
        #    entrada = input("Insira uma resposta válida (S/N): ")
        #if (entrada == 'S' or entrada == 's'):
        #    self.tabuleiro.reinicia_tabuleiro(self.jogador)
        #    # Cria novo jogador
        #    self.jogador = Jogador(self.tabuleiro.h - 1, self.tabuleiro.qtd_wumpus)
        #    self.comeca_jogo()
        #else:
        print("Encerrando sessão.")
        exit(0)