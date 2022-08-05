import pygame.font
import pygame
import sys


class TextImage:
    """для вывода текстовой информации"""

    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        self.text_color = (255, 255, 0)
        self.text_shadow_color = (170, 170, 0)
        self.text_status_color = (0, 0, 255)

        self.small_font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 100)
        self.status_font = pygame.font.SysFont(None, 50)
        self.info_font = pygame.font.SysFont(None, 30)

        self.info_text = ['Sea Battle (or Battleship)',
                          'is known worldwide as a pencil and paper game which dates from World War I.',
                          '',
                          'Maps created by Molly "Cougarmint" Willits:',
                          'https://www.deviantart.com/cougarmint',
                          '',
                          'Sounds are from https://zvukipro.com/1748-zvuki-vystrela-iz-korabelnyh-pushek.html',
                          '',
                          '© Oleh Suchalkin 2021-22']

        self.help_text = ['I - info text',
                          '',
                          'H - this help',
                          '',
                          'N - new game',
                          '',
                          'Q - quit',
                          '',
                          'S - sound on / off',
                          '']


    def make_text_obj(self, text, font, text_color):
        image = font.render(text, True, text_color)
        image_rect = image.get_rect()
        return image, image_rect

    def show_text_screen(self, text):
        """показывает большой текст в центре экрана - название, окончание и проч."""
        # рисует тень
        title_screen, title_rect = self.make_text_obj(text, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.screen_width / 2),
                             int(self.settings.screen_height / 2))
        self.screen.blit(title_screen, title_rect)

        # рисует текст
        title_screen, title_rect = self.make_text_obj(text, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.screen_width / 2) - 3,
                             int(self.settings.screen_height / 2) - 3)
        self.screen.blit(title_screen, title_rect)

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play', self.small_font, self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()

    def check_for_keypress(self):
        """ожидает события KEYUP"""
        # проверка на выход из програмы (Х или ESC)
        self.check_for_quit()
        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event == pygame.KEYDOWN:
                continue
            return event.key
        return None

    def check_for_quit(self):
        for event in pygame.event.get(pygame.QUIT):  # get all the QUIT event
            pygame.quit()
            sys.exit()

    def show_text_status(self, text):
        """верхний статус игры: подготовка, стрельба, победитель"""
        title_screen, title_rect = self.make_text_obj(text, self.status_font, self.text_status_color)
        title_rect.center = (int(self.settings.screen_width / 2), int(self.settings.ymargin / 2))
        self.screen.blit(title_screen, title_rect)

    def show_winner(self, text):
        """статус игры: подготовка, стрельба, победитель"""
        title_screen, title_rect = self.make_text_obj(text, self.status_font, self.text_status_color)
        title_rect.center = (int(self.settings.screen_width / 2), int(self.settings.ymargin / 2))
        self.screen.blit(title_screen, title_rect)

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play again', self.small_font,
                                                            self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()

    def show_info_screen(self, title, text):
        """показывает информационный текст"""
        # рисует тень
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_shadow_color)
        title_rect.center = (int(self.settings.screen_width / 2), 100)
        self.screen.blit(title_screen, title_rect)

        # рисует текст
        title_screen, title_rect = self.make_text_obj(title, self.big_font, self.text_color)
        title_rect.center = (int(self.settings.screen_width / 2) - 3, 100 - 3)
        self.screen.blit(title_screen, title_rect)

        i = 1
        for info in text:
            title_screen, title_rect = self.make_text_obj(info, self.info_font, self.text_color)
            title_rect.center = (int(self.settings.screen_width / 2), 300 + 30 * i)
            self.screen.blit(title_screen, title_rect)
            i += 1

        # рисуем "Press a key to play"
        presskey_screen, presskey_rect = self.make_text_obj('Press a key to play', self.small_font, self.text_color)
        presskey_rect.center = (int(self.settings.screen_width / 2),
                                int(self.settings.screen_height / 2) + 300)
        self.screen.blit(presskey_screen, presskey_rect)

        while self.check_for_keypress() is None:
            pygame.display.flip()
