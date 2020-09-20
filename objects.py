import math
from geopy.distance import great_circle
import helpers
import settings
import pretty_midi
import sys

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
            text_flight = self.font.render(infopanel.get_registration(self), True, settings.green)
            text_alt = self.font.render("Alt: " + str(infopanel.get_baro_alt(self)), True, settings.green)
            text_heading = self.font.render("HDG: " + str(infopanel.get_heading(self)), True, settings.green)
            text_ias = self.font.render("IAS: " + str(infopanel.get_IAS(self)), True, settings.green)
            text_range = self.font.render("Range: " + infopanel.get_range(self), True, settings.green)
            text_bearing = self.font.render("Bearing: " + infopanel.get_bearing(self), True, settings.green)
            text_note = self.font.render("Note: " + infopanel.get_note(self).note_name, True,
                                         settings.green)
            text_hz = self.font.render("Freq: " + str(infopanel.get_note(self).get_hz()) + " Hz",
                                       True,
                                       settings.green)

            if settings.debug_mode:
                text_x = self.font.render("X: " + infopanel.get_x(self), True, settings.green)
                text_y = self.font.render("Y: " + infopanel.get_y(self), True, settings.green)

            self.panel_surface.fill((0, 0, 0))
            self.panel_surface.blit(text_flight, (10, 10))
            self.panel_surface.blit(text_alt, (10, 30))
            self.panel_surface.blit(text_heading, (10, 50))
            self.panel_surface.blit(text_ias, (10, 70))
            self.panel_surface.blit(text_bearing, (10, 90))
            self.panel_surface.blit(text_range, (10, 110))

            if settings.debug_mode:
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
