class Wumpus:
    def __init__(self, pos_x: int, pos_y: int):
        self.x = pos_x
        self.y = pos_y
        self.estado = "vivo"

    def _verifica_redores(self, x, y, tabuleiro) -> bool:
        if tabuleiro.tab[y][x] != "P" and tabuleiro.tab[y][x] != "F":
            return True
        else:
            return False

    def cria_wumpus(self, tabuleiro):
        # Atualiza o tabuleiro com o novo wumpus
        tabuleiro.tab[self.y][self.x] = "W"

        # Encontra os limites do tabuleiro
        x_max = tabuleiro.c
        y_max = tabuleiro.h

        # Fedor na mesma linha
        x_fedor = self.x - 1
        y_fedor = self.y
        if x_fedor >= 0:
            if self._verifica_redores(x_fedor, y_fedor, tabuleiro):
                tabuleiro.tab[y_fedor][x_fedor] += "F"

        x_fedor = self.x + 1
        y_fedor = self.y
        if x_fedor < x_max:
            if self._verifica_redores(x_fedor, y_fedor, tabuleiro):
                tabuleiro.tab[y_fedor][x_fedor] += "F"

        # Fedor na mesma coluna
        x_fedor = self.x
        y_fedor = self.y - 1
        if y_fedor >= 0:
            if self._verifica_redores(x_fedor, y_fedor, tabuleiro):
                tabuleiro.tab[y_fedor][x_fedor] += "F"

        x_fedor = self.x
        y_fedor = self.y + 1
        if y_fedor < y_max:
            if self._verifica_redores(x_fedor, y_fedor, tabuleiro):
                tabuleiro.tab[y_fedor][x_fedor] += "F"
    
    def acerta_wumpus(self, tabuleiro, jogador) -> str:
        chat_flavor = "O Wumpus grita de dor e morre. Você recebeu 50 pontos!"
        tabuleiro.tab[self.y][self.x] = tabuleiro.tab[self.y][self.x].replace("W", "X")
        self.estado = "morto"
        jogador.curr += 50

        return chat_flavor