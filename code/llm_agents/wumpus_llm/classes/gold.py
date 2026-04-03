class Ouro:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.estado = "solto"

    def cria_tesouro(self, tabuleiro):
        tabuleiro.tab[self.y][self.x] += "T"

    def checa_encontrado(self, tabuleiro, jogador) -> str:
        # Essa lógica busca se há um "G" na string. Separamos a string por split()
        # e removemos o primeiro elemento da lista resultante. Se essa lista for vazia
        # então teremos que [] == [], que é verdadeiro. Caso contrário, significa que
        # houve separação no split(), logo havia um tesouro naquela posição.
        aux_split = tabuleiro.tab[self.y][self.x].split("T")
        aux_split = aux_split.pop(0)
        if (aux_split != [] and self.estado == "solto"): 
            chat_flavor = "Você coletou o ouro e recebeu 50 pontos! Retorne para a entrada da caverna."
            tabuleiro.tab[self.y][self.x] = tabuleiro.tab[self.y][self.x].replace("T", "")
            self.estado = "coletado"
            jogador.curr += 50
        else:
            chat_flavor = "Não há ouro aqui. Você perdeu 1 ponto."
            jogador.curr -= 1
        
        return chat_flavor