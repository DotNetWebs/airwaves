from geopy.distance import great_circle
import helpers

class aircraft:
    def __init__(self, flight, baro_alt, heading, IAS, lat, long, map):
        self.registration = flight
        self.baro_alt = baro_alt
        self.heading = int(heading)
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