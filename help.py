import pygame

SCREEN_WIDTH = 460
SCREEN_HEIGHT = 440
background_fill_color = '#ffcccc'


def how_to_play():
    pygame.init()
    title_font = pygame.font.Font('font/pixelType.ttf', 100)
    text_font = pygame.font.Font('font/pixelType.ttf', 32)

    lines = [text_font.render('Click a disc to select it, then click again', False, 'black'),
             text_font.render('over the desired stack to drop it.', False, 'black'),
             text_font.render('  ', False, 'black'),
             text_font.render('Discs cannot be placed on top of smaller discs.', False, 'black'),
             text_font.render('Stack all the discs', False, 'black'),
             text_font.render('on the right stand to win!', False, 'black'),
             text_font.render('  ', False, 'black'),
             text_font.render('Press escape to return to menu', False, 'black'),
             ]


    rects = []
    rect_y = 80
    for line in lines:
        rects.append(line.get_rect(center=(SCREEN_WIDTH / 2, rect_y)))
        rect_y += 40

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('How to play')
    clock = pygame.time.Clock()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(background_fill_color)
        for i in range(0, 8):
            screen.blit(lines[i], rects[i])

        pygame.display.update()
