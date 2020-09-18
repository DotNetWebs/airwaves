import midi
import objects
import settings
import pygame
import sys


class plotter:
    def __init__(self, infopanel):
        self.infopanel = infopanel
        self.active_aircraft = None
        self.active_note = None
        self.midiout = midi.controller()

    def plot_aircraft(self, scale, aircraft, screen, font):
        bearing_colour = settings.red

        # check for note boundary
        for count, angle in enumerate(scale.major_angles()):

            try:
                if int(aircraft.corrected_bearing()) - 1 <= int(angle) <= int(aircraft.corrected_bearing()) + 1:
                    if aircraft.plotted_x() > 0 < 1000 and aircraft.plotted_y() > 0 < 1000:
                        bearing_colour = settings.green
                        note = self.set_note(count, scale)
                        self.update_panel(aircraft=aircraft,aw_note=note)
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
                bearing_colour = settings.green

        plotted_xy = (aircraft.plotted_x(), aircraft.plotted_y())
        pygame.draw.circle(screen, (settings.white), (plotted_xy), 10)
        pygame.draw.circle(screen, (bearing_colour), (plotted_xy), 5)

        text_flight = font.render(aircraft.registration, True, bearing_colour)
        text_alt = font.render("Alt: " + str(aircraft.baro_alt), True, bearing_colour)
        text_heading = font.render("HDG: " + str(aircraft.heading), True, bearing_colour)
        text_ias = font.render("IAS: " + str(aircraft.IAS), True, bearing_colour)
        text_bearing = font.render("Bearing: " + str(aircraft.corrected_bearing()), True, bearing_colour)
        text_range = font.render("Range: " + str(aircraft.range(settings.home_pos)), True, bearing_colour)

        if settings.debug_mode:
            text_x = font.render("X: " + str(aircraft.plotted_x()), True, bearing_colour)
            text_y = font.render("Y: " + str(aircraft.plotted_y()), True, bearing_colour)

        screen.blit(text_flight, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer))
        screen.blit(text_alt, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 2))
        screen.blit(text_heading, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 3))
        screen.blit(text_ias, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 4))
        screen.blit(text_bearing, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 5))
        screen.blit(text_range, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 6))

        if settings.debug_mode:
            screen.blit(text_x, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 7))
            screen.blit(text_y, (plotted_xy[0] + 10, plotted_xy[1] + settings.text_spacer * 8))

    def set_note(self, count, scale):
        note = objects.aw_note()
        note.note_name = scale.key[count] + '2'
        note.note_number = note.note2number(note.note_name)
        self.active_note = note
        self.midiout.send_note(note)
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
