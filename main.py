import sys
from enum import IntEnum

import pygame

# Global constants
SCREENRECT = pygame.Rect(0, 0, 800, 600)

class Direction(IntEnum):
    LEFT = -1
    STATIONARY = 0
    RIGHT = 1


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("graphics/idle_1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(300, 500))
        self.speed = 3
        self.direction = Direction.LEFT

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        self.direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.rect.x += self.direction * self.speed
        self.rect.clamp_ip(SCREENRECT)

class Balloon(pygame.sprite.Sprite):
    def __init__(self, speed: int = 3) -> None:
        super().__init__()
        self.image = pygame.image.load("graphics/balloon1.png").convert_alpha()
        self.rect = self.image.get_rect(topright=(790, 10))
        self.speed = speed
        self.direction = Direction.LEFT
        self.width = self.rect.width

    def go_level_down(self) -> None:
        self.direction *= -1  # Reverse move direction
        self.rect.y += self.rect.height

    def update(self) -> None:
        self.rect.x += self.direction * self.speed
        if self.rect.centerx not in range(35, 765):
            self.go_level_down()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
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

    # Initialize Player sprite
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player())

    # Initialize dummy balloon
    balloons = pygame.sprite.Group()
    balloons.add(Balloon())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        player_group.sprite.move()
        player_group.draw(screen)
        balloons.update()
        balloons.draw(screen)
        if pygame.sprite.spritecollide(player_group.sprite, balloons, True):
            sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
