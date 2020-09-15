import pygame.font
from pygame.sprite import Group
from invasão_alienigena.ship import Ship


class Scoreboard:
    """Uma classe paa mostrar informações sobre pontuação"""

    def __init__(self, ia_settings, screen, stats):
        """ Inicializa os atributos da pontuação"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ia_settings = ia_settings
        self.stats = stats

        # Configurações de fonte para as informações de pontuação
        self.text_color = (181, 20, 20)
        self.font = pygame.font.SysFont(None, 40)
        self.string_color = (60, 60, 60)
        self.font_message_made = pygame.font.SysFont(None, 20)

        # Prepara a imagem da pontuação inicial
        self.prep_score()

        # Prepara as images das pontuações iniciais
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        "Mostra quantas espaçonaves restam."
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ia_settings, self.screen)
            ship.rect.x = 160 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        """Transforma o nível em uma imagem renderizada."""
        text_level = "Level"
        self.text_image_level = self.font.render(text_level, True, self.string_color, self.ia_settings.bg_color)
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ia_settings.bg_color)

        # Posição do numero nivel
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 35
        self.level_rect.top = 37

        # Exibe a palavra Level na tela
        self.text_level_rect = self.text_image_level.get_rect()
        self.text_level_rect.left = self.screen_rect.left + 10
        self.text_level_rect.top = 10

    def prep_high_score(self):
        """Transforma a pontuação máxima em uma imagem renderizada"""
        text_best_score = "Best Score Ever"
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = f'{high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ia_settings.bg_color)
        self.text_best_score = self.font.render(text_best_score, True, self.string_color, self.ia_settings.bg_color)

        # Centraliza a pontuação máxima na parte superior da tela
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 35

        # Posição da palvra best score ever
        self.text_best_score_rect = self.text_best_score.get_rect()
        self.text_best_score_rect.centerx = self.screen_rect.centerx
        self.text_best_score_rect.top = 5

    def prep_score(self):
        """Transforma a pontuaçao em uma imagem rendenrizada."""
        text = "Score"
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,} '
        self.score_image = self.font.render(score_str, True, self.text_color, self.ia_settings.bg_color)
        self.text_image = self.font.render(text, True, self.string_color, self.ia_settings.bg_color)

        # Posição do numero score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 37
        self.score_rect.right = self.screen_rect.right - 20

        # Exibe a palavra score na tela
        self.text_rect = self.text_image.get_rect()
        self.text_rect.top = 10
        self.text_rect.right = self.screen_rect.right - 25

    def show_score(self):
        """Desenha a pontuação na tela."""
        # Desenha a parte numérica
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Desenha a parte textual
        self.screen.blit(self.text_image, self.text_rect)
        self.screen.blit(self.text_image_level, self.text_level_rect)
        self.screen.blit(self.text_best_score, self.text_best_score_rect)

        # Desenha as espaçonaves
        self.ships.draw(self.screen)
