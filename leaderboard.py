import pygame
import pygame_gui

import snekdb


class Leaderboard(object):
    def __init__(self, width, height):

        self.db = snekdb.SnekDB()

        self.width = width
        self.height = height

        pygame.font.init()

        self.manager = pygame_gui.UIManager(
            (width, height), './data/button_theme.json')

        self.font = pygame.font.SysFont("Comic Sans MS", 22)

        self.start_window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.prev_page_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (25, 270), (75, 25)), text="<<<", manager=self.manager, object_id="#prev_page")
        self.next_page_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (250, 270), (75, 25)), text=">>>", manager=self.manager, object_id="#next_page")

        self.running = True

        self.leaderboard_book = self.db.get_scoreboard()
        self.leaderboard_page = 1

    def draw(self):
        self.start_window.fill((0, 0, 0))

    def game_loop(self):

        while self.running:
            time_delta = self.clock.tick(15)/1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.db.close_db()
                    self.running = False

            self.manager.update(time_delta)
            self.draw()
            self.manager.draw_ui(self.start_window)
            pygame.display.update()
