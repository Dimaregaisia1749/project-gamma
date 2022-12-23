from PIL import Image
from random import randint
import os
import pygame


class Map():
    def __init__(self, map_name):
        map = map_name
        self.variations_of_chunks = []
        for _ in range(9):
            image = Image.new('RGB', (1024, 1024))
            for i in range(8):
                for j in range(8):
                    path = f'images/maps/{map}/{randint(1, len(os.listdir(f"images/maps/{map}")))}.png'
                    texture = Image.open(path)
                    image.paste(texture, (128 * i, 128 * j))
            mode = image.mode
            size = image.size
            data = image.tobytes()
            image = pygame.image.fromstring(
                data, size, mode)
            self.variations_of_chunks.append(image)

        self.chunks_dict = {}
        self.add_chunks([i, j] for i in range(-1, 2) for j in range(-1, 2))


    def add_chunks(self, cords):
        for cord in cords:
            if f'{cord[0]} {cord[1]}' not in self.chunks_dict.keys():
                image = self.variations_of_chunks[randint(0, len(self.variations_of_chunks) - 1)]
                self.chunks_dict[f'{cord[0]} {cord[1]}'] = Chunk(
                    cord[0], cord[1], image)    

    def render(self, player_x, player_y, game_manager):
        self.player_x = int(player_x)
        self.player_y = int(player_y)
        self.current_chunk_x = self.player_x // 1024
        self.current_chunk_y = self.player_y // 1024
        self.current_chunk_relative_x = 1960//2 - self.player_x % 1024 - 1024
        self.current_chunk_relative_y = 1080//2 - self.player_y % 1024 - 1024
        self.add_chunks([i, j] for i in range(self.current_chunk_x - 2, self.current_chunk_x + 1)
                        for j in range(self.current_chunk_y - 2, self.current_chunk_y + 1))
        for i in range(self.current_chunk_x - 2, self.current_chunk_x + 1):
            for j in range(self.current_chunk_y - 2, self.current_chunk_y + 1):
                current_image_chunks = self.chunks_dict[f'{i} {j}'].image
                game_manager.display.blit(current_image_chunks, (
                    self.current_chunk_relative_x + 1024 * (i - self.current_chunk_x + 2), self.current_chunk_relative_y + 1024 * (j - self.current_chunk_y + 2)))


class Chunk():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
