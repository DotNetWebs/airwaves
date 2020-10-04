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






