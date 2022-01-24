import string

import pygame
import pygame_gui

import game
import snekdb
import start_screen


class GameOver(object):
    def __init__(self, width, height, score):
        self.score = score

        self.db = snekdb.SnekDB()

        self.width = width
        self.height = height

        pygame.font.init()

        self.manager = pygame_gui.UIManager(
            (width, height), './data/button_theme.json')

        self.font = pygame.font.SysFont("Comic Sans MS", 22)

        self.start_window = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        self.submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (130, 180), (75, 25)), text="Submit", manager=self.manager, object_id="#submit_button")

        self.skip_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (130, 205), (75, 25)), text="Skip", manager=self.manager, object_id="#skip_button")

        self.home_button = pygame_gui.elements.UIButton(relative_rect=pygame.rect.Rect(
            (130, 230), (75, 25)), text="Home", manager=self.manager, object_id="#home_button")

        # UITextEntryLine with a limit of 5 uppercase ascii characters
        self.name_text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.rect.Rect(
            (180, 120), (100, 30)), manager=self.manager)
        self.name_text_entry.length_limit = 5
        self.name_text_entry.allowed_characters = string.ascii_uppercase

        self.running = True

    def draw(self):
        self.start_window.fill((0, 0, 0))

        # Draw the score
        score_surface = self.font.render(
            f'Score: {self.score}', False, (248, 240, 227))
        self.start_window.blit(score_surface, (50, 120))

    def game_loop(self):

        while self.running:
            time_delta = self.clock.tick(15)/1000.0
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.submit_button:

                            # Insert the score and name into Scores
                            # commit the cursor execute and close database
                            insert_statement = f"INSERT INTO sys.Scores (Score, Name) VALUES ({self.score}, \"{self.name_text_entry.get_text()}\")"
                            self.db.cursor.execute(insert_statement)
                            self.db.cnx.commit()
                            self.db.close_db()

                            # After inserting the score open the game window and close game_over
                            game_window = game.GameWindow(
                                self.width, self.height, "Snek")
                            game_window.game_loop()
                            self.running = False

                        elif event.ui_element == self.skip_button:
                            # Skip entering a score and go straight back to the game
                            game_window = game.GameWindow(
                                self.width, self.height, "Snek")
                            game_window.game_loop()
                            self.running = False

                        elif event.ui_element == self.home_button:
                            screen = start_screen.StartScreen(350, 350)
                            screen.game_loop()

            self.manager.update(time_delta)
            self.draw()
            self.manager.draw_ui(self.start_window)
            pygame.display.update()
