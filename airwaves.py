#!/usr/bin/env python3
import mingus.core.keys as keys
import sys
import pygame

import objects
import panel
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
radar_rect = pygame.Rect((0,0) + radar)
radar_surface = pygame.Surface(radar)

dimensions = (width, height) = (settings.panel_width, settings.height)
panel_surface = pygame.Surface(dimensions)

infopanel = panel.infopanel(pygame, font, panel_surface, screen)
infopanel.init_display()
key = keys.get_notes(key=settings.initial_key)
scale = objects.scale(key)
plotter = plotter.plotter(screen, radar_surface, map, scale, infopanel, font, font_large)

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
    plotter.draw_scale(radar_surface)
    screen.blit(radar_surface, (0, 0))

    plotter.draw_aircraft()

    if plotter.active_aircraft:
        plotter.update_panel(aircraft=plotter.active_aircraft)

    # refresh radar
    pygame.display.update(radar_rect)

    # refresh info panel display
    infopanel.update_display()


pygame.quit()
