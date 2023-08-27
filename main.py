import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pop My Balloons")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("graphics/sky_background.jpg").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

balloon_surface = pygame.image.load("graphics/balloon1.png").convert_alpha()

player_surface = pygame.image.load("graphics/idle_1.png").convert_alpha()
player_rectange = player_surface.get_rect(midbottom=(300, 500))
player_x_pos = 300
player_speed = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    player_rectange.left += direction * player_speed
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 500))
    screen.blit(balloon_surface, (400, 200))
    screen.blit(player_surface, player_rectange)

    pygame.display.update()
    clock.tick(60)
