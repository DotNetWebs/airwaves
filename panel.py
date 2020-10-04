import settings
import objects
import sys
import pygame

class infopanel:
    def __init__(self, pygame, font, panel_surface, screen):
        self.aircraft = None
        self.pygame = pygame
        self.font = font
        self.panel_surface = panel_surface
        self.screen = screen
        self.note = objects.aw_note()
        self.x = ""
        self.y = ""
        self.rect = pygame.Rect(settings.width, 0, settings.panel_width, settings.height)

    def set_aircraft(self, aircraft):
         self.aircraft = aircraft

    def get_aircraft(self):
        return self.aircraft

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

            aircraft= self.get_aircraft()

            if aircraft:
                text_flight = self.font.render(aircraft.registration, True, settings.green)
                text_alt = self.font.render("Alt: " + str(aircraft.baro_alt), True, settings.green)
                text_heading = self.font.render("HDG: " + str(aircraft.heading), True, settings.green)
                text_ias = self.font.render("IAS: " + str(aircraft.IAS), True, settings.green)
                text_range = self.font.render("Range: " + str(aircraft.range()), True, settings.green)
                text_bearing = self.font.render("Bearing: " + str(aircraft.bearing), True, settings.green)
                text_note = self.font.render("Note: " + infopanel.get_note(self).note_name, True,
                                             settings.green)
                text_hz = self.font.render("Freq: " + str(infopanel.get_note(self).get_hz()) + " Hz",
                                           True,
                                           settings.green)

                if settings.debug_mode:
                    text_x = self.font.render("X: " + infopanel.get_x(self), True, settings.green)
                    text_y = self.font.render("Y: " + infopanel.get_y(self), True, settings.green)
                    text_life = self.font.render("Life: " + str(aircraft.life), True, settings.green)
                    text_init_bearing_diff = self.font.render("Init B Diff: " + str(aircraft.inital_bearing_diff), True, settings.green)
                    text_bearing_diff = self.font.render("B Diff: " + str(aircraft.bearing_diff), True, settings.green)

                self.panel_surface.fill((0, 0, 0))
                self.panel_surface.blit(text_flight, (10, 10))
                self.panel_surface.blit(text_alt, (10, settings.text_spacer * 2))
                self.panel_surface.blit(text_heading, (10, settings.text_spacer * 3))
                self.panel_surface.blit(text_ias, (10, settings.text_spacer * 4))
                self.panel_surface.blit(text_bearing, (10, settings.text_spacer * 5))
                self.panel_surface.blit(text_range, (10, settings.text_spacer * 6))

                self.panel_surface.blit(text_note, (10, settings.text_spacer * 8))
                self.panel_surface.blit(text_hz, (10, settings.text_spacer * 9))

                if settings.debug_mode:
                    self.panel_surface.blit(text_life, (10, settings.text_spacer * 11))
                    self.panel_surface.blit(text_x, (10, settings.text_spacer * 12))
                    self.panel_surface.blit(text_y, (10, settings.text_spacer * 13))
                    self.panel_surface.blit(text_init_bearing_diff, (10, settings.text_spacer * 14))
                    self.panel_surface.blit(text_bearing_diff, (10, settings.text_spacer * 15))

                self.screen.blit(self.panel_surface, (1000, 0))
                self.pygame.display.update(self.rect)

            else:
                self.panel_surface.fill((0, 0, 0))
                self.screen.blit(self.panel_surface, (1000, 0))
                self.pygame.display.update(self.rect)


        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass

    def init_display(self):
        try:
            self.panel_surface.fill((255, 255, 255))
            self.screen.blit(self.panel_surface, (1000, 0))
            self.pygame.display.update(self.rect)
        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass


