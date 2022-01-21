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

        self.font = pygame.font.SysFont("Comic Sans MS", 18)

        self.start_window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.prev_page_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (25, 270), (75, 25)), text="<<<", manager=self.manager, object_id="#prev_page")
        self.next_page_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (250, 270), (75, 25)), text=">>>", manager=self.manager, object_id="#next_page")

        self.running = True

        self.leaderboard_book = self.db.get_scoreboard()
        self.leaderboard_page = 1

    def get_page_count(self):
        return len(self.leaderboard_book)

    def get_current_page(self, page_number):
        board = self.leaderboard_book[page_number - 1][page_number]
        html_text = ''

        for ScoreID, Score, Name in board:
            html_text += f'{Score} {Name} <br>'

        return html_text

    def draw(self):
        self.start_window.fill((0, 0, 0))
        score_text = self.get_current_page(self.leaderboard_page)
        score_board = pygame_gui.elements.UITextBox(
            score_text,
            pygame.Rect(10, 10, 300, 150),
            manager=self.manager,
            object_id="#scoreboard"
        )

        page_surface = self.font.render(
            str(self.leaderboard_page), False, (248, 240, 227))
        self.start_window.blit(page_surface, (170, 270))

    def game_loop(self):

        page_count = self.get_page_count()

        while self.running:

            time_delta = self.clock.tick(15)/1000.0

            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.db.close_db()
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.next_page_button:
                            if self.leaderboard_page < page_count:
                                self.leaderboard_page += 1
                        elif event.ui_element == self.prev_page_button:
                            if self.leaderboard_page > 1:
                                self.leaderboard_page -= 1

            self.manager.update(time_delta)
            self.draw()
            self.manager.draw_ui(self.start_window)
            pygame.display.update()
