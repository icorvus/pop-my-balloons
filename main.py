import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pop My Balloons")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("graphics/sky_background.jpg").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

player_surface = pygame.image.load("graphics/idle_1.png").convert_alpha()
player_x_pos = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 500))
    screen.blit(player_surface, (player_x_pos, 440))

    pygame.display.update()
    clock.tick(60)