import os
import pygame
from interface import *


CONDITIONS = {'main title': 0, 'main menu': 1,
              'settings': 2, 'hub': 3, 'library': 4, 'characters': 5, 'upgrades': 6, 'choose map': 7}  # condition of game
MAPS = {'underground': 0, 'incineration plant': 1}
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
        self.current_map = None
        self.save = 'data/save.txt' if 'save.txt' in os.listdir(
            'data') else None

        self.main_title = Background('images/menu/main title.png')
        self.main_menu = Background('images/menu/main menu.png')
        self.hub_menu = Background('images/menu/hub menu.png')
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

    def main_loop(self):
        while True:
            self.clock.tick(self.fps)
            # load interface by condition
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
                self.hub_menu.render(self)
                for i in self.choose_map_menu_buttons:
                    self.choose_map_menu_buttons[i].render(self)

            # check events
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

                if i.type == pygame.KEYDOWN:
                    if self.current_condition == CONDITIONS['main title']:
                        self.current_condition = CONDITIONS['main menu']

            pygame.display.update()

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
        self.coins = 0
        self.create_save_file(path)

    def read_save(self, path):
        save_file = open(path, 'r')
        data = []
        for line in save_file:
            data.append(
                ''.join(map(lambda char: chr(ord(char) - CAESAR_SHIFT), line)))
        data = list(map(lambda y: y[:-1], data))
        self.coins = int(data[0])
        self.characters = list(map(lambda x: int(x), data[1].split(' ')))
        self.characters = list(map(lambda x: int(x), data[2].split(' ')))
        save_file.close()

    def create_save_file(self, path):
        characters = self.characters
        maps = self.maps
        coins = self.coins
        data = [str(coins),
                ' '.join(str(i) for i in characters),
                ' '.join(str(i) for i in maps)]
        settings = open(path, 'w')
        for line in data:
            for char in line:
                settings.write(chr(ord(char) + CAESAR_SHIFT))
            settings.write('\n')
        settings.close()


def main():
    game_manager = GameManager()
    game_manager.main_loop()


if __name__ == '__main__':
    main()
