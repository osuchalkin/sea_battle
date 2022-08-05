import pygame
import os
import copy


class Grid:
    """поле игры"""

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.width = self.settings.grid_width
        self.height = self.settings.grid_height
        self.space_size = self.settings.space_size

        self.board = []
        self.empty_space = self.settings.empty_space

        self.ocean_grid = pygame.image.load(os.path.join('data','oceangrid.png'))
        self.rect_ocean = self.ocean_grid.get_rect()
        self.rect_ocean.topleft = (self.settings.xmargin, self.settings.ymargin)

        self.radar_grid = pygame.image.load(os.path.join('data','radargrid.png'))
        self.rect_radar = self.radar_grid.get_rect()
        self.rect_radar.topright = (self.settings.screen_width - self.settings.xmargin, self.settings.ymargin)

        self.num_of_decks = 0
        self.num_of_killed_decks = 0
        # список (словарь) кораблей для расстановки на поле
        # 4 - 4-decks, 7, 10 - 3-decks, 12, 14, 16 - 2-decks, 17, 18, 19, 20 - 1-deck
        self.ships = {'4': False, '7': False, '10': False, '12': False, '14': False, '16': False,
                      '17': False, '18': False, '19': False, '20': False}

    def blit_grid(self, side):
        """рисуем океан или радар"""
        if side == 'ocean':
            self.screen.blit(self.ocean_grid, self.rect_ocean)
        if side == 'radar':
            self.screen.blit(self.radar_grid, self.rect_radar)

    def translate_grid_to_pixel_coord(self, x, y, grid):
        """перевод координат поля в пикселы"""
        if grid == 'ocean':
            return self.settings.xmargin + x * self.space_size + 1, \
                   self.settings.ymargin + y * self.space_size + 1
        if grid == "radar":
            add_x = self.settings.screen_width - (self.settings.size_pic + self.settings.xmargin * 2)
            return self.settings.xmargin + x * self.space_size + 1 + add_x, \
                   self.settings.ymargin + y * self.space_size + 1

    def get_space_clicked(self, mouse_pos, grid):
        """ Return a tuple of two integers of the board space coordinates where
        the mouse was clicked. (Or returns None not in any space.)"""
        mousex, mousey = mouse_pos
        x_board = self.settings.xmargin + 1
        y_board = self.settings.ymargin + 1
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if grid == 'ocean':
                    if x * self.space_size + x_board < mousex < (x + 1) * self.space_size + x_board and \
                            y * self.space_size + y_board < mousey < (y + 1) * self.space_size + y_board:
                        return x, y
                if grid == 'radar':
                    add_x = self.settings.screen_width - (self.settings.size_pic + self.settings.xmargin * 2)
                    if x * self.space_size + x_board + add_x < mousex < (x + 1) * self.space_size + x_board + add_x \
                            and y * self.space_size + y_board < mousey < (y + 1) * self.space_size + y_board:
                        return x, y
        return None

    def get_new_board(self):
        """Creates a brand new, empty board data structure."""
        for i in range(self.width):
            self.board.append([self.empty_space] * self.height)

    def set_ships_on_grid(self, x, y):
        """расстановка кораблей и проверка"""
        if self.check_place_ship(x, y):
            self.board[x][y] = self.settings.ship_space
            if self.settings.sound_on == True: self.settings.prepared_sound.play()
            self.num_of_decks += 1
            if self.num_of_decks in (4, 7, 10, 12, 14, 16, 17, 18, 19, 20):
                self.set_halo(self.board, self.settings.ship_space)
                if not self.check_ships_on_grid():
                    return False
        return True

    def check_place_ship(self, x, y):
        """проверка - правильно ли построен корабль"""
        virt_board = copy.deepcopy(self.board)
        if virt_board[x][y] != self.settings.empty_space:
            return False
        else:
            virt_board[x][y] = self.settings.ship_space

        if self.num_of_decks in (0, 4, 7, 10, 12, 14, 16, 17, 18, 19):
            return True
        elif self.num_of_decks in (1, 5, 8, 11, 13, 15):
            if (virt_board[x][y] == virt_board[x + 1][y]) or (virt_board[x][y] == virt_board[x - 1][y]) or \
                    (virt_board[x][y] == virt_board[x][y + 1]) or (virt_board[x][y] == virt_board[x][y - 1]):
                return True
        elif self.num_of_decks in (2, 3, 6, 9):
            if 1 < x < 10:
                if virt_board[x - 1][y] == virt_board[x - 2][y] == self.settings.ship_space \
                        or virt_board[x + 1][y] == virt_board[x + 2][y] == self.settings.ship_space:
                    return True
            if 1 < y < 10:
                if virt_board[x][y - 1] == virt_board[x][y - 2] == self.settings.ship_space \
                        or virt_board[x][y + 1] == virt_board[x][y + 2] == self.settings.ship_space:
                    return True
            if x == 1:
                if virt_board[x + 1][y] == virt_board[x + 2][y] == self.settings.ship_space:
                    return True
            if x == 10:
                if virt_board[x - 1][y] == virt_board[x - 2][y] == self.settings.ship_space:
                    return True
            if y == 1:
                if virt_board[x][y + 1] == virt_board[x][y + 2] == self.settings.ship_space:
                    return True
            if y == 10:
                if virt_board[x][y - 1] == virt_board[x][y - 2] == self.settings.ship_space:
                    return True
        else:
            return False

    def check_ships_on_grid(self):
        """проверка установки кораблей на поле в зависимости от количества построенных палуб"""
        ship = str(self.num_of_decks)
        self.ships[ship] = True

        if self.num_of_decks == 20:
            return False
        return True

    def set_halo(self, board, status):
        """устанавливаем ореол вокруг корабля"""
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if board[x][y] == status:
                    self._check_halo(board, status, x - 1, y - 1)
                    self._check_halo(board, status, x - 1, y)
                    self._check_halo(board, status, x - 1, y + 1)
                    self._check_halo(board, status, x, y - 1)
                    self._check_halo(board, status, x, y + 1)
                    self._check_halo(board, status, x + 1, y - 1)
                    self._check_halo(board, status, x + 1, y)
                    self._check_halo(board, status, x + 1, y + 1)

    def _check_halo(self, board, status, x, y):
        """вспомогательная функция для set_halo"""
        if status == self.settings.ship_space:
            if board[x][y] == self.settings.empty_space:
                board[x][y] = self.settings.halo_space
        if status == self.settings.killed_space:
            if board[x][y] == self.settings.empty_space or board[x][y] == self.settings.halo_space:
                board[x][y] = self.settings.halo_shoot

    def count_killed_decks(self, board):
        """подсчет убитых палуб и определение победителя"""
        self.num_of_killed_decks = 0
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if board[x][y] == self.settings.killed_space:
                    self.num_of_killed_decks += 1
        if self.num_of_killed_decks == 20:
            return True
        return False
