from settings import *
from support import *
from monster import *
from ui import *
from timer import Timer
from random import choice
from attack import AttackAnimationSprite


class Game:
    def __init__(self):
        # game setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Monster Battle')
        self.clock = pygame.time.Clock()
        self.running = True

        # images and audio
        self.import_assets()
        self.audio['music'].play(loops=-1)

        # groups 
        self.all_sprites = pygame.sprite.Group()

        # data
        self.player_active = True
        player_monster_list = ['Sparchu', 'Cleaf', 'Jacana', 'Finsta', 'Plumette', 'Gulfin']
        self.player_monsters = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monsters[0]
        self.all_sprites.add(self.monster)
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(opponent_name, self.front_surfs[opponent_name], self.all_sprites)

        # ui
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input)
        self.opp_ui = OpponentUI(self.opponent)

        # timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn),
                       'opponent end': Timer(1000, func = self.player_turn)}


    def get_input(self, state, data = None):
        """Calls on logic for each of menu buttons: attack, heal, switch, and escape.
        Activates timer for player."""

        if state == 'attack':
            self.apply_attack(self.opponent, data)
        elif state == 'heal':
            self.monster.health += 50
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
            self.audio['green'].play()
        elif state == ' switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster
        elif state == 'escape':
            self.running = False
        self.player_active = False
        self.timers['player end'].activate()


    def apply_attack(self, target, attack):
        """Creates attack damage based on attack and monster elements.
        Applies damage to target health. And starts attack animation & audio."""

        attack_data = ABILITIES_DATA[attack]
        damage_mult = ELEMENT_DATA[attack_data['element']][target.element]
        target.health -= attack_data['damage'] * damage_mult
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
        self.audio[attack_data['animation']].play()


    def opponent_turn(self):
        """Checks is opponent has died - > chooses another monster for the opponent.
        If opponent is alive, opponent applies random attack. And timer for opponent."""

        if self.opponent.health <= 0:
            self.player_active = True
            self.opponent.kill()
            monster_name = choice(list(MONSTER_DATA.keys()))
            self.opponent = Opponent(monster_name, self.front_surfs[monster_name], self.all_sprites)
            self.opp_ui.monster = self.opponent
        else:
            attack = choice(self.opponent.abilities)
            self.apply_attack(self.monster, attack)
            self.timers['opponent end'].activate()


    def player_turn(self):
        """Checks if player monster is alive.
        If monster dies, new monster appears from available player list.
        If list is empty, game stops."""

        self.player_active = True
        if self.monster.health <= 0:
            avail_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if avail_monsters:
                self.monster.kill()
                self.monster = avail_monsters[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
        else:
            self.running = False


    def update_timers(self):
        """Updates timers."""

        for timer in self.timers.values():
            timer.update()


    def import_assets(self):
        """Imports assets like images and audio from the custom path."""

        self.back_surfs = folder_importer('..', 'images', 'back')
        self.bg_surfs = folder_importer('..', 'images', 'other')
        self.front_surfs = folder_importer('..', 'images', 'front')
        self.simple_surfs = folder_importer('..', 'images', 'simple')
        self.attack_frames = tile_importer(4, '..', 'images', 'attacks')
        self.audio = audio_importer('..', 'audio')


    def draw_floor(self):
        """Draws floor image below the player and opponent monsters on screen."""

        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                self.screen.blit(self.bg_surfs['floor'], floor_rect)


    def run(self):
        """Runs game man loop."""

        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # update
            self.update_timers()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()

            # draw
            self.screen.blit(self.bg_surfs['bg'], (0, 0))
            self.draw_floor()
            self.all_sprites.draw(self.screen)
            self.ui.draw()
            self.opp_ui.draw()
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()