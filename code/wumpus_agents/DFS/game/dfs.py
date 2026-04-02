class DFS:
    # OBS: A classe inteira foi escrita com auxílio de um LLM
    def __init__(self, tabuleiro, jogador):
        self.tabuleiro = tabuleiro
        self.jogador = jogador
        self.visitados = set()
        self.caminho = []

    def buscar(self, x, y):
        # Verifica limites do tabuleiro
        if x < 0 or x >= self.tabuleiro.c or y < 0 or y >= self.tabuleiro.h:
            return False
        
        # Verifica se já visitou ou se é um perigo conhecido (Abismo ou Wumpus vivo)
        pos_atual = (x, y)
        if pos_atual in self.visitados:
            return False
        
        conteudo = self.tabuleiro.tab[y][x]
        if "P" in conteudo or "W" in conteudo:
            return False

        self.visitados.add(pos_atual)
        self.caminho.append(pos_atual)

        # Objetivo: Encontrar o Tesouro
        if "T" in conteudo:
            return True

        # Movimentos: Direita, Baixo, Esquerda, Cima
        movimentos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        
        for dx, dy in movimentos:
            if self.buscar(x + dx, y + dy):
                return True
        
        self.caminho.pop()
        return False

    def obter_rota(self):
        if self.buscar(self.jogador.x, self.jogador.y):
            return self.caminho
        return None
