import numpy as np
import math
import pygame

def plot_x(x, left, width):
    home_x = round(((x - left) / width) * 1000, 2)
    return int(home_x)


def plot_y(y, top, height):
    home_y = round(((top - y) / height) * 1000, 2)
    return int(home_y)


def cart2pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)


def cart2pol2(x, y):
    radius = math.sqrt(x * x + y * y)

    if x == 0:
        if y > 0:
            # Bearing is 180
            theta = -90
        else:
            # Bearing is 0
            theta = -270
    else:
        # theta in radians
        theta = math.atan(y / x)
        # radians to degrees
        theta = 180 * theta / math.pi

    return (radius, theta)


def draw_scale(scale, key, screen, map, color, font):
    for count, angle in enumerate(scale.major_angles()):
        radar = (map.home_x, map.home_y)
        radar_len = 750
        note_len = 300
        note_angle = (360 / len(scale.major_angles())) / 2
        x = radar[0] + math.cos(math.radians(angle - 90)) * radar_len
        note_x = radar[0] + math.cos(math.radians(angle - 90 + note_angle)) * note_len
        y = radar[1] + math.sin(math.radians(angle - 90)) * radar_len
        note_y = radar[1] + math.sin(math.radians(angle - 90 + note_angle)) * note_len
        note = key[count]
        text_note = font.render(note + " " + str(int(angle)), True, color, 22)
        text_note_plot = (note_x, note_y)
        screen.blit(text_note, text_note_plot)
        pygame.draw.line(screen, color, radar, (x, y), 2)



