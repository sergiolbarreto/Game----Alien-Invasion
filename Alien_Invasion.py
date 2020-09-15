import pygame
from invasão_alienigena.settings import Settings
from invasão_alienigena.ship import Ship
import invasão_alienigena.game_functions as gf
from pygame.sprite import Group
from invasão_alienigena.game_stats import GameStats
from invasão_alienigena.button import Button
from invasão_alienigena.scoreboard import Scoreboard
from invasão_alienigena.made_by import Made


def run_game():
    pygame.init()
    ia_settings = Settings()
    screen = pygame.display.set_mode((ia_settings.screen_width, ia_settings.screen_height))  # criar a tela
    pygame.display.set_caption("Alien Invasion")  # titulo do programa
    pygame.mixer.music.load('sounds/background.wav')
    pygame.mixer.music.play(-1)
    # Cria uma espaçonave, um grupo de projéteis e um grupo de alienígenas
    ship = Ship(ia_settings, screen)
    # Cria uma instância para armazenar dados estatísticos do jogo e pontuação
    stats = GameStats(ia_settings)
    sb = Scoreboard(ia_settings, screen, stats)
    # Cria o botão Play
    play_button = Button(ia_settings, screen, "Play")
    bullets = Group()
    aliens = Group()
    # Cria a frota de alienígenas
    gf.create_fleet(ia_settings, screen, ship, aliens)
    made = Made(ia_settings, screen)
    while True:  # no while você coloca os laços de eventos para administrar as atualizações de tela
        gf.check_events(ia_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        gf.update_screen(ia_settings, screen, stats, sb, ship, aliens, bullets, play_button, made)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ia_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ia_settings, screen, stats, sb, ship, aliens, bullets)


run_game()  # inicializa o jogo e o laço principal.
