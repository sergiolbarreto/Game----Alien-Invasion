import sys
import pygame
from invasão_alienigena.bullets import Bullet
from invasão_alienigena.alien import Alien
from time import sleep


def check_keydown_events(event, ia_settings, screen, ship, bullets, stats):  # checa eventos em que o jogador
    # pressiona a tecla
    if event.key == pygame.K_RIGHT:
        # Move a espaçonave para a direita
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move a espaçonave para a esquerda
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullets(ia_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        filename = 'high_score.txt'
        with open(filename, 'w') as documento:
            documento.write(str(stats.high_score))
        sys.exit()
    elif event.key == pygame.K_p:
        stats.game_active = True
        pygame.mouse.set_visible(False)


def fire_bullets(ia_settings, screen, ship, bullets):
    # Controla a quantidade de projéteis
    if len(bullets) < ia_settings.bullets_allowed:
        bullet_sound = pygame.mixer.Sound('sounds/laser.wav')
        bullet_sound.play()
        new_bullet = Bullet(ia_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):  # checa eventos em que o jogador solta uma tecla
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ia_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Responde a eventos de pressionamento de teclas e de mouse
    for event in pygame.event.get():  # responder os eventos, o pygame.event.get é para acessar esses eventos
        if event.type == pygame.QUIT:  # responder a eventos especificos, nesse caso, sair do jogo
            filename = 'high_score.txt'
            with open(filename, 'w') as documento:
                documento.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ia_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:  # jogador solta a tecla direita KEYUP quer dizer retirar o dedo de certa tecla
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ia_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ia_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo qunado o jogador clicar em Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reinincia as configurações do jogo
        ia_settings.initialize_dynamic_settings()
        # Oculta o cursor do mouse
        pygame.mouse.set_visible(False)
        # Reinicia os dados estatísticos do jogo
        stats.reset_stats()
        stats.game_active = True
        # Reinincia os dados estatísticos do jogo
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Esvazia a lista de alienígenas e de projéteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a espaçonave
        create_fleet(ia_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ia_settings, screen, stats, sb, ship, aliens, bullets, play_button, made):
    """Atualiza as images na tela e alterna para a nova tela"""
    # Redesenha a tela a cada passagem pelo laço
    screen.fill(ia_settings.bg_color)  # define a cor
    # Desenha a informação sobre pontuação
    sb.show_score()
    made.made_by()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()  # desenha a nave
    aliens.draw(screen)
    # Desenha o botão Play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()  # deixar visivel a tela mais recente


def update_bullets(ia_settings, screen, stats, sb, ship, aliens, bullets):  # Atualiza a posição dos projéteis e se livra dos
    # projéteis antigos
    # Atualiza as posições dos projéteis
    bullets.update()
    # Livra-se dos projéteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ia_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ia_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            explosion_sound = pygame.mixer.Sound('sounds/explosion_5.wav')
            explosion_sound.play()
            stats.score += ia_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:  # Destrói os projéteis existentes e cria uma nova frota, se a frota for destruida,
        # inicia um novo nível
        bullets.empty()
        ia_settings.increase_speed()  # aumenta a velocidade do jogo

        # Aumenta o nível
        stats.level += 1
        sb.prep_level()
        create_fleet(ia_settings, screen, ship, aliens)


def get_number_x(ia_settings, alien_width):
    """Determina o núero de alienígenas que cabem em uma linha"""
    available_space_x = ia_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x


def get_number_rows(ia_settings, ship_height, alien_height):  # Vê o espaço para colocar as linhas de aliens
    """Determina o número de linhas com alienígenas que cabem na tela"""
    avaliable_space_y = (ia_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows


def create_alien(ia_settings, screen, aliens, alien_number, row_number):
    # Cria um alienígena e o posiciona na linha
    alien = Alien(ia_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ia_settings, screen, ship, aliens):
    """Cria uma frota completa de alienígenas"""
    # Cria um alienígena e calcula o número de alienígenas em uma linha
    alien = Alien(ia_settings, screen)
    number_aliens_x = get_number_x(ia_settings, alien.rect.width)
    number_rows = get_number_rows(ia_settings, ship.rect.height, alien.rect.height)

    # Cria a primeira linha de alienígenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ia_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ia_settings, aliens):
    """Reesponde apropriadamente se algum alienígena alcançou uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ia_settings, aliens)
            break


def change_fleet_direction(ia_settings, aliens):
    """Faz toda a frota descer e muda a sua direção"""
    for alien in aliens.sprites():
        alien.rect.y += ia_settings.fleet_drop_speed
    ia_settings.fleet_direction *= -1


def check_aliens_bottom(ia_settings, screen, stats, sb, ship, aliens, bullets):
    """Verifica se algum alienígena alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esse caso do mesmo modo que é feito quando a espaçonave é atingida
            ship_hit(ia_settings, screen, stats, sb, ship, aliens, bullets)


def update_aliens(ia_settings,  screen, stats, sb, ship, aliens, bullets):
    """Verifica se a frota está em uma das bordas
    e então atualiza as posições de todos os alienígenas da frota"""
    check_fleet_edges(ia_settings, aliens)
    aliens.update()

    # Verifica se houve colisões entre alienígenas e a espaçonave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ia_settings, screen, stats, sb, ship, aliens, bullets)
    # Verifica se há algum alienígena que atingiu a parte inferior da tela
    check_aliens_bottom(ia_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ia_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde ao fato de a espaçonave ter sido atingida por um alienígena"""
    # Decrementa ships_left
    if stats.ship_left > 0:
        stats.ship_left -= 1
        # Atualiza o painel de pontuações
        sb.prep_ships()
    if stats.ship_left == 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.reset_stats()
        sb.prep_ships()
        sb.prep_level()
        sb.prep_score()
        ia_settings.initialize_dynamic_settings()

    # Esvazia a lista de alienígenas e de projéteis
    aliens.empty()
    bullets.empty()

    # Cria uma nova frota e centraliza a espaçonave
    create_fleet(ia_settings, screen, ship, aliens)
    ship.center_ship()

    # Faz uma pausa
    sleep(0.5)


def check_high_score(stats, sb):
    """Verifica se há uma nova pontuação máxima"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
