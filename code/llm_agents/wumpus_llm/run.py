from classes.game import Jogo

def start_game(altura: int, comprimento: int):
    jogo = Jogo(altura, comprimento)
    jogo.comeca_jogo()

if __name__ == "__main__":
    start_game(4, 4)