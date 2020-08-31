import numpy as np
import math
import pygame
import midiout
import settings
import objects
import sys

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


def plot_aircraft(scale, aircraft, screen, font, font_large, panel, infopanel):

    bearing_colour = settings.red
    # check for note boundary
    for count, angle in enumerate(scale.major_angles()):

        try:
            if int(aircraft.corrected_bearing()) - 1 <= int(angle) <= int(aircraft.corrected_bearing()) + 1:
                bearing_colour = settings.green
                aw_note = objects.aw_note()
                aw_note.note_name = scale.key[count] + '2'
                aw_note.note_number = aw_note.note2number(aw_note.note_name)
                infopanel.set_registration(aircraft.registration)
                infopanel.set_range(str(aircraft.range(settings.home_pos)))
                infopanel.set_bearing(str(aircraft.corrected_bearing()))
                infopanel.set_note(aw_note)
                infopanel.set_x(str(aircraft.plotted_x()))
                infopanel.set_y(str(aircraft.plotted_y()))
                midiout.send_note(aw_note, font, panel, aircraft)
                infopanel.update_display()
                break
            else:
                bearing_colour = settings.red
        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass

    plotted_xy = (aircraft.plotted_x(), aircraft.plotted_y())
    pygame.draw.circle(screen, (settings.white), (plotted_xy), 10)
    pygame.draw.circle(screen, (bearing_colour), (plotted_xy), 5)

    text_flight = font.render(aircraft.registration, True, bearing_colour)
    text_alt = font.render("Alt: " + str(aircraft.baro_alt), True, bearing_colour)
    text_heading = font.render("HDG: " + str(aircraft.heading), True, bearing_colour)
    text_ias = font.render("IAS: " + str(aircraft.IAS), True, bearing_colour)
    text_bearing = font.render("Bearing: " + str(aircraft.corrected_bearing()), True, bearing_colour)
    text_range = font.render("Range: " + str(aircraft.range(settings.home_pos)), True, bearing_colour)

    screen.blit(text_flight, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer))
    screen.blit(text_alt, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 2))
    screen.blit(text_heading, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 3))
    screen.blit(text_ias, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 4))
    screen.blit(text_bearing, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 5))
    screen.blit(text_range, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 6))
