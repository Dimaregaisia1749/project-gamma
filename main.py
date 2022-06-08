import os
import pygame

CONDITIONS = {'main title': 0, 'main menu': 1,
              'settings': 2}  # condition of game
FONT = "fonts/New Zelek.ttf"
MAIN_FONT_SIZE = 80
SLIDER_FONT_SIZE = 20
RADIO_BUTTON_FONT_SIZE = 30
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
        self.display = pygame.display.set_mode(self.resolution)
        self.main_title = Background('images/menu/main title.png')
        self.main_menu = Background('images/menu/main menu.png')
        self.current_condition = CONDITIONS['main title']
        self.saves = [f'data/saves/{i}' for i in os.listdir('data/saves')]
        # objects
        self.main_buttons = {}
        self.main_buttons['continue'] = Button(
            x=(self.resolution[0] - 800) // 2, y=100, text='Продолжить')
        self.main_buttons['new game'] = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Новая игра')
        self.main_buttons['load game'] = Button(
            x=(self.resolution[0] - 800) // 2, y=400, text='Загрузить')
        self.main_buttons['settings'] = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Настройки')
        self.main_buttons['exit'] = Button(
            x=(self.resolution[0] - 800) // 2, y=800, text='Выход')
        self.settings_buttons = {}
        self.settings_buttons['back'] = (
            Button(x=(self.resolution[0] - 800) // 2, y=800, text='Назад'))
        self.settings_buttons['volume'] = Slider(
            x=(self.resolution[0] - 800) // 2, y=200, text='Громкость')
        self.settings_buttons['fps'] = SwitchButton(
            x=(self.resolution[0] - 800) // 2, y=300, text='FPS', choices=['10', '30', '60', '120'], weight=200, value=self.fps)
        self.settings_buttons['reset'] = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Сбросить')

    def create_default_settings_file(self):
        fps = 60
        resolution = (1920, 1080)
        data = [str(fps), str(resolution[0]), str(resolution[1])]
        settings = open('data/default settings.txt', 'w')
        for line in data:
            for char in line:
                settings.write(chr(ord(char) + CAESAR_SHIFT))
            settings.write('\n')
        settings.close()

    def create_settings_file(self):
        fps = self.fps
        resolution = self.resolution
        data = [str(fps), str(resolution[0]), str(resolution[1])]
        settings = open('data/settings.txt', 'w')
        for line in data:
            for char in line:
                settings.write(chr(ord(char) + CAESAR_SHIFT))
            settings.write('\n')
        settings.close()

    def read_settings(self, path):
        settings = open(path, 'r')
        data = []
        for line in settings:
            data.append(
                ''.join(map(lambda char: chr(ord(char) - CAESAR_SHIFT), line)))
        data = list(map(lambda y: y[:-1], data))
        self.fps = int(data[0])
        self.resolution = (int(data[1]), int(data[2]))
        settings.close()

    def reset_settings(self):
        self.read_settings('data/default settings.txt')
        self.create_settings_file()

    def main_loop(self):
        while True:
            self.clock.tick(self.fps)

            # behaviour by condition
            if self.current_condition == CONDITIONS['main title']:
                self.main_title.render(self)
            elif self.current_condition == CONDITIONS['main menu']:
                self.main_menu.render(self)
                # check up saves
                if self.saves != []:
                    self.main_buttons['continue'].render(self)
                    self.main_buttons['new game'].y = 300
                    self.main_buttons['load game'].y = 500
                    self.main_buttons['settings'].y = 700
                    self.main_buttons['exit'].y = 900

                for i in self.main_buttons:
                    if i != 'continue':
                        self.main_buttons[i].render(self)
            elif self.current_condition == CONDITIONS['settings']:
                self.main_menu.render(self)
                for i in self.settings_buttons:
                    self.settings_buttons[i].render(self)

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

                    elif self.current_condition == CONDITIONS['settings']:
                        if self.settings_buttons['back'].check_click(i):
                            self.fps = self.settings_buttons['fps'].get_value()
                            self.create_settings_file()
                            self.current_condition = CONDITIONS['main menu']
                        if self.settings_buttons['reset'].check_click(i):
                            self.reset_settings()
                            self.settings_buttons['fps'].set_value(self.fps)
                        self.settings_buttons['volume'].set_value_by_mouse(i)
                        self.settings_buttons['fps'].set_value_by_mouse(i)
                if i.type == pygame.KEYDOWN:
                    if self.current_condition == CONDITIONS['main title']:
                        self.current_condition = CONDITIONS['main menu']

            pygame.display.update()


class UserInterface:
    def __init__(self, path):
        self.image = pygame.image.load(path)


class Background(UserInterface):
    def render(self, game_manager):
        game_manager.display.blit(self.image, self.image.get_rect())


class Button(UserInterface):
    def __init__(self, x=0, y=0, weight=800, height=150, text='sample', color=(0, 0, 0), path='images/menu/button.png'):
        super().__init__(path)
        self.weight = weight
        self.height = height
        self.font = pygame.font.Font(FONT, MAIN_FONT_SIZE)
        self.text_box = self.font.render(text, True, color)
        self.x, self.y = x, y

    def render(self, game_manager):
        image_rect = self.image.get_rect()
        text_box_rect = self.text_box.get_rect()
        game_manager.display.blit(self.image, (self.x, self.y))
        game_manager.display.blit(self.text_box, (self.x + (image_rect.width - text_box_rect.width) // 2,
                                                  (self.y + (image_rect.height - text_box_rect.height) // 2)))

    def check_click(self, event):
        if event.button == 1:
            if self.x <= pygame.mouse.get_pos()[0] <= self.x + self.weight:
                if self.y <= pygame.mouse.get_pos()[1] <= self.y + self.height:
                    return True
        return False


class Slider(UserInterface):
    def __init__(self, x=0, y=0, weight=800, height=20, text='sample', color=(0, 0, 0), value=100,
                 path_base='images/menu/slider base.png', path_circle='images/menu/slider circle.png'):
        self.image_base = pygame.image.load(path_base)
        self.image_circle = pygame.image.load(path_circle)
        self.value = value
        self.weight = weight
        self.height = height
        self.font = pygame.font.Font(FONT, SLIDER_FONT_SIZE)
        self.text = text
        self.text_color = color
        self.text_box = self.font.render(text, True, color)
        self.x, self.y = x, y

    def render(self, game_manager):
        image_base_rect = self.image_base.get_rect()
        text_box_rect = self.text_box.get_rect()
        self.text_box = self.font.render(
            self.text + f': {self.value}', True, self.text_color)
        self.image_circle_x = (self.x - 10) + self.value * self.weight // 100
        self.image_circle_y = self.y - 10
        game_manager.display.blit(self.image_base, (self.x, self.y))
        game_manager.display.blit(self.text_box, (self.x + (image_base_rect.width - text_box_rect.width) // 2,
                                                  (self.y + text_box_rect.height + 10)))
        game_manager.display.blit(
            self.image_circle, (self.image_circle_x, self.image_circle_y))

    def set_value_by_mouse(self, event):
        if event.button == 1:
            if self.x <= pygame.mouse.get_pos()[0] <= self.x + self.weight:
                if self.y <= pygame.mouse.get_pos()[1] <= self.y + self.height:
                    self.value = round(
                        (pygame.mouse.get_pos()[0] - self.x) / self.weight * 100)


class SwitchButton(UserInterface):
    def __init__(self, x=0, y=0, weight=800, height=150, text='sample', choices=['sample', 'sample2'], color=(0, 0, 0), value=0, space_between_buttons=100,
                 path_true='images/menu/button true.png', path_false='images/menu/button false.png', path='images/menu/fps button.png'):
        self.image_true = pygame.image.load(path_true)
        self.image_false = pygame.image.load(path_false)
        self.main_button = pygame.image.load(path)
        self.space_between_buttons = space_between_buttons
        self.choices = choices
        self.weight = weight
        self.height = height
        self.value = self.value = choices.index(str(value))
        self.main_font = pygame.font.Font(FONT, MAIN_FONT_SIZE)
        self.choices_font = pygame.font.Font(FONT, RADIO_BUTTON_FONT_SIZE)
        self.text_color = color
        self.text_box = self.main_font.render(text, True, color)
        self.text_box_of_choices = list(
            map(lambda x: self.choices_font.render(x, True, color), choices))
        self.x, self.y = x, y
        self.range_of_x_coord_buttons = list(map(lambda i:
                                                 range(self.x + self.weight + self.space_between_buttons * (i + 1) +
                                                       (self.image_true.get_rect(
                                                       ).height - self.text_box_of_choices[i].get_rect().width) // 2,
                                                       self.x + self.weight + self.space_between_buttons * (i + 1) +
                                                       (self.image_true.get_rect().height - self.text_box_of_choices[i].get_rect().width) // 2 + self.image_false.get_rect().width),
                                                 range(len(self.choices))))

    def render(self, game_manager):
        main_button_rect = pygame.transform.scale(
            self.main_button, (self.weight, self.height))
        text_box_rect = self.text_box.get_rect()
        game_manager.display.blit(main_button_rect, (self.x, self.y))
        game_manager.display.blit(self.text_box, (self.x + (self.weight - text_box_rect.width) // 2,
                                                  (self.y + (self.height - text_box_rect.height) // 2)))
        for i in range(len(self.choices)):
            if i == self.value:
                button_image = self.image_true
            else:
                button_image = self.image_false
            game_manager.display.blit(
                button_image, (self.x + self.weight + self.space_between_buttons * (i + 1), self.y))
            game_manager.display.blit(
                self.text_box_of_choices[i],
                (self.x + self.weight + self.space_between_buttons * (i + 1) +
                 (button_image.get_rect().height -
                  self.text_box_of_choices[i].get_rect().width) // 2,
                 self.y + button_image.get_rect().height))

    def set_value_by_mouse(self, event):
        if event.button == 1:
            if self.y <= pygame.mouse.get_pos()[1] <= self.y + self.height:
                buttons_on_which_mouse = list(map(lambda x: 1 if pygame.mouse.get_pos()[
                                              0] in x else 0, self.range_of_x_coord_buttons))
                if any(buttons_on_which_mouse):
                    self.value = buttons_on_which_mouse.index(1)
    
    def set_value(self, value):
        self.value = self.choices.index(str(value))

    def get_value(self):
        return int(self.choices[self.value])


def main():
    game_manager = GameManager()
    game_manager.main_loop()


if __name__ == '__main__':
    main()
