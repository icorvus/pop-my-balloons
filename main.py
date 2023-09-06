from __future__ import annotations

from enum import IntEnum
from pathlib import Path
import random
from typing import Self
import sys

import pygame

# Global constants
SCREENRECT = pygame.Rect(0, 0, 800, 600)
FRAMERATE = 60


class Direction(IntEnum):
    LEFT = -1
    STATIONARY = 0
    RIGHT = 1


class MetaPMBSprite(type):
    """Metaclass for Pop My Balloons base sprite class.

    It's used to create group attribute for all subclasses.
    """

    def __new__(mcs, name, bases, attrs) -> MetaPMBSprite:
        """Creates group attribute for subclasses."""
        cls = super().__new__(mcs, name, bases, attrs)
        cls.group = pygame.sprite.Group()
        return cls


class PMBSprite(pygame.sprite.Sprite, metaclass=MetaPMBSprite):
    """Pop My Balloons base sprite class."""

    @classmethod
    def create(cls, *args, **kwargs) -> Self:
        """Creates instance of the class and adds it to a group."""
        instance = cls(*args, **kwargs)
        cls.group.add(instance)
        return instance


class Player(pygame.sprite.Sprite):
    group = pygame.sprite.GroupSingle()

    def __init__(self, spawn_pos: tuple[int, int] = (300, 500), speed: int = 3) -> None:
        super().__init__()
        self.frames = tuple(
            pygame.image.load(file).convert_alpha()
            for file in Path("assets/sprites/player/idle").iterdir()
        )
        self.running_frames = tuple(
            pygame.image.load(file).convert_alpha()
            for file in Path("assets/sprites/player/run").iterdir()
        )
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(midbottom=spawn_pos)
        self.speed = speed
        self.direction = Direction.STATIONARY

    def _animate(self) -> None:
        self.current_frame_index += self.animation_speed
        if self.direction != Direction.STATIONARY:
            self.current_frame_index %= len(self.running_frames)
            self.image = self.running_frames[int(self.current_frame_index)]
            if self.direction == Direction.LEFT:
                # Flips player surface horizontally.
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.current_frame_index %= len(self.frames)
            self.image = self.frames[int(self.current_frame_index)]

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        self.direction = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.rect.x += self.direction * self.speed
        self.rect.clamp_ip(SCREENRECT)
        self._animate()


class Balloon(PMBSprite):
    SPAWN_EVENT = pygame.USEREVENT + 1

    def __init__(self, speed: int = 4) -> None:
        super().__init__()
        self.frames = (
            pygame.image.load("assets/sprites/balloon/balloon_0.png").convert_alpha(),
            pygame.image.load("assets/sprites/balloon/balloon_1.png").convert_alpha(),
            pygame.image.load("assets/sprites/balloon/balloon_2.png").convert_alpha(),
        )
        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(topleft=(random.randint(800, 1000), 10))
        self.active = False  # Have sprite appeared on the screen fully?
        self.speed = speed
        self.direction = Direction.LEFT
        self.width = self.rect.width

    def _go_level_down(self) -> None:
        self.direction *= -1  # Reverse move direction
        self.rect.y += self.rect.height

    def _animate(self) -> None:
        self.current_frame_index += 0.1
        self.current_frame_index %= len(self.frames)
        self.image = self.frames[int(self.current_frame_index)]

    def update(self) -> None:
        self._animate()
        self.rect.x += self.direction * self.speed
        if not self.active and SCREENRECT.contains(self.rect):
            self.active = True
        if self.active and self.rect.centerx not in range(15, 785):
            self._go_level_down()

    def kill(self) -> None:
        # TODO: Spawn water splash animation
        super().kill()


class Arrow(PMBSprite):
    MAX_ARROWS_ON_SCREEN = 3

    def __init__(self, spawn_coordinates: tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.image.load("assets/sprites/arrow/arrow.png").convert_alpha()
        self.rect = self.image.get_rect(center=spawn_coordinates)
        self.speed = 5

    def _is_off_screen(self) -> bool:
        return not SCREENRECT.contains(self)

    @classmethod
    def create(cls, spawn_coordinates: tuple[int, int]) -> Arrow | None:
        """Create an Arrow sprite and add it to the group, if within the limit.

        The limit of max arrows on screen is defined as Arrow class variable.

        Args:
            spawn_coordinates (tuple[int, int]): (x, y) coordinates where to spawn

        Returns:
            Arrow | None: created Arrow object or None if not within the limit.
        """
        if len(cls.group.sprites()) < cls.MAX_ARROWS_ON_SCREEN:
            return super().create(spawn_coordinates)

    def update(self) -> None:
        self.rect.y -= self.speed
        if self._is_off_screen():
            self.kill()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size)
    pygame.display.set_caption("Pop My Balloons")
    icon_surface = pygame.image.load("assets/icons/icon.png").convert_alpha()
    pygame.display.set_icon(icon_surface)

    game_loop(screen)


def game_loop(screen: pygame.surface.Surface) -> None:
    """Main game loop

    Args:
        screen: Surface to draw the game on
    """
    clock = pygame.time.Clock()

    # Load surfaces
    sky_surface = pygame.image.load("assets/sprites/background/sky.jpg").convert()
    ground_surface = pygame.image.load("assets/sprites/background/ground.png").convert()

    # Initialize Player sprite
    player_group = pygame.sprite.GroupSingle()
    player_group.add(Player())

    pygame.time.set_timer(
        Balloon.SPAWN_EVENT, 900 - int(pygame.time.get_ticks() / 1000)
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == Balloon.SPAWN_EVENT:
                pygame.time.set_timer(  # Spawn balloons faster as the game progresses
                    Balloon.SPAWN_EVENT, 900 - int(pygame.time.get_ticks() / 100)
                )
                Balloon.create()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Arrow.create(spawn_coordinates=player_group.sprite.rect.midtop)

        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 500))
        player_group.update()
        player_group.draw(screen)
        Balloon.group.update()
        Balloon.group.draw(screen)
        Arrow.group.draw(screen)
        Arrow.group.update()
        if pygame.sprite.spritecollide(player_group.sprite, Balloon.group, True):
            sys.exit()
        if pygame.sprite.groupcollide(Arrow.group, Balloon.group, True, True):
            pass

        pygame.display.update()
        clock.tick(FRAMERATE)


if __name__ == "__main__":
    main()
