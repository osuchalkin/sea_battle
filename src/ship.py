import pygame


class Ship:
    """класс корабля"""

    def __init__(self, game):
        """Создает объект корабля."""
        self.screen = game.screen
        self.settings = game.settings

        self.color = self.settings.ship_color
        self.wounded_color = self.settings.ship_wounded_color
        self.killed_color = self.settings.ship_killed_color
        self.halo_color = self.settings.halo_color

        self.width = self.settings.ship_width
        self.height = self.settings.ship_height

        self.ship_status = {self.settings.ship_space: self.color,
                            self.settings.wounded_space: self.wounded_color,
                            self.settings.killed_space: self.killed_color}

        self.rect = pygame.Rect(0, 0, self.width, self.height)

    def draw_ship(self, x, y, status):
        """выводит палубу на экран"""
        color = self.ship_status.get(status)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, color, self.rect)
        if status == self.settings.killed_space:
            pygame.draw.line(self.screen, (255, 255, 255), (x + 1, y + 1),
                             (x + (self.width - 1), y + (self.height - 1)), 2)
            pygame.draw.line(self.screen, (255, 255, 255), (x + (self.width - 1), y + 1),
                             (x + 1, y + (self.height - 1)), 2)
        if status == self.settings.halo_shoot:
            pygame.draw.circle(self.screen, color, (x + self.width / 2, y + self.height / 2), 10, 0)

    def draw_halo(self, x, y):
        """рисуем ореол вокруг убитого корабля и отмечает мимо-выстрел"""
        pygame.draw.circle(self.screen, self.halo_color, (x + self.width / 2, y + self.height / 2), 5, 0)

    def draw_models_ships(self, ships):
        """выводит все корабли рядом с океаном при расстановке"""
        # 4-палубный
        if not ships['4']:
            self._draw_model(4, 2, 1)
        # 3-палубные
        if not ships['7']:
            self._draw_model(3, 2, 4)
        if not ships['10']:
            self._draw_model(3, 5, 4)
        # 2-палубные
        if not ships['12']:
            self._draw_model(2, 0, 9)
        if not ships['14']:
            self._draw_model(2, 3, 9)
        if not ships['16']:
            self._draw_model(2, 6, 9)
        # 1-палубные
        if not ships['17']:
            self._draw_model(1, 0, 1)
        if not ships['18']:
            self._draw_model(1, 7, 1)
        if not ships['19']:
            self._draw_model(1, 0, 5)
        if not ships['20']:
            self._draw_model(1, 7, 5)

    def _draw_model(self, decks, x, y):
        """вспомогательная функция для рисования модели корабля"""
        begin_x = self.settings.space_size * x
        begin_y = self.settings.space_size * y
        if decks == 3:
            for i in range(decks):
                self.rect = pygame.Rect((self.settings.screen_width / 2) + (((self.settings.screen_width / 2) -
                                                                             self.settings.size_pic) / 2) + begin_x,
                                        self.settings.ymargin + begin_y + i * self.settings.space_size,
                                        self.width, self.height)
                pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            for i in range(decks):
                self.rect = pygame.Rect((self.settings.screen_width / 2) + (((self.settings.screen_width / 2) -
                                                                             self.settings.size_pic) / 2) +
                                        begin_x + i * self.settings.space_size,
                                        self.settings.ymargin + begin_y,
                                        self.width, self.height)
                pygame.draw.rect(self.screen, self.color, self.rect)
