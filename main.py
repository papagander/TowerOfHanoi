import pygame
from sys import exit

disc_count = 3

screen_height = 520
screen_width = 1200

disc_height = 60

stack_width = 256
stack_height = 52
stack_pad = 50
stack_x_pos = [stack_pad, (screen_width - stack_width) / 2, screen_width - stack_width - stack_pad]

# vars indicating where to draw the next disc per stack
default_empty_slot = screen_height - stack_height - disc_height
empty_slot_y = [default_empty_slot, default_empty_slot, default_empty_slot]

# vars to store which disc on top of each stack
top_disc_size = [-1, -1, -1]

# vars used to store mouse offset when grabbing disc
mouse_offset_x = 0
mouse_offset_y = 0

# var used to store selected disc
selected_disc = None

# rects defining the area for the mouse to drop on stacks
stack_0_drop_zone = pygame.Rect(0, 0, screen_width / 3, screen_height)
stack_1_drop_zone = pygame.Rect(screen_width / 3, 0, screen_width / 3, screen_height)
stack_2_drop_zone = pygame.Rect(2 * screen_width / 3, 0, screen_width / 3, screen_height)


class Disc:
    def __init__(self, dex):
        self.index = dex
        self.color = get_color(dex)
        self.width = stack_width - (1 + dex) * 32
    my_rect = pygame.Rect(100, 100, 100, disc_height)
    stack_num = 0


class Stack:
    def __init__(self, dex):
        self.index = dex
        self.drop_zone = pygame.Rect(dex * screen_width / 3, 0, screen_width / 3, screen_height)
    top_disc_size = -1

def draw_frame():
    screen.fill(background_fill_color)
    pygame.draw.rect(screen, 'brown', [stack_x_pos[0], screen_height - stack_height, stack_width, disc_height], width=0)
    pygame.draw.rect(screen, 'brown', [stack_x_pos[1], screen_height - stack_height, stack_width, disc_height], width=0)
    pygame.draw.rect(screen, 'brown', [stack_x_pos[2], screen_height - stack_height, stack_width, disc_height], width=0)


def can_add_to_stack(disc_num, stack_num):
    if disc_num > top_disc_size[stack_num]:
        return True
    return False


def can_remove_from_stack(disc_num):
    stack_num = discs[disc_num].stack_num
    if disc_num == top_disc_size[stack_num]:
        return True
    return False


def get_new_top_disc(stack_num):
    top_disc_size[stack_num] = -1
    for disc in discs:
        if disc.stack_num == stack_num:
            if disc.index >= top_disc_size[stack_num]:
                top_disc_size[stack_num] = disc.index


def get_top_slot(stack_num):
    empty_slot_y[stack_num] = default_empty_slot
    for disc in discs:
        if disc.stack_num == stack_num:
            empty_slot_y[stack_num] -= disc_height


def add_to_stack(disc, stack_num):
    from_stack_num = disc.stack_num
    top_disc_size[stack_num] = disc.index
    disc.my_rect = pygame.Rect(stack_x_pos[stack_num], empty_slot_y[stack_num],
                               disc.width, disc_height)
    disc.stack_num = stack_num
    get_new_top_disc(from_stack_num)
    top_disc_size[stack_num] = disc.index
    empty_slot_y[from_stack_num] += disc_height
    empty_slot_y[stack_num] -= disc_height
    get_top_slot(from_stack_num)
    get_top_slot(stack_num)


def initialise(disc, stack_num):
    from_stack_num = disc.stack_num
    disc.stack_num = stack_num
    top_disc_size[stack_num] = disc.index
    disc.my_rect = pygame.Rect(stack_x_pos[stack_num], empty_slot_y[stack_num],
                               disc.width, disc_height)
    empty_slot_y[stack_num] -= disc_height
    get_new_top_disc(from_stack_num)


def get_color(dex):
    index = dex % 7
    if index == 0:
        return 'darkRed'
    if index == 1:
        return 'orange'
    if index == 2:
        return 'yellow'
    if index == 3:
        return 'green'
    if index == 4:
        return 'blue'
    if index == 5:
        return 'indigo'
    if index == 6:
        return 'violet'


def get_mouse_zone():
    if stack_0_drop_zone.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        return 0
    if stack_1_drop_zone.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        return 1
    if stack_2_drop_zone.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        return 2
    else:
        return -1


def get_selection():
    for disc in discs:
        if disc.my_rect.collidepoint(pygame.mouse.get_pos()):
            return disc.index
    return -1


def check_for_win():
    for disc in discs:
        if disc.stack_num != 2:
            return False
    return True


pygame.init()
background_fill_color = '#ccccff'
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tower of Hanoi')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/pixelType.ttf', 50)
win_text = test_font.render('You Win!', False, 'darkGreen')

discs = []
for i in range(0, disc_count):
    discs.append(Disc(i))
for disc in discs:
    initialise(disc, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selected_disc is None:
                selection_index = get_selection()
                if selection_index == -1:
                    continue
                if not can_remove_from_stack(selection_index):
                    continue
                selected_disc = discs[selection_index]
                from_stack_num = selected_disc.stack_num
                empty_slot_y[from_stack_num] += disc_height
                mouse_offset_x = pygame.mouse.get_pos()[0] - selected_disc.my_rect[0]
                mouse_offset_y = pygame.mouse.get_pos()[1] - selected_disc.my_rect[1]
            else:
                stack_num = get_mouse_zone()
                if can_add_to_stack(selected_disc.index, stack_num):
                    add_to_stack(selected_disc, stack_num)
                else:
                    add_to_stack(selected_disc, from_stack_num)
                selected_disc = None
        if event.type == pygame.MOUSEMOTION and selected_disc is not None:
            pos = pygame.mouse.get_pos()
            selected_disc.my_rect = pygame.Rect(pos[0] - mouse_offset_x, pos[1] - mouse_offset_y,
                                                selected_disc.width, disc_height)
    draw_frame()
    for disc in discs:
        pygame.draw.rect(screen, disc.color, disc.my_rect)
    if check_for_win():
        screen.blit(win_text, (400, 20))
    pygame.display.update()
    clock.tick(60)
