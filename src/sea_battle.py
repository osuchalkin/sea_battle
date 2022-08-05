import sys

import pygame
import random
from time import sleep, time

from settings import Settings
from grid import Grid
from ship import Ship
from text import TextImage


class Game:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        pygame.display.set_icon(self.settings.icon)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        self.text = TextImage(self)

        # human
        self.grid_ocean = Grid(self)
        self.player_ship = Ship(self)
        self.prepare = True  # флаг подготовки к игре

        # computer
        self.grid_radar = Grid(self)
        self.comp_ship = Ship(self)
        self.computer_prepare = True
        self.computer_shoot_status = 'random'
        # x, y для AI
        self.x_shoot = 0
        self.y_shoot = 0

        self.game_active = False
        self.turn = ''
        self.winner = ''
        self.high_status = ''

    def run_game(self):
        """запуск основного цикла"""
        if self.settings.sound_on: self.settings.wounded_sound.play()
        self.screen.fill(self.settings.bg_color)
        self.text.show_text_screen('SEA BATTLE')

        while True:
            if not self.game_active:
                self.new_game()
            else:
                if not self.get_winner():
                    if self.turn == 'computer':
                        self.high_status = 'Computer shoots'
                        self.computer_ai(self.grid_ocean.board, self.computer_shoot_status)
                    else:
                        self.high_status = 'Human shoots'

            self._check_events()

            self._update_screen()

    def get_winner(self):
        """определяет победителя"""
        if self.grid_ocean.count_killed_decks(self.grid_ocean.board) or self.grid_radar.count_killed_decks(
                self.grid_radar.board):
            if self.grid_ocean.count_killed_decks(self.grid_ocean.board):
                self.winner = 'COMPUTER'
            elif self.grid_radar.count_killed_decks(self.grid_radar.board):
                self.winner = 'HUMAN'

            self.high_status = ''

            self.game_active = False
            self.prepare = True
            self.computer_prepare = True

            return True
        else:
            return False

    def new_game(self):
        """новая игра"""
        # обнуляем установки
        del self.grid_ocean
        del self.grid_radar
        self.grid_ocean = Grid(self)
        self.grid_radar = Grid(self)
        self.grid_ocean.get_new_board()
        self.grid_radar.get_new_board()
        self.computer_shoot_status = 'random'
        self.x_shoot = 0
        self.y_shoot = 0
        self.winner = ''
        self.high_status = 'PREPARE TO BATTLE'

        if self.prepare:
            self.prepare_to_battle()
        sleep(1)

        if self.computer_prepare:
            self.computer_set_ships()
            self.turn = random.choice(['human', 'computer'])

        self.game_active = True

    def prepare_to_battle(self):
        """расстановка кораблей"""
        while self.prepare:
            self._check_events()

            self._update_screen()

    def computer_set_ships(self):
        """компьютер расстанавливает корабли"""
        while self.computer_prepare:
            self._check_events()
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            if not self.grid_radar.set_ships_on_grid(x, y):
                self.computer_prepare = False

    def _kill_ship(self, board, x, y):
        """превращаем раненные корабли в окончательно убитые"""
        if board[x - 1][y] == self.settings.wounded_space:
            for i in range(1, 4):
                if x - i < 0:
                    break
                else:
                    if board[x - i][y] == self.settings.wounded_space:
                        board[x - i][y] = self.settings.killed_space
        if board[x + 1][y] == self.settings.wounded_space:
            for i in range(1, 4):
                if x + i > 11:
                    break
                else:
                    if board[x + i][y] == self.settings.wounded_space:
                        board[x + i][y] = self.settings.killed_space
        if board[x][y - 1] == self.settings.wounded_space:
            for i in range(1, 4):
                if y - i < 0:
                    break
                else:
                    if board[x][y - i] == self.settings.wounded_space:
                        board[x][y - i] = self.settings.killed_space
        if board[x][y + 1] == self.settings.wounded_space:
            for i in range(1, 4):
                if y + i > 11:
                    break
                else:
                    if board[x][y + i] == self.settings.wounded_space:
                        board[x][y + i] = self.settings.killed_space

    def _killed(self, board, x, y):
        """убит"""
        board[x][y] = self.settings.killed_space
        if self.settings.sound_on: self.settings.wounded_sound.play()
        # self.settings.killed_sound.play()
        # перекрасить все W в К
        self._kill_ship(board, x, y)
        # ореол вокруг убитого корабля из 'X'
        if self.turn == 'human':
            self.grid_radar.set_halo(board, self.settings.killed_space)
        else:
            self.grid_ocean.set_halo(board, self.settings.killed_space)
            self.computer_shoot_status = 'random'

    def _get_w_coord(self, board, crux, x, y):
        """вспомогательная для wounded_or_killed"""
        direction, x_w, y_w, x_ww, y_ww = 0, 0, 0, 0, 0
        for i in range(4):
            if crux[i] == self.settings.wounded_space:
                direction = i
        if direction == 0:
            x_w, y_w = x, y - 1
            x_ww, y_ww = x, y - 2
        elif direction == 1:
            x_w, y_w = x, y + 1
            x_ww, y_ww = x, y + 2
        elif direction == 2:
            x_w, y_w = x - 1, y
            x_ww, y_ww = x - 2, y
        elif direction == 3:
            x_w, y_w = x + 1, y
            x_ww, y_ww = x + 2, y
        crux_w = list(board[x_w][y_w - 1] + board[x_w][y_w + 1] + board[x_w - 1][y_w] + board[x_w + 1][y_w])
        if x_ww + 1 > 11 or x_ww - 1 < 0 or y_ww + 1 > 11 or y_ww - 1 < 0:  # не выходим за границы поля
            crux_ww = crux_w
        else:
            crux_ww = list(
                board[x_ww][y_ww - 1] + board[x_ww][y_ww + 1] + board[x_ww - 1][y_ww] + board[x_ww + 1][y_ww])
        if self.settings.ship_space in crux_w:
            return True
        elif self.settings.wounded_space in crux_w:
            if self.settings.ship_space in crux_ww \
                    and (board[x_ww][y_ww] != self.settings.empty_space
                         and board[x_ww][y_ww] != self.settings.halo_space
                         and board[x_ww][y_ww] != self.settings.halo_shoot):
                return True
            else:
                return False
        else:
            return False

    def wounded_or_killed(self, board, x, y):
        """проверка - ранен или убит"""
        crux = list(board[x][y - 1] + board[x][y + 1] + board[x - 1][y] + board[x + 1][y])

        if self.settings.ship_space in crux:
            board[x][y] = self.settings.wounded_space
            if self.settings.sound_on: self.settings.wounded_sound.play()
            if self.turn == 'computer':
                self.x_shoot, self.y_shoot = x, y
                self.computer_ai(board, self.computer_shoot_status)
        elif self.settings.wounded_space in crux:
            if self._get_w_coord(board, crux, x, y):
                board[x][y] = self.settings.wounded_space
                if self.settings.sound_on: self.settings.wounded_sound.play()
                if self.turn == 'computer':
                    self.x_shoot, self.y_shoot = x, y
                    self.computer_ai(board, self.computer_shoot_status)
            else:
                self._killed(board, x, y)
        else:
            self._killed(board, x, y)

    def shoots(self, board, x, y, player):
        """стрельба"""
        # попал
        if board[x][y] == self.settings.ship_space:
            if player == 'computer':
                self.computer_shoot_status = 'wounded'
            board[x][y] = self.settings.wounded_space
            # функция: ранен или убит
            self.wounded_or_killed(board, x, y)
        # мимо
        if board[x][y] == self.settings.empty_space or board[x][y] == self.settings.halo_space:
            if self.settings.sound_on: self.settings.past_sound.play()
            board[x][y] = self.settings.halo_shoot
            if player == 'human':
                self.turn = 'computer'
            else:
                self.turn = 'human'

    def computer_shoot_random(self):
        """стреляет компьютер"""
        result = False
        while not result:
            x = random.randint(1, 10)
            y = random.randint(1, 10)

            if self.grid_ocean.board[x][y] != self.settings.wounded_space \
                    and self.grid_ocean.board[x][y] != self.settings.killed_space \
                    and self.grid_ocean.board[x][y] != self.settings.halo_shoot:
                result = True
        self.shoots(self.grid_ocean.board, x, y, 'computer')

    def computer_ai(self, board, status):
        """искуственный интеллект"""
        # компьютер "думает"
        pause_until = time() + random.randint(15, 25) * 0.1
        while time() < pause_until:
            self._update_screen()

        if status == 'random':
            self.computer_shoot_random()
        if status == 'wounded':
            result = False
            x, y = self.x_shoot, self.y_shoot
            # для 4-палубного
            if board[x][y] == board[x][y - 1] == board[x][y - 2] == self.settings.wounded_space:
                coords = [(x, y + 1), (x, y - 3)]
            elif board[x][y] == board[x][y + 1] == board[x][y + 2] == self.settings.wounded_space:
                coords = [(x, y - 1), (x, y + 3)]
            elif board[x][y] == board[x - 1][y] == board[x - 2][y] == self.settings.wounded_space:
                coords = [(x + 1, y), (x - 3, y)]
            elif board[x][y] == board[x + 1][y] == board[x + 2][y] == self.settings.wounded_space:
                coords = [(x - 1, y), (x + 3, y)]
            # для 3-палубных
            elif board[x][y] == board[x][y - 1] == self.settings.wounded_space:
                coords = [(x, y + 1), (x, y - 2)]
            elif board[x][y] == board[x][y + 1] == self.settings.wounded_space:
                coords = [(x, y - 1), (x, y + 2)]
            elif board[x][y] == board[x - 1][y] == self.settings.wounded_space:
                coords = [(x + 1, y), (x - 2, y)]
            elif board[x][y] == board[x + 1][y] == self.settings.wounded_space:
                coords = [(x - 1, y), (x + 2, y)]
            # для 2-палубных
            else:
                coords = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            while not result:
                xx, yy = random.choice(coords)
                if 0 < xx < 11 and 0 < yy < 11:
                    if board[xx][yy] != self.settings.wounded_space \
                            and board[xx][yy] != self.settings.killed_space \
                            and board[xx][yy] != self.settings.halo_shoot:
                        result = True
            self.shoots(board, xx, yy, 'computer')

    def _check_mouse_prepare(self):
        """события мыши во время подготовки"""
        mouse_pos = pygame.mouse.get_pos()
        # проверка, что клик на океане
        mousexy = self.grid_ocean.get_space_clicked(mouse_pos, 'ocean')
        if mousexy is not None:
            x, y = mousexy
            # проверка - правильно ли построен корабль
            if not self.grid_ocean.set_ships_on_grid(x, y):
                self.prepare = False

    def _check_mouse_shoot(self):
        """игрок стреляет мышкой"""
        mouse_pos = pygame.mouse.get_pos()
        # проверка, что клик на океане
        mousexy = self.grid_radar.get_space_clicked(mouse_pos, 'radar')
        if mousexy is not None:
            x, y = mousexy
            self.shoots(self.grid_radar.board, x, y, 'human')

    def _check_keyup_events(self, event):
        """Вспомогательная для _check_events"""
        if event.key == pygame.K_i:
            # информация
            self.screen.fill(self.settings.bg_color)
            self.text.show_info_screen('Sea Battle 2.0', self.text.info_text)
        elif event.key == pygame.K_h:
            # help
            self.screen.fill(self.settings.bg_color)
            self.text.show_info_screen('Little Help', self.text.help_text)
        elif event.key == pygame.K_n:
            self.new_game()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_s:
            if self.settings.sound_on == True:
                self.settings.sound_on = False
            else:
                self.settings.sound_on = True

    def _check_events(self):
        """Обрабатываем нажатия клавиш и мышь"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                # для prepare_to_battle
                if self.prepare:
                    self._check_mouse_prepare()
                # стреляет игрок
                if self.turn == 'human':
                    self._check_mouse_shoot()

    def draw_ship_in_grid(self, side, board, ship):
        """отображение кораблей на полях"""
        for x in range(1, self.settings.grid_width - 1):
            for y in range(1, self.settings.grid_height - 1):
                centerx, centery = self.grid_ocean.translate_grid_to_pixel_coord(x, y, side)
                if board[x][y] == self.settings.ship_space:
                    if side == 'ocean':
                        ship.draw_ship(centerx, centery, self.settings.ship_space)
                    if side == 'radar' and self.winner == 'COMPUTER':
                        ship.draw_ship(centerx, centery, self.settings.ship_space)
                if board[x][y] == self.settings.wounded_space:
                    ship.draw_ship(centerx, centery, self.settings.wounded_space)
                if board[x][y] == self.settings.killed_space:
                    ship.draw_ship(centerx, centery, self.settings.killed_space)
                if board[x][y] == self.settings.halo_shoot:
                    ship.draw_halo(centerx, centery)

    def _update_screen(self):
        """Обновляет изображения на экране"""
        self.screen.fill(self.settings.bg_color)

        # рисуем сетку с океаном
        self.grid_ocean.blit_grid('ocean')
        # отображение моделей кораблей для расстановки
        if self.prepare:
            self.player_ship.draw_models_ships(self.grid_ocean.ships)

        # отображение кораблей в океане
        self.draw_ship_in_grid('ocean', self.grid_ocean.board, self.player_ship)

        if not self.computer_prepare or self.winner != '':
            self.grid_radar.blit_grid('radar')
            # отображение кораблей на радаре
            self.draw_ship_in_grid('radar', self.grid_radar.board, self.comp_ship)

        # верхний статус
        self.text.show_text_status(self.high_status)

        if self.winner != '':
            self.low_status = ''
            self.high_status = ''
            winner = f'{self.winner} WINS!'
            self.text.show_winner(winner)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
