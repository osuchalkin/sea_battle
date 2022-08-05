import pygame
import os


class Settings:
    """класс для хранения всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры"""
        # Screen settings
        if pygame.display.Info().current_w < 1200 or pygame.display.Info().current_h < 800:
            self.screen_width = pygame.display.Info().current_w - 100
            self.screen_height = pygame.display.Info().current_h - 50
        else:
            self.screen_width = 1200
            self.screen_height = 800
        self.bg_color = (0, 170, 255)

        self.caption = 'Sea Battle 2.0'
        self.icon = pygame.image.load(os.path.join('data', 'sb.png'))

        self.size_pic = 452  # 452 - размер картинки png
        self.xmargin = ((self.screen_width / 2) - self.size_pic) / 2
        self.ymargin = (self.screen_height - self.size_pic) / 2

        # параметры корабля
        self.ship_width = 40
        self.ship_height = 40
        self.ship_color = (255, 255, 0)
        self.ship_wounded_color = (255, 0, 0)
        self.ship_killed_color = (129, 129, 129)
        self.halo_color = (150, 150, 150)

        # параметры сетки (grid)
        self.grid_width = 12  # число колонок
        self.grid_height = 12  # число рядов (строк)
        self.space_size = 41  # ширина и высота каждого поля
        self.empty_space = ' '
        self.ship_space = 'S'
        self.halo_space = 'H'
        self.wounded_space = 'W'
        self.killed_space = 'K'
        self.halo_shoot = 'X'

        # параметры звука
        self.sound_on = True
        self.past_sound = pygame.mixer.Sound(os.path.join('data', 'past.mp3'))
        self.wounded_sound = pygame.mixer.Sound(os.path.join('data', 'wounded.mp3'))
        # self.killed_sound = pygame.mixer.Sound(os.path.join('data', 'killed.mp3'))
        self.prepared_sound = pygame.mixer.Sound(os.path.join('data', 'appear.wav'))
