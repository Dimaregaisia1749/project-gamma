import os
import pygame

CONDITIONS = {'main title': 0, 'main menu': 1}  # condition of game
FONT = "New Zelek.ttf"
FONT_SIZE = 80


class GameManager:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('project gamma')
        self.fps = 100
        self.resolution = (1920, 1080)
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(self.resolution)
        self.main_title = Background('images/menu/main title.png')
        self.main_menu = Background('images/menu/main menu.png')
        self.current_condition = CONDITIONS['main title']
        self.saves = []
        # objects
        self.continue_button = Button(
            x=(self.resolution[0] - 800) // 2, y=100, text='Продолжить')
        self.new_game_button = Button(
            x=(self.resolution[0] - 800) // 2, y=200, text='Новая игра')
        self.load_game_button = Button(
            x=(self.resolution[0] - 800) // 2, y=400, text='Загрузить')
        self.settings_button = Button(
            x=(self.resolution[0] - 800) // 2, y=600, text='Настройки')
        self.exit_button = Button(
            x=(self.resolution[0] - 800) // 2, y=800, text='Выход')

    def main_loop(self):
        while True:
            self.clock.tick(self.fps)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.check_click(i):
                        exit()
                if i.type == pygame.KEYDOWN:
                    if self.current_condition == CONDITIONS['main title']:
                        self.current_condition = CONDITIONS['main menu']
            # behaviour by condition
            if self.current_condition == CONDITIONS['main title']:
                self.main_title.render(self)
            elif self.current_condition == CONDITIONS['main menu']:
                self.main_menu.render(self)
                # check up saves
                if os.listdir('saves') != []:
                    self.continue_button.render(self)
                    self.new_game_button.y = 300
                    self.load_game_button.y = 500
                    self.settings_button.y = 700
                    self.exit_button.y = 900
                    self.saves = [f'/saves/{i}' for i in os.listdir('saves')]
                self.new_game_button.render(self)
                self.load_game_button.render(self)
                self.settings_button.render(self)
                self.exit_button.render(self)
            pygame.display.update()

class UserProfile():
    pass

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
        self.font = pygame.font.Font(FONT, FONT_SIZE)
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


def main():
    game_manager = GameManager()
    game_manager.main_loop()


if __name__ == '__main__':
    main()
