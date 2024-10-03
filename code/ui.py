import pygame
from support import folder_importer

from settings import *

class UI:
    def __init__(self, monster, player_monsters, simple_surfs, get_input):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = WINDOW_WIDTH / 2 - 100
        self.top = WINDOW_HEIGHT / 2 + 50
        self.monster = monster
        self.pl_mon = player_monsters
        self.simple_surfs = simple_surfs
        self.get_input = get_input

        # controls
        self.options = ['attack', 'heal', 'switch', 'escape']
        self.gen_idx = {'col': 0, 'row': 0}
        self.attack_idx = {'col': 0, 'row': 0}
        self.sw_idx = 0
        self.state = 'general'
        self.rows, self.cols = 2, 2
        self.vis_mon = 4
        self.avail_mon = [monster for monster in self.pl_mon
                          if monster != self.monster and monster.health > 0]


    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == 'general':
            self.gen_idx['row'] = (self.gen_idx['row'] + int(keys[pygame.K_DOWN]) - int(
                keys[pygame.K_UP])) % self.rows
            self.gen_idx['col'] = (self.gen_idx['col'] + int(keys[pygame.K_RIGHT]) - int(
                keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                self.state = self.options[self.gen_idx['col'] + self.gen_idx['row'] * 2]

        elif self.state == 'attack':
            self.attack_idx['row'] = (self.attack_idx['row'] + int(keys[pygame.K_DOWN]) - int(
                keys[pygame.K_UP])) % self.rows
            self.attack_idx['col'] = (self.attack_idx['col'] + int(keys[pygame.K_RIGHT]) - int(
                keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE]:
                attack = self.monster.abilities[self.attack_idx['col'] + self.attack_idx['row'] * 2]
                self.get_input(self.state, attack)
                self.state = 'general'

        elif self.state == 'switch':
            if self.avail_mon:
                self.sw_idx = ((self.sw_idx + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]))
                               % len(self.avail_mon))
            if keys[pygame.K_SPACE]:
                self.get_input(self.state, self.avail_mon[self.sw_idx])
                self.state = 'general'

        elif self.state == 'heal':
            self.get_input('heal')
            self.state = 'general'

        elif self.state == 'escape':
            self.get_input('escape')

        if keys[pygame.K_ESCAPE]:
            self.state = 'general'
            self.gen_idx = {'col': 0, 'row': 0}
            self.attack_idx = {'col': 0, 'row': 0}
            self.sw_idx = 0


    def select_menu(self, index, options):
        # background
        rect = pygame.FRect(self.left + 40, self.top + 60, 400, 200)
        pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

        # menu
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                color = COLORS['gray'] if col == index['col'] and row == index['row'] else COLORS['black']

                text_surf = self.font.render(options[i], True, color)
                text_rect = text_surf.get_frect(center=(x, y))
                self.screen.blit(text_surf, text_rect)


    def switch(self):
        # background
        rect = pygame.FRect(self.left + 40, self.top - 100, 400, 400)
        pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

        # menu
        v_offset = 0 if self.sw_idx < self.vis_mon \
            else -(self.sw_idx - self.vis_mon + 1) * rect.height / self.vis_mon

        for i in range(len(self.avail_mon)):
            x =rect.centerx
            y = (rect.top + rect.height / (self.vis_mon * 2) + rect.height
                 / self.vis_mon * i + v_offset)

            color = COLORS['gray'] if i == self.sw_idx else COLORS['black']
            name = self.avail_mon[i].name

            m_img_surf = self.simple_surfs[name]
            m_img_rect = m_img_surf.get_frect(center = (x - 120, y))
            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_frect(center = (x,y))
            if rect.collidepoint(text_rect.center):
                self.screen.blit(text_surf, text_rect)
                self.screen.blit(m_img_surf, m_img_rect)


    def stats(self):
        # background
        rect = pygame.rect.FRect(self.left, self.top, 250, 80)
        pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

        # data
        name_surf = self.font.render(self.monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
        self.screen.blit(name_surf, name_rect)

        # health bar
        health_rect = pygame.rect.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        pygame.draw.rect(self.screen, COLORS['gray'], health_rect)
        self.draw_bar(health_rect, self.monster.health, self.monster.max_health)


    def draw_bar(self, rect, value, max_value):
        ration = rect.width / max_value
        progress_rect = pygame.rect.FRect(rect.topleft, (value * ration, rect.height))
        pygame.draw.rect(self.screen, COLORS['red'], progress_rect)


    def update(self):
        self.input()
        self.avail_mon = [monster for monster in self.pl_mon if monster != self.monster
                          and monster.health > 0]


    def draw(self):
        match self.state:
            case 'general':
                self.select_menu(self.gen_idx, self.options)
            case 'attack':
                self.select_menu(self.attack_idx, self.monster.abilities)
            case 'switch':
                self.switch()

        if self.state != 'switch':
            self.stats()


class OpponentUI:
    def __init__(self, monster):
        self.screen = pygame.display.get_surface()
        self.monster = monster
        self.font = pygame.font.Font(None, 30)


    def draw(self):
        # background
        rect = pygame.rect.FRect((0, 0), (250, 80)).move_to(midleft = (500, self.monster.rect.centery))
        pygame.draw.rect(self.screen, COLORS['white'], rect, 0, 4)
        pygame.draw.rect(self.screen, COLORS['gray'], rect, 4, 4)

        # name
        name_surf = self.font.render(self.monster.name, True, COLORS['black'])
        name_rect = name_surf.get_frect(topleft=rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
        self.screen.blit(name_surf, name_rect)

        # health
        health_rect = pygame.rect.FRect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        ratio = health_rect.width / self.monster.max_health
        progress_bar = pygame.rect.FRect(health_rect.topleft, (self.monster.health * ratio, health_rect.height))
        pygame.draw.rect(self.screen, COLORS['gray'], health_rect)
        pygame.draw.rect(self.screen, COLORS['red'], progress_bar)
