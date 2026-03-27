class Abismo:
    def __init__(self, pos_x: int, pos_y: int):
        self.x = pos_x
        self.y = pos_y

    def _verifica_redores(self, x, y, tabuleiro) -> bool:
        if tabuleiro.tab[y][x] != "P" and tabuleiro.tab[y][x] != "B":
            return True
        else:
            return False

    def cria_abismo(self, tabuleiro):
        # Atualiza o tabuleiro com o novo abismo
        tabuleiro.tab[self.y][self.x] = "P"

        # Encontra os limites do tabuleiro
        x_max = tabuleiro.c
        y_max = tabuleiro.h

        # Brisa na mesma linha
        x_brisa = self.x - 1
        y_brisa = self.y
        if x_brisa >= 0:
            if self._verifica_redores(x_brisa, y_brisa, tabuleiro):
                tabuleiro.tab[y_brisa][x_brisa] += "B"

        x_brisa = self.x + 1
        y_brisa = self.y
        if x_brisa < x_max:
            if self._verifica_redores(x_brisa, y_brisa, tabuleiro):
                tabuleiro.tab[y_brisa][x_brisa] += "B"

        # Brisa na mesma coluna
        x_brisa = self.x
        y_brisa = self.y - 1
        if y_brisa >= 0:
            if self._verifica_redores(x_brisa, y_brisa, tabuleiro):
                tabuleiro.tab[y_brisa][x_brisa] += "B"

        x_brisa = self.x
        y_brisa = self.y + 1
        if y_brisa < y_max:
            if self._verifica_redores(x_brisa, y_brisa, tabuleiro):
                tabuleiro.tab[y_brisa][x_brisa] += "B"