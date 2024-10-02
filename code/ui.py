import pygame

from settings import *

class UI:
    def __init__(self, monster, player_monsters):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT / 2 + 50
        self.monster = monster
        self.player_monsters = player_monsters

        # controls
        self.general_options = ['attack', 'heal', 'switch', 'escape']
        self.general_index = {'col': 0, 'row': 0}
        self.attack_index = {'col': 0, 'row': 0}
        self.state = 'general'
        self.rows, self.cols = 2, 2
        self.visible_monsters = 4


    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == 'general':
            self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_DOWN]) - int(
                keys[pygame.K_UP])) % self.rows
            self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_RIGHT]) - int(
                keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                self.state = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]

        elif self.state == 'attack':
            self.attack_index['row'] = (self.attack_index['row'] + int(keys[pygame.K_DOWN]) - int(
                keys[pygame.K_UP])) % self.rows
            self.attack_index['col'] = (self.attack_index['col'] + int(keys[pygame.K_RIGHT]) - int(
                keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                print(self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2])


    def select_menu(self, index, options):
        # background
        rect = pygame.FRect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)

        # menu
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']

                text_surf = self.font.render(options[i], True, color)
                text_rect = text_surf.get_frect(center=(x, y))
                self.display_surface.blit(text_surf, text_rect)


    def switch(self):
        # background
        rect = pygame.FRect(self.left + 40, self.top - 140, 400, 400)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'], rect, 4, 4)

        # menu
        for i in range(len(self.player_monsters)):
            x =rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i

            name = self.player_monsters[i].name
            text_surf = self.font.render(name, True, 'black')
            text_rect = text_surf.get_frect(center = (x,y))
            self.display_surface.blit(text_surf, text_rect)


    def update(self):
        self.input()


    def draw(self):
        match self.state:
            case 'general':
                self.select_menu(self.general_index, self.general_options)
            case 'attack':
                self.select_menu(self.attack_index, self.monster.abilities)
            case 'switch':
                self.switch()