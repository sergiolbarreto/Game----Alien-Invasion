import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):  # Uma classe que admnistra projéteis disparados pela espaçonave
    def __init__(self, ia_settings, screen, ship):
        # Cria um objeto para o projétil na posição atual da espaçonave
        super().__init__()
        self.screen = screen
        # Cria um rentângulo para um projétil em (0,0) e, em seguida, define a posião correta
        self.rect = pygame.Rect(0, 0, ia_settings.bullet_width, ia_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx  # o centerx do projétil é igual ao centerx da espaçonave
        self.rect.top = ship.rect.top
        # Armazena a posição do projétil como um valor decimal
        self.y = float(self.rect.y)
        self.color = ia_settings.bullet_color
        self.speed_factor = ia_settings.bullet_speed_factor

    def update(self):  # Move o projétil para cima da tela
        # Atualiza a posição decimal do projétil
        self.y -= self.speed_factor
        # Atualiza a posição de rect
        self.rect.y = self.y

    def draw_bullet(self):  # Desenha o projétil na tela.
        pygame.draw.rect(self.screen, self.color, self.rect)
