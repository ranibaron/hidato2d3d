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
level = ['easy', 'medium', 'hard']  # optional game levels
selected = level[0]  # keep the game level in memory
game_started = 0  # in order to no to lose your point if clicking on other stuff by mistake


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
def draw_hex(x, y, side_length, line_color, line_width):  # , fill_color
    diagonal_sin = int((sin(pi/3)) * float(side_length))
    diagonal_cos = int((sin(pi/6)) * float(side_length))

    hex_coords = [x, y], [x + diagonal_sin, y + diagonal_cos], [x + diagonal_sin, y + diagonal_cos + side_length], [x, y  + 2 * diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos + side_length], [x - diagonal_sin, y + diagonal_cos]
    hex_coords_2 = [x, y + 1], [x - 1 + diagonal_sin, y + diagonal_cos], [x - 1 + diagonal_sin, y + diagonal_cos + side_length], [x , y - 1 + 2 * diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos + side_length], [x + 1 - diagonal_sin, y + diagonal_cos]
    pygame.draw.aalines(screen, line_color, True, hex_coords, True)
    pygame.draw.aalines(screen, line_color, True, hex_coords_2, True)


# function for creating buttons
def button(msg, x, y, w, h, inactive_color, active_color, inactive_selected, active_selected):
    global selected

    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
        if clicked[0]:
            selected = msg

    if selected == msg:
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, inactive_selected, [x, y, w, h])
        else:
            pygame.draw.rect(screen, active_selected, [x, y, w, h])
    else:
        if x <= mouse[0] <= x + w and y <= mouse[1] <= y + h:
            pygame.draw.rect(screen, inactive_color, [x, y, w, h])
        else:
            pygame.draw.rect(screen, active_color, [x, y, w, h])

    small_text = pygame.font.Font("freesansbold.ttf", 18)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(text_surf, text_rect)

    # TODO rouned corners for the buttons


while 1:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)
    draw_hex(100, 100, 30, WHITE, True)
#    pygame.draw.circle(screen, GREEN, [100, 130], 24)

# create difficulty selection buttons
#     group = ButtonGroup()
    for b in range(len(level)):
        button(level[b], 100 + b * 110, 100, 100, 40, BUTTON, BUTTON_HOVER, BUTTON_SELECTED, BUTTON_SELECTED_HOVER)

    pygame.display.flip()
