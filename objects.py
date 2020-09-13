import math
from geopy.distance import great_circle
import objects
import helpers
import settings
import pretty_midi
import sys
import pygame
import midiout

class map:
    def __init__(self, lat, long, offset, height, width):
        self.centre = (lat, long)
        self.height = height
        self.width = width
        self.offset = offset
        self.tl = (self.centre[0] + self.offset,
                   self.centre[1] - (self.offset / (math.cos(math.radians(self.centre[0] + self.offset)))))
        self.tr = (self.centre[0] + self.offset,
                   self.centre[1] + (self.offset / (math.cos(math.radians(self.centre[0] + self.offset)))))
        self.br = (self.centre[0] - self.offset,
                   self.centre[1] + (self.offset / (math.cos(math.radians(self.centre[0] - self.offset)))))
        self.bl = (self.centre[0] - self.offset,
                   self.centre[1] - (self.offset / (math.cos(math.radians(self.centre[0] - self.offset)))))
        self.top = great_circle(self.tl, self.tr).nautical
        self.right = great_circle(self.tr, self.br).nautical
        self.bottom = great_circle(self.bl, self.br).nautical
        self.left = great_circle(self.bl, self.tl).nautical
        self.left_x = (self.tl[1] + self.bl[1]) / 2
        self.right_x = (self.tr[1] + self.br[1]) / 2
        self.x_width = round(self.right_x - self.left_x, 1)
        self.top_y = (self.tl[0] + self.tr[0]) / 2
        self.bottom_y = (self.bl[0] + self.br[0]) / 2
        self.y_height = round(self.top_y - self.bottom_y, 1)
        self.check = math.cos(math.radians(self.top_y))
        self.check2 = math.cos(math.radians(self.bottom_y))
        self.check3 = round(self.y_height / ((self.check + self.check2) / 2), 1)
        self.tl_dist = great_circle(self.tl, self.centre).nautical
        self.tr_dist = great_circle(self.tr, self.centre).nautical
        self.bl_dist = great_circle(self.bl, self.centre).nautical
        self.br_dist = great_circle(self.br, self.centre).nautical
        self.nm_scale_factor_x = self.width / ((self.top + self.bottom) / 2)
        self.nm_scale_factor_y = height / ((self.left + self.right) / 2)
        self.home_x = helpers.plot_x(self.centre[1], self.left_x, self.x_width)
        self.home_y = helpers.plot_y(self.centre[0], self.top_y, self.y_height)


class plotter:
    def __init__(self, infopanel):
        self.infopanel =  infopanel
        self.active_aircraft = None
        self.active_note = None

    def plot_aircraft(self, scale, aircraft, screen, font, font_large, panel):
        bearing_colour = settings.red
        # check for note boundary
        for count, angle in enumerate(scale.major_angles()):

            try:
                if int(aircraft.corrected_bearing()) - 1 <= int(angle) <= int(aircraft.corrected_bearing()) + 1:
                    if aircraft.plotted_x() > 0 < 1000 and aircraft.plotted_y() > 0 < 1000:
                        bearing_colour = settings.green
                        note = self.set_note(count, scale)
                        self.update_panel(aw_note=note)
                        self.active_aircraft = aircraft
                        break
                else:
                    bearing_colour = settings.red
            except Exception as e:
                line = sys.exc_info()[-1].tb_lineno
                exc_type, exc_obj, exc_tb = sys.exc_info()
                pass

        if self.active_aircraft:
            if self.active_aircraft.registration == aircraft.registration:
                self.active_aircraft = aircraft
                bearing_colour=settings.green

        plotted_xy = (aircraft.plotted_x(), aircraft.plotted_y())
        pygame.draw.circle(screen, (settings.white), (plotted_xy), 10)
        pygame.draw.circle(screen, (bearing_colour), (plotted_xy), 5)

        text_flight = font.render(aircraft.registration, True, bearing_colour)
        text_alt = font.render("Alt: " + str(aircraft.baro_alt), True, bearing_colour)
        text_heading = font.render("HDG: " + str(aircraft.heading), True, bearing_colour)
        text_ias = font.render("IAS: " + str(aircraft.IAS), True, bearing_colour)
        text_bearing = font.render("Bearing: " + str(aircraft.corrected_bearing()), True, bearing_colour)
        text_range = font.render("Range: " + str(aircraft.range(settings.home_pos)), True, bearing_colour)

        text_x = font.render("X: " + str(aircraft.plotted_x()), True, bearing_colour)
        text_y = font.render("Y: " + str(aircraft.plotted_y()), True, bearing_colour)

        screen.blit(text_flight, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer))
        screen.blit(text_alt, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 2))
        screen.blit(text_heading, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 3))
        screen.blit(text_ias, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 4))
        screen.blit(text_bearing, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 5))
        screen.blit(text_range, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 6))
        screen.blit(text_x, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 7))
        screen.blit(text_y, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 8))

    def set_note(self, count, scale):
        note = objects.aw_note()
        note.note_name = scale.key[count] + '2'
        note.note_number = note.note2number(note.note_name)
        self.active_note = note
        midiout.send_note(note)
        return note

    def update_panel(self, aircraft=None, aw_note=None):

        if aircraft:
            self.infopanel.set_baro_alt(aircraft.baro_alt)
            self.infopanel.set_heading(aircraft.heading)
            self.infopanel.set_IAS(aircraft.IAS)
            self.infopanel.set_registration(aircraft.registration)
            self.infopanel.set_range(str(aircraft.range(settings.home_pos)))
            self.infopanel.set_bearing(str(aircraft.corrected_bearing()))
            self.infopanel.set_x(str(aircraft.plotted_x()))
            self.infopanel.set_y(str(aircraft.plotted_y()))

        if aw_note:
            self.infopanel.set_note(aw_note)

        self.infopanel.update_display()


class aircraft:
    def __init__(self, flight, baro_alt, heading, IAS, lat, long, map):
        self.registration = flight
        self.baro_alt = baro_alt
        self.heading = heading
        self.IAS = IAS
        self.position = (lat, long)
        self.map = map

    def position_string(self):
        return str(round(self.position[0], 3)) + "  " + str(round(self.position[1], 3))

    def plotted_y(self):
        if self.map:
            return helpers.plot_y(self.position[0], self.map.top_y, self.map.y_height)
        else:
            return 0

    def plotted_x(self):
        if self.map:
            return helpers.plot_x(self.position[1], self.map.left_x, self.map.x_width)
        else:
            return 0

    def cartesian(self):
        if self.map:
            return helpers.cart2pol2(self.plotted_x() - 500, self.plotted_y() - 500)
        else:
            return (0, 0)

    def corrected_bearing(self):
        if self.plotted_x() > 500:
            return int(self.cartesian()[1]) + 90
        else:
            return int(self.cartesian()[1]) + 90 + 180

    def range(self, home):
        return round(great_circle(home, self.position).nautical, 2)

    def blit_XY(self):
        return ()


class scale:
    def __init__(self, key):
        self.key = key
        self.numberofnotes = len(key)

    def major_angles(self):
        major_angles = [0, ]

        for arc in range(1, self.numberofnotes):

            if self.numberofnotes:
                major_angles.append(arc * 360 / self.numberofnotes)

        return major_angles


class aw_note:
    def __init__(self):
        self.note_number = 0
        self.note_name = ""

    def note2number(self, note_name):
        note_number = pretty_midi.note_name_to_number(note_name)
        return note_number

    def get_hz(self):
        return round(pretty_midi.note_number_to_hz(self.note_number),2)


class infopanel:
    def __init__(self, pygame, font, panel_surface, screen):
        self.pygame = pygame
        self.font = font
        self.panel_surface = panel_surface
        self.screen = screen
        self.registration = ""
        self.baro_alt = ""
        self.heading = ""
        self.IAS = ""
        self.range = ""
        self.bearing = ""
        self.note = aw_note()
        self.x = ""
        self.y = ""

    def get_registration(self):
        return self.registration

    def set_registration(self, reg):
        self.registration = reg

    def get_baro_alt(self):
        return self.baro_alt

    def set_baro_alt(self, alt):
        self.baro_alt = alt

    def get_IAS(self):
        return self.IAS

    def set_IAS(self, ias):
        self.IAS = ias

    def get_heading(self):
        return self.heading

    def set_heading(self, hdg):
        self.heading = hdg

    def get_range(self):
        return self.range

    def set_range(self, rng):
        self.range = rng

    def get_bearing(self):
        return self.bearing

    def set_bearing(self, brg):
        self.bearing = brg

    def get_note(self):
        return self.note

    def set_note(self, note):
        self.note = note

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def update_display(self):
        try:
            text_alt = self.font.render("Alt: " + str(infopanel.get_baro_alt(self)), True, settings.blue)
            text_heading = self.font.render("HDG: " + str(infopanel.get_heading(self)), True, settings.blue)
            text_ias = self.font.render("IAS: " + str(infopanel.get_IAS(self)), True, settings.blue)
            text_flight = self.font.render("Reg: " + infopanel.get_registration(self), True, settings.blue)
            text_range = self.font.render("Range: " + infopanel.get_range(self), True, settings.blue)
            text_bearing = self.font.render("Bearing: " + infopanel.get_bearing(self), True, settings.blue)
            text_note = self.font.render("Note: " + infopanel.get_note(self).note_name, True,
                                         settings.blue)
            text_hz = self.font.render("Freq: " + str(infopanel.get_note(self).get_hz()) + " Hz",
                                       True,
                                       settings.blue)
            text_x = self.font.render("X: " + infopanel.get_x(self), True, settings.blue)
            text_y = self.font.render("Y: " + infopanel.get_y(self), True, settings.blue)
            self.panel_surface.fill((255, 255, 255))

            self.panel_surface.blit(text_alt, (10, 10))
            self.panel_surface.blit(text_heading, (10, 30))
            self.panel_surface.blit(text_ias, (10, 50))

            self.panel_surface.blit(text_flight, (10, 70))
            self.panel_surface.blit(text_bearing, (10, 90))
            self.panel_surface.blit(text_range, (10, 110))
            self.panel_surface.blit(text_x, (10, 130))
            self.panel_surface.blit(text_y, (10, 150))
            self.panel_surface.blit(text_note, (10, 190))
            self.panel_surface.blit(text_hz, (10, 210))
            self.screen.blit(self.panel_surface, (1000, 0))
            self.pygame.display.flip()
        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass

    def init_display(self):
        try:
            self.panel_surface.fill((255, 255, 255))
            self.screen.blit(self.panel_surface, (1000, 0))
            self.pygame.display.flip()
        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass
