import sys

import pygame
import game
import help
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 560

disc_count = 4

play_button_rect = None
solve_button_rect = None
help_button_rect = None
plus_button_rect = None
minus_button_rect = None
quit_button_rect = None
quitting = False

def menu():
    global disc_count
    global play_button_rect
    global solve_button_rect
    global help_button_rect
    global quit_button_rect
    global plus_button_rect
    global minus_button_rect
    pygame.init()
    title_font = pygame.font.Font('font/pixelType.ttf', 100)
    button_font = pygame.font.Font('font/pixelType.ttf', 56)
    num_label_font = pygame.font.Font('font/pixelType.ttf', 32)
    num_font = pygame.font.Font('font/pixelType.ttf', 80)

    title_text = title_font.render('Tower_of_Hanoi', False, 'darkBlue')
    play_text = button_font.render('PLAY', False, 'skyBlue')
    solve_text = button_font.render('SOLVE', False, 'skyBlue')
    help_text = button_font.render('HOW TO PLAY', False, 'skyBlue')
    quit_text = button_font.render('QUIT', False, 'skyBlue')
    num_label_text = num_label_font.render('num of discs', False, 'black')
    num_text = num_font.render('5', False, 'black')
    plus_text = num_font.render('+', False, 'white')
    minus_text = num_font.render('-', False, 'white')

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 120))

    help_rect = help_text.get_rect(center=(SCREEN_WIDTH / 2, 380))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH / 2, 460))
    solve_rect = solve_text.get_rect(center=(SCREEN_WIDTH / 2, 540))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, 620))

    num_label_rect = num_label_text.get_rect(center=(SCREEN_WIDTH / 2, 180))
    num_rect = num_text.get_rect(center=(SCREEN_WIDTH / 2, 240))

    plus_rect = plus_text.get_rect(center=(SCREEN_WIDTH / 2 + 56, 240))
    minus_rect = minus_text.get_rect(center=(SCREEN_WIDTH / 2 - 56, 240))

    play_button_rect = play_rect.scale_by(1.25, 1.25)
    play_button_rect = pygame.Rect(
                            (SCREEN_WIDTH - play_button_rect.width) / 2,
                            play_rect.top + (play_rect.height - play_button_rect.height) / 2,
                            play_button_rect.width,
                            play_button_rect.height
                            )
    solve_button_rect = solve_rect.scale_by(1.25, 1.25)
    help_button_rect = help_rect.scale_by(1.25, 1.25)
    quit_button_rect = quit_rect.scale_by(1.25, 1.25)

    num_box_rect = num_rect.scale_by(1.25, 1.25)
    plus_button_rect = plus_rect.scale_by(1.25, 1.25)
    minus_button_rect = minus_rect.scale_by(1.25, 1.25)

    background_fill_color = '#ffcccc'
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tower of Hanoi')
    clock = pygame.time.Clock()

    disc_count = 4

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = handle_click(pygame.mouse.get_pos())
        num_text = num_font.render(str(disc_count), False, 'black')
        screen.fill(background_fill_color)

        pygame.draw.rect(screen, 'darkBlue', play_button_rect)
        pygame.draw.rect(screen, 'darkBlue', solve_button_rect)
        pygame.draw.rect(screen, 'darkBlue', help_button_rect)
        pygame.draw.rect(screen, 'darkBlue', quit_button_rect)
        pygame.draw.rect(screen, 'white', num_box_rect)
        pygame.draw.rect(screen, 'black', plus_button_rect)
        pygame.draw.rect(screen, 'black', minus_button_rect)

        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(solve_text, solve_rect)
        screen.blit(help_text, help_rect)
        screen.blit(quit_text, quit_rect)

        screen.blit(num_label_text, num_label_rect)
        screen.blit(num_text, num_rect)
        screen.blit(plus_text, plus_rect)
        screen.blit(minus_text, minus_rect)

        pygame.display.update()
        clock.tick(60)

    if not quitting:
        return True
    return False

def plus_button():
    global disc_count
    if disc_count > 8:
        return
    else:
        disc_count += 1


def handle_click(mouse_pos):
    global quitting
    if play_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        game.play_game(disc_count, False)
        return False
    if solve_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        game.play_game(disc_count, True)
        return False
    if help_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        help.how_to_play()
        return False
    if quit_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        quitting = True
        return False
    if plus_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        plus_button()
        return True
    if minus_button_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
        minus_button()
        return True


def minus_button():
    global disc_count
    if disc_count < 2:
        return
    else:
        disc_count -= 1
