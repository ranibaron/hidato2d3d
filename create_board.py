import sys
import pygame
from math import pi, sin

pygame.init()

size = display_width, display_height = 1000, 600
BG_COLOR =              (117, 117, 117)
GRAY =                  (127, 127, 127)
BLACK =                 (  0,   0,   0)
WHITE =                 (255, 255, 255)
BUTTON_SELECTED_HOVER = (  0, 150, 136)
BUTTON_SELECTED =       (  0, 171, 153)
DARK_BLUE =             (  0,   0, 200)
BUTTON =                (  0, 131, 143)
BUTTON_HOVER =          (  0, 151, 167)
GREEN =                 (0  , 200,   0)
RED =                   (255,   0,   0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyDato")
clock = pygame.time.Clock()
level = ['Easy', 'Medium', 'Hard']  # optional game levels
selected_level = level[0]  # keep the game level in memory
game_started = 0  # in order to no to lose your point if clicking on other stuff by mistake
hex_counter = 0
hex_filled = []
hex_correct = []
button_group = []

def hive():
    if selected_level is level[0]:
        hive_struct = [3, 4, 5, 4, 3]
    elif selected_level is level[1]:
        hive_struct = [4, 5, 6, 7, 6, 5, 4]
    else:
        hive_struct = [5, 6, 7, 8, 9, 8, 7, 6, 5]
    return hive_struct


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
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


# function for text display
def message_display(text):
    largeText = pygame.font.Font('freesans.ttf',100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect)


# function to draw a hexagon
def draw_hex(number, x, y, side_length, line_color, line_width):  # , fill_color

    diagonal_sin = int((sin(pi/3)) * float(side_length))
    diagonal_cos = int((sin(pi/6)) * float(side_length))

    hex_coords = [x, y], [x + diagonal_sin, y + diagonal_cos], [x + diagonal_sin, y + diagonal_cos + side_length], [x, y  + 2 * diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos]
    hex_coords_2 = [x, y + 1], [x - 1 + diagonal_sin, y + diagonal_cos], [x - 1 + diagonal_sin, y + diagonal_cos + side_length], [x , y - 1 + 2 * diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos]

    # check if mouse in hexagon
    mx, my = pygame.mouse.get_pos()
    if point_inside_polygon(mx, my, hex_coords):
        line_color = DARK_BLUE

    pygame.draw.aalines(screen, line_color, True, hex_coords, True)
    pygame.draw.aalines(screen, line_color, True, hex_coords_2, True)

    small_text = pygame.font.Font("freesansbold.ttf", 18)
    text_surf, text_rect = text_objects(number, small_text)
    text_rect.center = (x, y + side_length)
    screen.blit(text_surf, text_rect)


# function for creating buttons
def button(msg, x, y, w, h, inactive_color, active_color, inactive_selected, active_selected):
    global selected_level

    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    # check if mode button clicked and change current selection
    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
        if clicked[0] and msg is not "New Game":
            selected_level = msg

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
    small_text = pygame.font.Font("freesansbold.ttf", 18)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

    # TODO rouned corners for the buttons

while 1:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)

    for i, hexa in enumerate(hive()):
        for hex_i in range(hexa):
            hex_counter += 1
            draw_hex(str(hex_counter), 400 + hex_i * 50 - hexa * 25 + 1, 150 + i * 45 + 1, 30, WHITE, True)
            # pygame.draw.circle(screen, GREEN, [400 + hex_i * 50 - hexa * 25, 150 + i * 45 + 25], 24)

    # create difficulty selection buttons
    for b in range(len(level)):
        button(level[b], 100 + b * 110, 50, 80, 40, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER)

    # create start new game button
    button('New Game', 500 + b * 110, 50, 120, 60, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER)

    hex_counter = 0
    pygame.display.flip()
