#!/usr/bin/env python3
import mingus.core.keys as keys
import sys
import pygame
import aircraft
import connect
import helpers
import objects
import plotter
import settings

# init pygame
pygame.init()
running = True

# init map
map = objects.map(settings.home_pos[0], settings.home_pos[1], settings.offset, settings.height, settings.width)

# intit screen
font = pygame.font.SysFont(settings.main_font[0], settings.main_font[1])
font_large = pygame.font.SysFont(settings.large_font[0], settings.large_font[1])
bg = pygame.image.load(settings.bg_image)
screen = pygame.display.set_mode([settings.width + settings.panel_width, settings.height])
pygame.display.set_caption('Airwaves')

radar = (width, height) = (settings.width, settings.height)
radar_surface = pygame.Surface(radar)

panel = (width, height) = (settings.panel_width, settings.height)
panel_surface = pygame.Surface(panel)

infopanel = objects.infopanel(pygame, font, panel_surface, screen)
infopanel.init_display()
plotter = plotter.plotter(infopanel)

# main loop
while running:

    # loop unless quit detected
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw background
    radar_surface.blit(bg, settings.home_xy)
    pygame.draw.circle(radar_surface, (settings.green), (map.home_x, map.home_y), settings.home_radius)

    # draw scale
    key = keys.get_notes(key=settings.initial_key)
    scale = objects.scale(key)
    helpers.draw_scale(scale, key, radar_surface, map, settings.green, font_large)

    live_aircraft = []

    try:
        # draw aircraft
        for adsb_aircraft in connect.get_aircraft():

            try:
                flight = aircraft.aircraft(adsb_aircraft['flight'], adsb_aircraft['alt_baro'],
                                           adsb_aircraft['mag_heading'], adsb_aircraft['ias'], adsb_aircraft['lat'],
                                           adsb_aircraft['lon'], map)
                plotter.plot_aircraft(scale, flight, radar_surface, font)

                live_aircraft.append(flight)

            except Exception as e:
                line = sys.exc_info()[-1].tb_lineno
                exc_type, exc_obj, exc_tb = sys.exc_info()
                pass

        plotter.set_live_aircraft(live_aircraft)

    except Exception as e:
        line = sys.exc_info()[-1].tb_lineno
        exc_type, exc_obj, exc_tb = sys.exc_info()
        pass

    screen.blit(radar_surface, (0, 0))

    if plotter.active_aircraft:
        plotter.update_panel(aircraft=plotter.active_aircraft)

    infopanel.update_display()
    pygame.display.flip()

pygame.quit()
