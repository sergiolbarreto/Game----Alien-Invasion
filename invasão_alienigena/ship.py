import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ia_settings, screen):
        super().__init__()
        self.screen = screen
        self.ia_settings = ia_settings
        # Carrega a imagem da espaçonave e obtém seu rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()  # rect = retangulo
        self.screen_rect = screen.get_rect()  # voce meio que transforma a tela toda em um rect/retangulo para poder
        # trabalhar com as medidas, poder modelar etc
        # Inicia cada nova espaçonave na parte inferior central da tela - coordenadas da espaçonave
        self.rect.centerx = self.screen_rect.centerx  # a coordenada x do centro da espaçonave
        self.rect.bottom = self.screen_rect.bottom  # a coordenada y da parte inferior da espaçonave
        # Armazena um valor decimal para o centro da espaçonave
        self.center = float(self.rect.centerx)
        # Flag de movimento
        self.moving_right = False
        self.moving_left = False

    def update(self):  # Atualiza a posição da espaçonave de acordo com a flag de movimento
        # Atualiza o valor do centro da espaçonave, e não o retângulo
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ia_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ia_settings.ship_speed_factor
        # Atualiza o objeto rect de acordo com o self.center
        self.rect.centerx = self.center

    def blitme(self):  # desenhará a imagem na tela na posição especificada por self.rect
        """# desenha a espaçonave em sua posição atual."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centraliza a espaçonave na tela."""
        self.center = self.screen_rect.centerx
