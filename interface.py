import pygame


FONT = "fonts/New Zelek.ttf"
MAIN_FONT_SIZE = 80
SLIDER_FONT_SIZE = 25
RADIO_BUTTON_FONT_SIZE = 30


class UserInterface:
    def __init__(self, path, x=0, y=0):
        self.x, self.y = x, y
        self.image = pygame.image.load(path)

    def render(self, game_manager):
        game_manager.display.blit(self.image, (self.x, self.y))


class Title(UserInterface):
    def __init__(self, text, x=0, y=0, color=(0, 0, 0), font_size=MAIN_FONT_SIZE):
        self.x, self.y = x, y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(FONT, font_size)

    def render(self, game_manager):
        self.text_box = self.font.render(self.text, True, self.color)
        game_manager.display.blit(self.text_box, (self.x, self.y))


class Background(UserInterface):
    def render(self, game_manager):
        game_manager.display.blit(self.image, self.image.get_rect())


class Button(UserInterface):
    def __init__(self, x=0, y=0, weight=800, height=150, text='sample', color=(0, 0, 0), path='images/menu/button.png', font_size=MAIN_FONT_SIZE):
        super().__init__(path, x=x, y=y)
        self.weight = weight
        self.height = height
        self.font = pygame.font.Font(FONT, font_size)
        self.text_box = self.font.render(text, True, color)

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
    def __init__(self, x=0, y=0, weight=800, height=20, text='sample', color=(0, 0, 0), value=100, max_value=100,
                    path_base='images/menu/slider base.png', path_circle='images/menu/slider circle.png',
                    font_size=SLIDER_FONT_SIZE):
        self.image_base = pygame.image.load(path_base)
        self.image_circle = pygame.image.load(path_circle)
        self.value = value
        self.max_value = max_value
        self.weight = weight
        self.height = height
        self.font = pygame.font.Font(FONT, font_size)
        self.text = text
        self.text_color = color
        self.text_box = self.font.render(text, True, color)
        self.x, self.y = x, y

    def render(self, game_manager):
        image_base_rect = self.image_base.get_rect()
        text_box_rect = self.text_box.get_rect()
        self.text_box = self.font.render(
            self.text + f': {self.value}', True, self.text_color)
        self.image_circle_x = (self.x - 10) + self.value * \
            self.weight // self.max_value
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
                        (pygame.mouse.get_pos()[0] - self.x) / self.weight * self.max_value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
