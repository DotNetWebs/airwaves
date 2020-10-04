import math
from geopy.distance import great_circle
import helpers
import pretty_midi

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

    def __repr__(self):
        return f'Scale: {self.key} Notes: {self.numberofnotes}'

class aw_sector:
    def __init__(self):
        self.colour = None
        self.note = None
        self.aircraft = None

class aw_note:
    def __init__(self):
        self.note_number = 0
        self.note_name = ""

    def note2number(self, note_name):
        note_number = pretty_midi.note_name_to_number(note_name)
        return note_number

    def get_hz(self):
        return round(pretty_midi.note_number_to_hz(self.note_number),2)


