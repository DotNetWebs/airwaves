import math
from geopy.distance import great_circle
import helpers
import settings


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


class infopanel:
    def __init__(self, pygame, font, panel_surface, screen):
        self.pygame = pygame
        self.font = font
        self.panel_surface = panel_surface
        self.screen = screen
        self.registration = ""
        self.range = ""
        self.bearing = ""
        self.note = ""
        self.hz = 0.0
        self.x = ""
        self.y = ""

    def get_registration(self):
        return self.registration

    def set_registration(self, reg):
        self.registration = reg

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

    def get_hz(self):
        return round(self.hz, 2)

    def set_note(self, note, hz):
        self.note = note
        self.hz = hz

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def update_display(self):
        self.screen.blit(self.panel_surface, (1000, 0))
        text_flight = self.font.render("Reg: " + infopanel.get_registration(self), True, settings.blue)
        text_range = self.font.render("Range: " + infopanel.get_range(self), True, settings.blue)
        text_bearing = self.font.render("Bearing: " + infopanel.get_bearing(self), True, settings.blue)
        text_note = self.font.render("Note: " + infopanel.get_note(self), True,
                                     settings.blue)
        text_hz = self.font.render("Freq: " + str(infopanel.get_hz(self)) + " Hz",
                                     True,
                                     settings.blue)
        text_x = self.font.render("X: " + infopanel.get_x(self), True, settings.blue)
        text_y = self.font.render("Y: " + infopanel.get_y(self), True, settings.blue)
        self.panel_surface.fill((255, 255, 255))
        self.panel_surface.blit(text_flight, (10, 10))
        self.panel_surface.blit(text_x, (10, 30))
        self.panel_surface.blit(text_y, (10, 50))
        self.panel_surface.blit(text_bearing, (10, 70))
        self.panel_surface.blit(text_range, (10, 90))
        self.panel_surface.blit(text_note, (10, 110))
        self.panel_surface.blit(text_hz, (10, 130))
        self.pygame.display.flip()
