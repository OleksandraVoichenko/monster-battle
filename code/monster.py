from settings import *
from random import sample


class Creature:
    def __init__(self):
        self.rect = None
        self._health = None


    def get_data(self, name):
        """Gets element of monster, monster health, available monster attacks, and monster name."""

        self.element = MONSTER_DATA[name]['element']
        self._health = self.max_health = MONSTER_DATA[name]['health']
        self.abilities = sample(list(ABILITIES_DATA.keys()), 4)
        self.name = name


    @property
    def health(self):
        """Getter for the monster health."""

        return self._health


    @health.setter
    def health(self, value):
        """Setter for a monster health."""

        self._health = min(self.max_health, max(0, value))


class Monster(pygame.sprite.Sprite, Creature):
    def __init__(self, name, surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(bottomleft=(100, WINDOW_HEIGHT))
        self.name = name
        self.get_data(name)


    def __repr__(self):
        """Returns monster name and health/max_health value"""
        return f'{self.name}, {self.health/self.max_health}'


class Opponent(pygame.sprite.Sprite, Creature):
    def __init__(self, name, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=(WINDOW_WIDTH - 250, 350))
        self.get_data(name)