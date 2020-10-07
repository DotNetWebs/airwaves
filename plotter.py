import aircraft
import connect
import midi
import objects
import settings
import math
import pygame
import sys


class plotter:
    def __init__(self, screen, radar_surface, map, scale, infopanel, font, font_large):
        self.screen = screen
        self.radar_surface = radar_surface
        self.map = map
        self.scale = scale
        self.infopanel = infopanel
        self.live_aircraft = []
        self.active_sector = None
        self.midiout = midi.controller()
        self.font = font
        self.font_large = font_large

    def draw_scale(self, screen):
        for count, angle in enumerate(self.scale.major_angles()):
            radar = (self.map.home_x, self.map.home_y)
            radar_len = 750
            note_len = 300
            note_angle = (360 / len(self.scale.major_angles())) / 2
            x = radar[0] + math.cos(math.radians(angle - 90)) * radar_len
            note_x = radar[0] + math.cos(math.radians(angle - 90 + note_angle)) * note_len
            y = radar[1] + math.sin(math.radians(angle - 90)) * radar_len
            note_y = radar[1] + math.sin(math.radians(angle - 90 + note_angle)) * note_len
            note = self.scale.key[count]
            text_note = self.font_large.render(note + " " + str(int(angle)), True, settings.green, 22)
            text_note_plot = (note_x, note_y)
            screen.blit(text_note, text_note_plot)
            pygame.draw.line(screen, settings.green, radar, (x, y), 2)

    def draw_live_aircraft(self):
        live_aircraft = []
        try:
            # draw aircraft
            for adsb_aircraft in connect.get_aircraft():

                try:
                    flight = aircraft.aircraft(adsb_aircraft['flight'], adsb_aircraft['alt_baro'],
                                               adsb_aircraft['mag_heading'], adsb_aircraft['ias'], adsb_aircraft['lat'],
                                               adsb_aircraft['lon'], self.map)

                    live_aircraft.append(flight)

                except Exception as e:
                    line = sys.exc_info()[-1].tb_lineno
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    pass

        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass

        plotter.set_live_aircraft(self, live_aircraft)

        for flight in self.live_aircraft:
            plotter.plot_aircraft(self, flight)


    def set_live_aircraft(self, live_aircraft):
        prev_aircraft = set(self.live_aircraft)
        current_aircraft = set(live_aircraft)
        retained_aircraft = prev_aircraft & current_aircraft
        new_aircraft = current_aircraft - prev_aircraft
        old_aircraft = prev_aircraft - current_aircraft

        # remove old aircraft
        for aircraft in old_aircraft:

            for i, o in enumerate(self.live_aircraft):
                if o.registration == aircraft.registration:
                    del self.live_aircraft[i]
                    break

        # add new aircraft
        for aircraft in new_aircraft:
            self.live_aircraft.append(aircraft)

        # update retained aircraft
        for aircraft in retained_aircraft:

            for i, o in enumerate(self.live_aircraft):
                if o.registration == aircraft.registration:
                    o.baro_alt = aircraft.baro_alt
                    o.heading = aircraft.heading
                    o.IAS = aircraft.IAS
                    o.position = aircraft.position

        # update aircraft life
        for aircraft in self.live_aircraft:
            aircraft.update_life()

    # draw aircraft
    def plot_aircraft(self, aircraft):
        sector = self.check_boundaries(aircraft, self.scale)
        colour = sector.color

        if self.active_sector:
            if self.active_sector.aircraft:
                if self.active_sector.aircraft.registration == aircraft.registration:
                    self.active_sector.aircraft = aircraft
                    colour = settings.green

        plotted_xy = (aircraft.plotted_x(), aircraft.plotted_y())
        pygame.draw.circle(self.screen, (settings.white), (plotted_xy), 10)
        pygame.draw.circle(self.screen, (colour), (plotted_xy), 5)

        text_flight = self.font.render(aircraft.registration, True, colour)
        text_alt = self.font.render("Alt: " + str(aircraft.baro_alt), True, colour)
        text_heading = self.font.render("HDG: " + str(aircraft.heading), True, colour)
        text_ias = self.font.render("IAS: " + str(aircraft.IAS), True, colour)
        text_bearing = self.font.render("Bearing: " + str(aircraft.corrected_bearing()), True, colour)
        text_range = self.font.render("Range: " + str(aircraft.range()), True, colour)

        if settings.debug_mode:
            text_x = self.font.render("X: " + str(aircraft.plotted_x()), True, colour)
            text_y = self.font.render("Y: " + str(aircraft.plotted_y()), True, colour)
            text_life = self.font.render("Life: " + str(aircraft.life), True, colour)
            text_init_bearing_diff = self.font.render("Init B Diff: " + str(aircraft.inital_bearing_diff), True,
                                                      colour)
            text_bearing_diff = self.font.render("B Diff: " + str(aircraft.bearing_diff), True, colour)

        self.screen.blit(text_flight, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer))
        self.screen.blit(text_alt, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 2))
        self.screen.blit(text_heading, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 3))
        self.screen.blit(text_ias, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 4))
        self.screen.blit(text_bearing, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 5))
        self.screen.blit(text_range, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 6))

        if settings.debug_mode:
            self.screen.blit(text_life, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 8))
            self.screen.blit(text_x, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 9))
            self.screen.blit(text_y, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 10))
            self.screen.blit(text_init_bearing_diff, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 11))
            self.screen.blit(text_bearing_diff, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 12))

    def check_boundaries(self, aircraft, scale):

        sector = objects.aw_sector()
        sector.color = settings.red

        # check for note boundary
        for count, angle in enumerate(scale.major_angles()):

            try:
                if aircraft.inital_bearing_diff != 0:
                    if int(aircraft.corrected_bearing()) - 1 <= int(angle) <= int(aircraft.corrected_bearing()) + 1:
                        if aircraft.plotted_x() > 0 < 1000 and aircraft.plotted_y() > 0 < 1000:

                            note = self.set_note(count, scale, aircraft, sector)
                            sector.aircraft = aircraft
                            sector.color = settings.green
                            sector.note = note
                            self.update_panel(aircraft=aircraft, aw_note=note)
                            self.active_sector = sector
                            break
                else:
                    if aircraft.inital_bearing_diff == 0:
                        sector.color = settings.gray
                    else:
                        sector.color = settings.red

            except Exception as e:
                line = sys.exc_info()[-1].tb_lineno
                exc_type, exc_obj, exc_tb = sys.exc_info()
                pass
        return sector

    def set_note(self, count, scale, aircraft, sector):
        note = objects.aw_note()
        if aircraft.bearing_diff > 0:
            note.note_name = scale.key[count] + '2'
        else:
            note.note_name = scale.key[count - 1] + '2'
        note.note_number = note.note2number(note.note_name)
        sector.note = note
        self.midiout.send_note(note)
        return note

    def update_panel(self, aircraft=None, aw_note=None):

        if aircraft:
            self.infopanel.set_aircraft(aircraft)
            self.infopanel.set_x(str(aircraft.plotted_x()))
            self.infopanel.set_y(str(aircraft.plotted_y()))

        if aw_note:
            self.infopanel.set_note(aw_note)

        self.infopanel.update_display()
