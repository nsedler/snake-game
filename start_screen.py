import os
import sys

import pygame
import pygame_gui

import game
import snekdb


class StartScreen(object):
    def __init__(self, width, height, score):
        pygame.init()
        pygame.font.init()

        self.width = width
        self.height = height

        self.manager = pygame_gui.UIManager(
            (350, 350), 'data/button_theme.json')

        self.font = pygame.font.SysFont("Comic Sans MS", 22)

        self.start_window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (140, 150), (75, 25)), text="Play", manager=self.manager, object_id="#play_button")
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (140, 200), (75, 25)), text="Exit", manager=self.manager, object_id="#exit_button")
        self.test_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (140, 250), (75, 25)), text="test", manager=self.manager, object_id="#exit_button")

        self.running = True

        self.score = score

        self.db = snekdb.SnekDB()

    def draw(self):
        self.start_window.fill((0, 0, 0))
        score_surface = self.font.render(
            str(self.score), False, (248, 240, 227))
        self.start_window.blit(score_surface, (170, 20))

    def game_loop(self):

        while self.running:
            time_delta = self.clock.tick(15)/1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.exit_button:
                            self.running == False
                            pygame.quit()
                        elif event.ui_element == self.play_button:
                            game_window = game.GameWindow(
                                self.width, self.height, "Snake")
                            game_window.game_loop()
                            self.running = False
                        elif event.ui_element == self.test_button:
                            self.db.get_scoreboard()
                            self.running = False

            self.manager.update(time_delta)
            self.draw()
            self.manager.draw_ui(self.start_window)
            pygame.display.update()
