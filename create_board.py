import sys
import pygame
from math import pi, sin
import random

pygame.init()

size = display_width, display_height = 800, 600
BG_COLOR =              (117, 117, 117)
GRAY =                  (127, 127, 127)
BLACK =                 (  0,   0,   0)
WHITE =                 (255, 255, 255)
BUTTON_SELECTED_HOVER = (  0, 150, 136)
BUTTON_SELECTED =       (  0, 171, 153)
DARK_BLUE =             (  0,   0, 200)
BUTTON =                (  0, 151, 167)
BUTTON_HOVER =          (  0, 131, 143)
GREEN =                 (0  , 200,   0)
RED =                   (255,   0,   0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyDato")
clock = pygame.time.Clock()
level = ['Easy', 'Medium', 'Hard']  # game levels
selected_level = level[0]  # keep the game level in memory
game_started = 0  # in order to no to lose your point if clicking on other stuff by mistake
hex_filled = []  # to control which hexagon is already filled
hex_correct = []  # the list of correct answers. this is a sub-list of hex_filled
button_group = ['level', 'game_control']  # to control button behaviors in for diffent GUI parts
selected_hexagon = 0
hex_coords = []
corners = []
sides = []


def hive():
    if selected_level is level[0]:
        hive_struct = [3, 4, 5, 4, 3]
    elif selected_level is level[1]:
        hive_struct = [4, 5, 6, 7, 6, 5, 4]
    else:
        hive_struct = [5, 6, 7, 8, 9, 8, 7, 6, 5]

    return hive_struct


def hexagon_special_hexas():
    global corners, sides
    side_hexas = []
    hive()

        # get the coordinates of the big hexagon coreners
    corner_hexas = [[0, 0], [0, hive_struct[0] - 1], [int((len(hive_struct) - 1) / 2), 0], [int((len(hive_struct) - 1) / 2), len(hive_struct) - 1], [len(hive_struct) - 1, 0], [len(hive_struct) - 1, len(hive_struct) - 1]]
    # get the sides of the big hexagon - ordered clockwise: top, left_top, left_bottom, bottom, right_bottom, right_top
    for i in range(6):
        side_length = hive_struct[0] - 2
        for j in range(side_length):
            if i == 0:
                side_hexas.append([j + 1, 0])
            elif i == 1:
                side_hexas.append([(hive_struct[j]), j + 1])
            elif i == 2:
                side_hexas.append([len(hive_struct) - 2 - j, hive_struct[j]])
            elif i == 3:
                side_hexas.append([j + 1, len(hive_struct) - 1])
            elif i == 4:
                side_hexas.append([0, hive_struct[j]])
            elif i == 5:
                side_hexas.append([0, j + 1])
        sides.append(side_hexas)
        side_hexas = []

hexagon_special_hexas()


def create_hidato_list():
    list_len = sum(hive())
    for i, row in enumerate(hive()):
        for item in range(row):
            hex_coords.append([i, item])

    hidato_list = random.sample(range(1, list_len + 1), list_len)

    return hidato_list


# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for p in range(n + 1):
        p2x, p2y = poly[p % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intersect:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


# function for text creation
def text_objects(text, font):
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()


# function for text display
def message_display(x_text_center, y_text_center, text, fontsize):
    text_font = pygame.font.Font('freesansbold.ttf', fontsize)
    text_surf, text_rect = text_objects(text, text_font)
    text_rect.center = (x_text_center, y_text_center)
    screen.blit(text_surf, text_rect)


# function to draw a hexagon
def draw_hex(number, x, y, side_length, line_color, active_color, inactive_color, active_selected, inactive_selected):  # , fill_color
    global selected_hexagon
    fill_color = inactive_color if selected_hexagon != number else inactive_selected
    diagonal_sin = int((sin(pi/3)) * float(side_length))
    diagonal_cos = int((sin(pi/6)) * float(side_length))

    hex_coords = [x, y], [x + diagonal_sin, y + diagonal_cos], [x + diagonal_sin, y + diagonal_cos + side_length], [x, y + 2 * diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos]
    hex_coords_2 = [x, y + 1], [x - 1 + diagonal_sin, y + diagonal_cos], [x - 1 + diagonal_sin, y + diagonal_cos + side_length], [x, y - 1 + 2 * diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos]

    # check if mouse in hexagon
    mx, my = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    if point_inside_polygon(mx, my, hex_coords):
        if clicked[0]:
            selected_hexagon = number

        if selected_hexagon == number:
            fill_color = active_selected
        else:
            fill_color = active_color

    pygame.draw.polygon(screen, fill_color, hex_coords, 0)
    pygame.draw.aalines(screen, line_color, True, hex_coords, True)
    pygame.draw.aalines(screen, line_color, True, hex_coords_2, True)

    # text_surf, text_rect = text_objects(number, small_text)
    message_display(x, y + side_length, number, 18)


# draw the hive
def draw_hive():
    global hex_counter
    for i, hexa in enumerate(hive()):
        for hex_i in range(hexa):

            # mouse = pygame.mouse.get_pos()
            draw_hex(str(current_list[hex_counter]), 400 + hex_i * 50 - hexa * 25 + 1, 150 + i * 45 + 1, 30, WHITE, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER)
            hex_counter += 1


# function for creating buttons
def button(msg, x, y, w, h, inactive_color, active_color, inactive_selected, active_selected, group):
    global selected_level, current_list, selected_hexagon

    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    # check if mode button clicked and change current selection
    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
        if clicked[0]:
            if group is not button_group[1]:
                selected_level = msg
            elif group is button_group[1]:
                pygame.draw.rect(screen, active_selected, [x, y, w, h])
            current_list = create_hidato_list()
            selected_hexagon = 0

    # TODO accept only a single change per mouse click


    # check if button is selected and if mouse is hovering and change colors accordingly
    if selected_level == msg:
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, inactive_selected, [x, y, w, h])
        else:
            pygame.draw.rect(screen, active_selected, [x, y, w, h])
    else:
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, inactive_color, [x, y, w, h])
        else:
            pygame.draw.rect(screen, active_color, [x, y, w, h])

    # set button caption
    message_display(x + w / 2, y + h / 2, msg, 18)

    # TODO rounded corners for the buttons


current_list = create_hidato_list()
print(corners, sides)

while 1:
    hex_counter = 0  # helps in creating the numbering
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)

    draw_hive()
    # create difficulty selection buttons
    for b in range(len(level)):
        button(level[b], 100 + b * 110, 50, 80, 40, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER, button_group[0])

    # create start new game button
    button('New Game', 500, 50, 120, 60, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER, button_group[1])

    hex_counter = 0
    hex_coords = sides = []
    pygame.display.flip()
