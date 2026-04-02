from game.game import Jogo

def start_game(altura: int, comprimento: 4):
    jogo = Jogo(altura, comprimento)
    jogo.comeca_jogo()

if __name__ == "__main__":
    start_game(4, 4)