import sys
import pygame
import subprocess
from sys import exit

screen = None

screen_height = 600
screen_width = 1200

MOV_SPEED = 200
# vertical length of discs
disc_height = 60
# how much smaller discs should get each time
disc_step = 20

# dimensions for stack stands
stand_width = 256
stand_height = 52

# margin between outer stacks and wall
stack_pad = 50

# defines the x positions for the stack bases
stack_x_pos = [stack_pad, (screen_width - stand_width) / 2, screen_width - stand_width - stack_pad]
stack_y_pos = screen_height - stand_height
# indicates y height to draw the first disc per stack
bottom_disc_y = screen_height - stand_height - disc_height

disc_count = 5
all_discs = []
stacks = []

mov_list = []
mov_num = 0
MOV_EVENT = pygame.USEREVENT + 1


class Disc:
    def __init__(self, dex):
        self.size = dex
        self.color = get_color(dex)
        self.width = stand_width - (1 + dex) * disc_step

    my_rect = pygame.Rect(100, 100, 100, disc_height)
    # all discs start on the first stack
    stack_num = 0


class Stack:
    def __init__(self, dex):
        self.index = dex
        self.drop_zone = pygame.Rect(dex * screen_width / 3, 0, screen_width / 3, screen_height)
        self.x_pos = stack_x_pos[dex]
        self.my_discs = []
        self.top = -1

    def push(self, new_disc):
        if self.top != -1:
            if new_disc.size < self.peek().size:
                return False
        new_disc.stack_num = self.index
        self.top += 1
        self.my_discs.append(new_disc)
        self.stack_discs()

    def pop(self):
        if self.top == -1:
            return None
        self.top -= 1
        popped_disc = self.my_discs.pop()
        self.stack_discs()
        return popped_disc

    def peek(self):
        if self.top == -1:
            return None
        return self.my_discs[self.top]

    def stack_discs(self):
        disc_y = bottom_disc_y
        for d in self.my_discs:
            disc_x = self.x_pos + (stand_width - d.width) / 2
            d.my_rect = pygame.Rect(disc_x, disc_y, d.width, disc_height)
            disc_y -= disc_height

    def draw(self):
        pygame.draw.rect(screen, 'brown', [self.x_pos, screen_height - stand_height, stand_width, disc_height], width=0)
        for d in self.my_discs:
            pygame.draw.rect(screen, d.color, d.my_rect)
    # stores the y coord to draw the next disc pushed
    # empty_slot_y = bottom_disc_y


def can_add_to_stack(_disc, _stack_num):
    top_disc = stacks[_stack_num].peek()
    if top_disc is None:
        return True
    if top_disc.size < _disc.size:
        return True
    return False


def can_remove_from_stack(disc_num):
    _disc = all_discs[disc_num]
    _stack = stacks[_disc.stack_num]
    top_disc = _stack.peek()
    if top_disc.size == _disc.size:
        return _disc.stack_num
    return -1


def get_color(dex):
    index = dex % 7
    if index == 0:
        return 'red'
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
    mouse_pos = pygame.mouse.get_pos()
    for stack in stacks:
        if stack.drop_zone.collidepoint(mouse_pos[0], mouse_pos[1]):
            return stack.index
    return -1


def get_selection():
    for d in all_discs:
        if d.my_rect.collidepoint(pygame.mouse.get_pos()):
            return d.size
    return -1


def check_for_win():
    for d in all_discs:
        if d.stack_num != 2:
            return False
    return True


def draw_stacks():
    for stack in stacks:
        stack.draw()


def draw_selected_disc(my_disc, mouse_offset_x, mouse_offset_y):
    if my_disc is None:
        return
    _x = pygame.mouse.get_pos()[0] - mouse_offset_x
    _y = pygame.mouse.get_pos()[1] - mouse_offset_y
    pygame.draw.rect(screen, my_disc.color, [_x, _y, my_disc.width, disc_height], width=0)


def get_left_stack_num(from_stack_num):
    if from_stack_num == 0:
        return 2
    else:
        return from_stack_num - 1


def get_right_stack_num(from_stack_num):
    if from_stack_num == 2:
        return 0
    else:
        return from_stack_num + 1


def auto_mov():
    global mov_num
    to_stack_num, from_stack_num = mov_list[mov_num][0], mov_list[mov_num][1]
    mov_num += 1
    stacks[to_stack_num].push(stacks[from_stack_num].pop())


def mov_stack_right(disc_num):
    global mov_list
    if disc_num < disc_count - 1:
        mov_stack_left(disc_num + 1)
        from_stack_num = all_discs[disc_num].stack_num
        to_stack_num = get_right_stack_num(from_stack_num)
        all_discs[disc_num].stack_num = to_stack_num
        mov_list.append([to_stack_num, from_stack_num])
        mov_stack_left(disc_num + 1)
    else:
        from_stack_num = all_discs[disc_num].stack_num
        to_stack_num = get_right_stack_num(from_stack_num)
        all_discs[disc_num].stack_num = to_stack_num
        mov_list.append([to_stack_num, from_stack_num])


def mov_stack_left(disc_num):
    global mov_list
    if disc_num < disc_count - 1:
        mov_stack_right(disc_num + 1)
        from_stack_num = all_discs[disc_num].stack_num
        to_stack_num = get_left_stack_num(from_stack_num)
        all_discs[disc_num].stack_num = to_stack_num
        mov_list.append([to_stack_num, from_stack_num])
        mov_stack_right(disc_num + 1)
    else:
        from_stack_num = all_discs[disc_num].stack_num
        to_stack_num = get_left_stack_num(from_stack_num)
        all_discs[disc_num].stack_num = to_stack_num
        mov_list.append([to_stack_num, from_stack_num])


def play_game(_disc_count, solve_mode):
    global disc_count
    global screen
    global all_discs
    global stacks
    global mov_list
    global mov_num

    all_discs = []
    stacks = []
    mov_list = []
    mov_num = 0

    screen = pygame.display.set_mode((screen_width, screen_height))
    # var used to store selected disc
    selected_disc = None
    # stack the selected disc is from
    last_stack = None
    disc_count = _disc_count
    # vars used to store mouse offset when grabbing disc
    mouse_offset_x = 0
    mouse_offset_y = 0

    stacks.append(Stack(0))
    stacks.append(Stack(1))
    stacks.append(Stack(2))

    for i in range(0, disc_count):
        all_discs.append(Disc(i))
    for disc in all_discs:
        stacks[0].push(disc)

    pygame.init()
    background_fill_color = '#ccccff'
    pygame.display.set_caption('Tower of Hanoi')
    clock = pygame.time.Clock()

    font = pygame.font.Font('font/pixelType.ttf', 50)
    win_text = font.render('You Win!', False, 'darkGreen')
    quit_text = font.render('press esc to quit', False, 'darkGreen')

    if solve_mode:
        pygame.time.set_timer(MOV_EVENT, MOV_SPEED)
        mov_stack_left(0)
    for disc in all_discs:
        disc.stack_num = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if not solve_mode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if selected_disc is None:
                        selection_index = get_selection()
                        if selection_index == -1:
                            continue
                        from_stack_num = can_remove_from_stack(selection_index)
                        if from_stack_num == -1:
                            continue
                        selected_disc = stacks[from_stack_num].pop()
                        mouse_offset_x = pygame.mouse.get_pos()[0] - selected_disc.my_rect[0]
                        mouse_offset_y = pygame.mouse.get_pos()[1] - selected_disc.my_rect[1]
                    else:
                        stack_num = get_mouse_zone()
                        if can_add_to_stack(selected_disc, stack_num):
                            stacks[stack_num].push(selected_disc)
                        else:
                            stacks[from_stack_num].push(selected_disc)
                        selected_disc = None
            if event.type == MOV_EVENT and solve_mode:
                auto_mov()
        screen.fill(background_fill_color)
        draw_stacks()
        draw_selected_disc(selected_disc, mouse_offset_x, mouse_offset_y)

        if check_for_win():
            screen.blit(win_text, (400, 20))
            screen.blit(quit_text, (400, 120))
            running = False
        pygame.display.update()
        clock.tick(60)

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
