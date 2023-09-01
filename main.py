import sys
from enum import Enum

import pygame


class PlayerDirection(Enum):
    LEFT = -1
    STATIONARY = 0
    RIGHT = 1


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("graphics/idle_1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(300, 500))
        self.speed = 3
        self.direction = PlayerDirection.LEFT

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        self.direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        print(self.direction)
        self.rect.x += self.direction * self.speed


def main() -> None:
    WINDOW_SIZE = (800, 600)

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Pop My Balloons")
    icon_surface = pygame.image.load("graphics/icon.png").convert_alpha()
    pygame.display.set_icon(icon_surface)
    game_loop(screen)


def game_loop(screen: pygame.surface.Surface) -> None:
    """Main game loop

    Args:
        screen: Surface to draw the game on
    """
    clock = pygame.time.Clock()

    # Load surfaces
    sky_surface = pygame.image.load("graphics/sky_background.jpg").convert()
    ground_surface = pygame.image.load("graphics/ground.png").convert()
    balloon_surface = pygame.image.load("graphics/balloon1.png").convert_alpha()

    # Initialize Player sprite
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        screen.blit(balloon_surface, (400, 200))
        player_group.sprite.move()
        player_group.draw(screen)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
