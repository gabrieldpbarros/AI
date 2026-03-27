class Ouro:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.estado = "solto"

    def checa_encontrado(self, tabuleiro, jogador) -> str:
        aux_split = tabuleiro.tab[self.y][self.x].split("")
        if (aux_split.count("G") > 0):
            chat_flavor = "Você coletou o ouro e recebeu 50 pontos! Retorne para a entrada da caverna."
            tabuleiro.tab[self.y][self.x] = tabuleiro.tab[self.y][self.x].replace("G", "")
            self.estado = "coletado"
            jogador.curr += 50
        else:
            chat_flavor = "Não há ouro aqui. Você perdeu 1 ponto."
            jogador.curr -= 1
        
        return chat_flavor