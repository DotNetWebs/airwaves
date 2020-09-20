from geopy.distance import great_circle
import helpers
import settings

class aircraft:
    def __init__(self, flight, baro_alt, heading, IAS, lat, long, map):
        self.registration = flight
        self.baro_alt = baro_alt
        self.heading = int(heading)
        self.IAS = IAS
        self.position = (lat, long)
        self.map = map
        self.life = 0
        self.bearing = 0
        self.last_bearing = None
        self.bearing_diff = 0

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

            bearing = int(self.cartesian()[1]) + 90
            self.bearing = bearing

            if self.last_bearing:
                self.bearing_diff = bearing - self.last_bearing

            self.last_bearing = bearing
            return bearing
        else:
            bearing = int(self.cartesian()[1]) + 90 + 180
            self.bearing = bearing

            if self.last_bearing:
                self.bearing_diff = bearing - self.last_bearing

            self.last_bearing = bearing
            return bearing

    def range(self):
        return round(great_circle(settings.home_pos, self.position).nautical, 2)

    def blit_XY(self):
        return ()

    def update_life(self):
        self.life += 1

    def __eq__(self, other):
        if not isinstance(other, aircraft):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.registration == other.registration

    def __hash__(self):
        # required to enable hashing for dictionaries and sets.
        return hash((self.registration))

    def __repr__(self):
        return self.registration