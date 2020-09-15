import pygame
import pygame.font


class Made:
    def __init__(self, ia_settings, screen):
        self.font_message_made = pygame.font.SysFont(None, 20)
        self.string_color = (18, 10, 143)
        self.ia_settings = ia_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

    def made_by(self):
        text = "made by sergio barreto"
        self.text_image = self.font_message_made.render(text, True, self.string_color, self.ia_settings.bg_color)

        # Posição da mensagem
        self.text_rect = self.text_image.get_rect()
        self.text_rect.top = 10
        self.text_rect.right = self.screen_rect.right - 230
        self.screen.blit(self.text_image, self.text_rect)
