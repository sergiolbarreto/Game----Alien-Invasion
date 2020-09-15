class GameStats:
    """ Armazena dados estatísticos da Invasão Alienígena."""
    def __init__(self, ia_settings):
        self.ia_settings = ia_settings
        self.reset_stats()

        # Inicia a Invasão Alienígena em um estado inativo
        self.game_active = False

        # a pontuaçõa máxima jamais deverá ser reiniciada
        with open('invasão_alienigena/high_score.txt') as documento:  # tem que ser sem formatação
            linhas = documento.read()
        self.high_score = int(linhas)

    def reset_stats(self):
        "Inicializa os dados estatísticos que podem mudar durante o jogo."
        self.ship_left = 3
        self.score = 0
        self.level = 1

