import os
import pygame
import time
from interface import *
from cheat_code import *
from map import *
from random import choice


CONDITIONS = {'main title': 0, 'main menu': 1,
              'settings': 2, 'hub': 3, 'library': 4, 'characters': 5, 'upgrades': 6, 'choose map': 7, 'game': 8, 'game over': 9}  # condition of game
MAPS = {'underground': 0, 'incineration plant': 1}
CHARACTERS = {'cleaner': 0, 'guard': 1}
CAESAR_SHIFT = 10


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('project gamma')
        self.create_default_settings_file()
        if 'settings.txt' not in os.listdir('data'):
            self.read_settings('data/default settings.txt')
            self.create_settings_file()
        self.read_settings('data/settings.txt')
        self.clock = pygame.time.Clock()
        self.resolution = (1920, 1080)
        self.display = pygame.display.set_mode(self.resolution)
        self.current_condition = CONDITIONS['main title']
        self.current_map = MAPS['underground']
        self.current_character = CHARACTERS['cleaner']
        self.save = 'data/save.txt' if 'save.txt' in os.listdir(
            'data') else None

        self.main_title = Background('images/menu/main title.png')
        self.main_menu = Background('images/menu/main menu.png')
        self.hub_menu = Background('images/menu/hub menu.png')
        self.choose_map_menu = Background('images/menu/choose map menu.png')
        self.game_over_menu = Background('images/menu/game over.png')
        # objects

        self.main_buttons = {}
        self.main_buttons['continue'] = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Продолжить')
        self.main_buttons['new game'] = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Новая игра')
        self.main_buttons['settings'] = Button(
            x=(self.resolution[0] - 800) // 2, y=400, text='Настройки')
        self.main_buttons['exit'] = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Выход')

        self.settings_buttons = {}
        self.settings_buttons['back'] = Button(
            x=(self.resolution[0] - 800) // 2, y=800, text='Назад')
        self.settings_buttons['volume'] = Slider(
            x=(self.resolution[0] - 800) // 2, y=200, text='Громкость', value=self.volume)
        self.settings_buttons['fps'] = Slider(
            x=(self.resolution[0] - 800) // 2, y=300, text='FPS', value=self.fps, max_value=120)
        self.settings_buttons['reset'] = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Сбросить')

        self.hub_buttons = {}
        self.hub_buttons['start'] = Button(
            x=(self.resolution[0] - 800) // 2, y=100, text='Начать')
        self.hub_buttons['characters'] = Button(
            x=150, y=400, text='Персонажи')
        self.hub_buttons['upgrades'] = Button(
            x=970, y=400, text='Улучшения')
        self.hub_buttons['library'] = Button(
            x=(self.resolution[0] - 800) // 2, y=700, text='Библиотека')
        self.hub_buttons['exit button'] = Button(
            x=(self.resolution[0] - 150) // 2, y=900, text='', path='images/menu/exit button.png')

        self.choose_map_menu_buttons = {}
        self.choose_map_menu_buttons['return button'] = Button(
            x=(self.resolution[0] - 150) // 2 + 550, y=920, text='', path='images/menu/return button.png')
        self.choose_map_menu_buttons['left arrow'] = Button(
            x=(self.resolution[0] - 150) // 2 - 500, y=150, weight=256, height=256, text='', path='images/menu/left arrow.png')
        self.choose_map_menu_buttons['right arrow'] = Button(
            x=(self.resolution[0] - 150) // 2 + 400, y=150, weight=256, height=256, text='', path='images/menu/right arrow.png')
        self.choose_map_menu_buttons['start'] = Button(
            x=(self.resolution[0] - 800) // 2, y=500, text='Начать')
        self.choose_map_menu_buttons['buy'] = Button(
            x=(self.resolution[0] - 800) // 2, y=500, text='Купить за 500 чипов', font_size=50)
        self.choose_map_menu_buttons['underground'] = UserInterface(
            x=(self.resolution[0] - 600) // 2, y=58, path='images/menu/underground.png')
        self.choose_map_menu_buttons['incineration plant'] = UserInterface(
            x=(self.resolution[0] - 600) // 2, y=58, path='images/menu/incineration plant.png')
        self.choose_map_menu_buttons['chips'] = ImageWithCounter(
            x=(self.resolution[0] - 96) // 2 + 500, y=40, path='images/menu/chip.png')
        self.descriptions_of_maps = ['Подземная парковка', 'Мусоросжигатель']
        self.map_description = Title(
            x=500, y=700, text=self.descriptions_of_maps[self.current_map], font_size=70)
        
        self.main_buttons = {}
        self.main_buttons['continue'] = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Продолжить')
        self.main_buttons['new game'] = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Новая игра')
        self.main_buttons['settings'] = Button(
            x=(self.resolution[0] - 800) // 2, y=400, text='Настройки')
        self.main_buttons['exit'] = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Выход')
        
        self.game_over_buttons = {}
        self.game_over_buttons['continue'] = Button(
            x=(self.resolution[0] - 800) // 2, y=800, text='Продолжить')

    def main_loop(self):
        while True:
            self.clock.tick(self.fps)
            self.load_interface()
            self.check_events()
            # autosave
            if self.current_condition not in [CONDITIONS['main title'], CONDITIONS['main menu'], CONDITIONS['settings']]:
                self.player_profile.create_save_file('data/save.txt')
            pygame.display.update()

    def load_interface(self):
        if self.current_condition == CONDITIONS['main title']:
            self.main_title.render(self)
        elif self.current_condition == CONDITIONS['main menu']:
            self.main_menu.render(self)
            # check up save
            for i in self.main_buttons:
                if i == 'continue':
                    if self.save != None:
                        self.main_buttons[i].render(self)
                elif i == 'new game':
                    if self.save == None:
                        self.main_buttons[i].render(self)
                else:
                    self.main_buttons[i].render(self)
        elif self.current_condition == CONDITIONS['settings']:
            self.main_menu.render(self)
            for i in self.settings_buttons:
                self.settings_buttons[i].render(self)
        elif self.current_condition == CONDITIONS['hub']:
            self.hub_menu.render(self)
            for i in self.hub_buttons:
                self.hub_buttons[i].render(self)
        elif self.current_condition == CONDITIONS['choose map']:
            self.choose_map_menu.render(self)
            for i in self.choose_map_menu_buttons:
                if i == 'start':
                    if self.current_map in self.player_profile.maps:
                        self.choose_map_menu_buttons[i].render(self)
                elif i == 'buy':
                    if self.current_map not in self.player_profile.maps:
                        self.choose_map_menu_buttons[i].render(self)
                elif i in MAPS:
                    if MAPS[i] == self.current_map:
                        self.choose_map_menu_buttons[i].render(self)
                    self.indicators_of_difficulty = []
                    for j in range(len(MAPS)):
                        if self.current_map >= j:
                            self.indicators_of_difficulty.append(
                                UserInterface(path='images/menu/black circle.png', x=1000 + j * 75, y=880))
                        else:
                            self.indicators_of_difficulty.append(
                                UserInterface(path='images/menu/white circle.png', x=1000 + j * 75, y=880))
                    for j in self.indicators_of_difficulty:
                        j.render(self)
                elif i == 'chips':
                    self.choose_map_menu_buttons[i].update_value(
                        str(self.player_profile.chips))
                    self.choose_map_menu_buttons[i].render(self)
                else:
                    self.choose_map_menu_buttons[i].render(self)
                self.map_description.text = self.descriptions_of_maps[self.current_map]
                self.map_description.render(self)
        elif self.current_condition == CONDITIONS['game over']:
            self.game_over_menu.render(self)
            self.timer_bar = TimerBar(
                "images/character/clock.png", x=850, y=300)
            self.timer_bar.render(self, self.last_time)
            for i in self.game_over_buttons:
                self.game_over_buttons[i].render(self)

    def check_events(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            if i.type == pygame.MOUSEBUTTONDOWN:
                if self.current_condition == CONDITIONS['main menu']:
                    if self.main_buttons['exit'].check_click(i):
                        exit()
                    if self.main_buttons['settings'].check_click(i):
                        self.current_condition = CONDITIONS['settings']
                    if self.main_buttons['continue'].check_click(i) or self.main_buttons['new game'].check_click(i):
                        self.current_condition = CONDITIONS['hub']
                        self.player_profile = PLayerProfile(
                            'data/save.txt')

                elif self.current_condition == CONDITIONS['settings']:
                    if self.settings_buttons['back'].check_click(i):
                        self.fps = self.settings_buttons['fps'].get_value()
                        self.volume = self.settings_buttons['volume'].get_value(
                        )
                        self.create_settings_file()
                        self.current_condition = CONDITIONS['main menu']
                    if self.settings_buttons['reset'].check_click(i):
                        self.reset_settings()
                        self.settings_buttons['fps'].set_value(self.fps)
                        self.settings_buttons['volume'].set_value(
                            self.volume)
                    self.settings_buttons['volume'].set_value_by_mouse(i)
                    self.settings_buttons['fps'].set_value_by_mouse(i)

                elif self.current_condition == CONDITIONS['hub']:
                    if self.hub_buttons['exit button'].check_click(i):
                        exit()
                    if self.hub_buttons['start'].check_click(i):
                        self.current_condition = CONDITIONS['choose map']
                        self.current_map = MAPS['underground']

                elif self.current_condition == CONDITIONS['choose map']:
                    if self.choose_map_menu_buttons['return button'].check_click(i):
                        self.current_condition = CONDITIONS['hub']
                    if self.choose_map_menu_buttons['left arrow'].check_click(i):
                        self.current_map -= 1
                        if self.current_map < 0:
                            self.current_map = len(MAPS) - 1
                    if self.choose_map_menu_buttons['right arrow'].check_click(i):
                        self.current_map += 1
                        if self.current_map > len(MAPS) - 1:
                            self.current_map = 0
                    if self.choose_map_menu_buttons['start'].check_click(i):
                        if self.current_map not in self.player_profile.maps:
                            if self.player_profile.chips >= 500:
                                self.player_profile.chips -= 500
                                self.player_profile.maps.append(self.current_map)
                        else:
                            self.current_condition = CONDITIONS['game']
                            self.map = Map(self.current_map)
                            self.player_entity = Player(
                                0, 0, (f'images/character/{self.current_character}.png', ))
                            self.player_entity.add_weapon(Hook(self.player_entity))
                            self.enemy_spawner = EnemySpawner(
                                self.current_map, self.fps, self)
                            self.start_time = time.time()
                            self.healt_bar = HealthBar("images/character/health.png")
                            self.timer_bar = TimerBar(
                                "images/character/clock.png")

                elif self.current_condition == CONDITIONS['game over']:
                    if self.game_over_buttons['continue'].check_click(i):
                        self.current_condition = CONDITIONS['choose map']

            if i.type == pygame.KEYDOWN:
                if self.current_condition == CONDITIONS['main title']:
                    self.current_condition = CONDITIONS['main menu']
                if i.key == pygame.K_BACKQUOTE:
                    self.cheat_engine = CheatCode(self)

        if self.current_condition == CONDITIONS['game']:
            self.time_since_start = int(
                (time.time() - self.start_time) * 100) / 100
            self.map.render(self.player_entity.x, self.player_entity.y, self)
            self.player_entity.update_movement(self.clock.get_fps())
            self.enemy_spawner.update_enemy_movement(
                self.player_entity.x, self.player_entity.y)
            self.player_entity.render(self)
            self.player_entity.shoot(self.time_since_start, self.clock.get_fps(), self)
            self.enemy_spawner.update_dificulty(self.time_since_start)
            if self.time_since_start % 1 == 0 and int(self.time_since_start) % 5 == 0:
                self.enemy_spawner.spawn_enemies()
            self.healt_bar.render(
                self, self.player_entity.hp, self.player_entity.max_hp)
            self.timer_bar.render(self, self.time_since_start)
            self.player_entity.check_collision(self, self.time_since_start)
            self.last_time = self.time_since_start
            if self.player_entity.hp <= 0:
                self.current_condition = CONDITIONS['game over']


    def create_default_settings_file(self):
        fps = 60
        volume = 100
        data = [str(fps), str(volume)]
        with open('data/default settings.txt', 'w') as settings:
            for line in data:
                for char in line:
                    settings.write(chr(ord(char) + CAESAR_SHIFT))
                settings.write('\n')
            settings.close()

    def create_settings_file(self):
        fps = self.fps
        volume = self.volume
        data = [str(fps), str(volume)]
        settings = open('data/settings.txt', 'w')
        for line in data:
            for char in line:
                settings.write(chr(ord(char) + CAESAR_SHIFT))
            settings.write('\n')
        settings.close()

    def read_settings(self, path):
        if not os.path.exists(path):
            self.create_default_settings_file()
        settings = open(path, 'r')
        data = []
        for line in settings:
            data.append(
                ''.join(map(lambda char: chr(ord(char) - CAESAR_SHIFT), line)))
        data = list(map(lambda y: y[:-1], data))
        self.fps = int(data[0])
        self.volume = int(data[1])
        settings.close()

    def reset_settings(self):
        self.read_settings('data/default settings.txt')
        self.create_settings_file()


class PLayerProfile():
    def __init__(self, path):
        self.path = path
        self.create_default_save_file('data/clear save.txt')
        if not os.path.exists(self.path):
            self.read_save('data/clear save.txt')
            self.create_save_file(self.path)
        self.read_save(self.path)

    def create_default_save_file(self, path):
        self.characters = (0,)
        self.maps = (0,)
        self.chips = 0
        self.create_save_file(path)

    def read_save(self, path):
        save_file = open(path, 'r')
        data = []
        for line in save_file:
            data.append(
                ''.join(map(lambda char: chr(ord(char) - CAESAR_SHIFT), line)))
        data = list(map(lambda y: y[:-1], data))
        self.chips = int(data[0])
        self.characters = list(map(lambda x: int(x), data[1].split(' ')))
        self.maps = list(map(lambda x: int(x), data[2].split(' ')))
        save_file.close()

    def create_save_file(self, path):
        characters = self.characters
        maps = self.maps
        chips = self.chips
        data = [str(chips),
                ' '.join(str(i) for i in characters),
                ' '.join(str(i) for i in maps)]
        settings = open(path, 'w')
        for line in data:
            for char in line:
                settings.write(chr(ord(char) + CAESAR_SHIFT))
            settings.write('\n')
        settings.close()

    def add_chips(self, value):
        self.chips += value


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, paths):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = [pygame.image.load(i).convert_alpha() for i in paths]
        self.image_count = 0
        self.image = self.images[self.image_count]
        self.size = self.image.get_size()[0] // 2
        self.rect = self.image.get_rect()
        self.rect.height //= 2
        self.rect.width //= 2


class Player(Entity):
    def __init__(self, x, y, paths):
        super().__init__(x, y, paths)
        self.rect.x = (1920 - self.size) // 2
        self.rect.y = (1080 - self.size) // 2
        self.speed = 300
        self.image = pygame.transform.scale(
            self.image, (100, 100)).convert_alpha()
        self.weapons = []
        self.max_hp = 100
        self.hp = 100
        self.iframes = 0.2
        self.last_hit_time = 0
    
    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def update_movement(self, fps):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        k = (self.speed/fps) / \
            (abs(1920 // 2 - mouse_x) + abs(1080 // 2 - mouse_y) + 1)
        self.x -= (1920 // 2 - mouse_x) * k
        self.y -= (1080 // 2 - mouse_y) * k

    def render(self, game_manager):
        game_manager.display.blit(self.image, (self.rect.x, self.rect.y))
        for i in self.weapons:
            i.render(game_manager)
    
    def shoot(self, time, fps, game_manager):
        for i in self.weapons:
            i.shoot(time, fps, game_manager)
    
    def check_collision(self, game_manager, time):
        collision = pygame.sprite.spritecollideany(
            self, game_manager.enemy_spawner.enemy_group)
        if collision != None and (time - self.last_hit_time) > self.iframes:
            self.hp -= collision.damage
            self.last_hit_time = time

class Weapon():
    def __init__(self, player, path, attack_interval=1, speed=10, damage=30):
        self.image = pygame.image.load(path)
        self.attack_interval = attack_interval
        self.speed = speed
        self.damage = damage
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.x = 1920 // 2
        self.rect.y = 1080 // 2
    
    def return_relative_coords(self, player_x, player_y):
        relative_x = 960 - player_x - 64 + self.x
        relative_y = 540 - player_y - 64 + self.y
        return int(relative_x), int(relative_y)
    
    def render(self, game_manager):
        relative_x, relative_y = self.return_relative_coords(
            self.player.x, self.player.y)
        self.rect.x = relative_x
        self.rect.y = relative_y
        game_manager.display.blit(self.image, (relative_x, relative_y))


class Hook(Weapon):
    def __init__(self, player, path='images/weapon/hook.png'):
        super().__init__(player, path, speed=1000)
        self.is_atacking = False
        self.reset_pos()
    
    def shoot(self, time, fps, game_manager):
        self.rect.x -= self.delta_x / fps
        self.rect.y -= self.delta_y / fps
        collision = pygame.sprite.spritecollideany(
            self, game_manager.enemy_spawner.enemy_group)
        if collision != None:
            game_manager.enemy_spawner.enemies.remove(collision)
            collision.kill()
            del collision
            self.reset_pos()
        if not((0 < self.rect.x < 1920) and (0 < self.rect.y < 1080)):
            self.reset_pos()
    
    def reset_pos(self):
        self.rect.x = 1920 // 2
        self.rect.y = 1080 // 2
        self.delta_x = randint(0, self.speed) * choice((-1, 1))
        self.delta_y = (self.speed ** 2 - self.delta_x **
                        2) ** 0.5 * choice((-1, 1))

    def render(self, game_manager):
        game_manager.display.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(Entity):
    def __init__(self, x, y, paths, group, damage=10, attack_speed=1, base_hp=100):
        super().__init__(x, y, paths)
        self.speed = 200
        self.base_damage = damage
        self.damage = self.base_damage
        self.attack_speed = attack_speed
        self.base_hp = base_hp
        self.group = group
        self.add(self.group)

    def update_movement(self, target_x, target_y, fps, frame_count):
        if frame_count % 30 == 0:
            self.image_count += 1
            self.image = self.images[self.image_count % len(self.images)]
        k = (self.speed/fps) / (abs(self.x - target_x) + abs(self.y - target_y))
        delta_x = (self.x - target_x) * k
        delta_y = (self.y - target_y) * k
        self.group.remove(self)
        self.rect.x -= delta_x
        self.rect.y -= delta_y
        collision = pygame.sprite.spritecollideany(self, self.group)
        if collision == None:
            self.x -= delta_x
            self.y -= delta_y
        else:
            if abs(collision.rect.x - 1920 / 2) < abs(self.rect.x - 1920 / 2):
                self.x += delta_x / 2
            else:
                self.x -= delta_x / 2
            if abs(collision.rect.y - 1080 / 2) < abs(self.rect.y - 1080 / 2):
                self.y += delta_y / 2
            else:
                self.y-= delta_y / 2
        self.add(self.group)

    def return_relative_coords(self, player_x, player_y):
        relative_x = 960 - player_x - 64 + self.x
        relative_y = 540 - player_y - 64 + self.y
        return int(relative_x), int(relative_y)
    
    def render(self, player_x, player_y, game_manager):
        relative_x, relative_y = self.return_relative_coords(player_x, player_y)
        self.rect.x = relative_x
        self.rect.y = relative_y
        game_manager.display.blit(self.image, (relative_x, relative_y))

    def update_stats(self, time):
        pass


class Warrior(Enemy):
    def __init__(self, x, y, paths, group):
        super().__init__(x, y, paths, group, 10, 1)

class EnemySpawner():
    def __init__(self, map, fps, game_manager):
        self.all_enemies_image = Image.new('RGB', (1920, 1080))
        self.map = map
        self.enemies = []
        self.fps = fps
        self.game_manager = game_manager
        self.enemy_group = pygame.sprite.Group()
        self.frame_count = 0

    def spawn_enemies(self):
        x = self.game_manager.player_entity.x
        y = self.game_manager.player_entity.y
        if self.game_manager.current_map == MAPS['underground']:
            spawn_count = 5
        else:
            spawn_count = 20
        for i in range(spawn_count):
            enemy_x = randint(0, 1920)
            enemy_y = randint(0, 1080)
            x_sign = randint(0, 2)
            y_sign = randint(0, 2)
            if x_sign == 0:
                enemy_x = x + enemy_x + 1920
            elif x_sign == 1:
                enemy_x = x - enemy_x - 1920
            if y_sign == 0:
                enemy_y = y + enemy_y + 1080
            else:
                enemy_y = y - enemy_y - 1080
            self.enemies.append(
                Warrior(enemy_x, enemy_y, (f'images/enemy/{self.map}/0.png', f'images/enemy/{self.map}/0_1.png'), self.enemy_group))

    def update_enemy_movement(self, target_x, target_y):
        self.all_enemies_image = Image.new('RGB', (1920, 1080), color=None)
        self.frame_count += 1
        for i in self.enemies:
            i.update_movement(target_x, target_y, self.game_manager.clock.get_fps(), self.frame_count)
            i.render(target_x, target_y, self.game_manager)


    def update_dificulty(self, time):
        self.dificulty = time // 60


def main():
    game_manager = GameManager()
    game_manager.main_loop()


if __name__ == '__main__':
    main()
