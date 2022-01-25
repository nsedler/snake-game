import pygame

import apple
import game_over
import snake
import snekdb
import start_screen


class GameWindow(object):
    def __init__(self, width, height, title):

        pygame.font.init()

        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Comic Sans MS", 22)

        # Get the window, caption and time started
        self.game_window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        # Create our game objects
        self.player = snake.Snake()
        self.food = apple.Apple()

        self.running = True
        self.score = 0  # score default is 0

        self.db = snekdb.SnekDB()

    def quit_game(self):
        # Creates a new game over screen
        over_screen = game_over.GameOver(self.width, self.height, self.score)
        over_screen.game_loop()

        # Set running to False - ending the game
        self.running = False

    def reset_game(self):
        # Resets game to initial position
        self.score = 0
        self.player.reset_snake()

    def draw(self):
        self.game_window.fill((38, 70, 83))

        if self.player.direction != "":  # Make sure the snake should be moving
            self.player.move_snake()

        # Collisions for checking if the player collides with the apple
        # if the snake head did collide then delete the apple, grow the snake, create a new apple and add 1 to the total score
        if self.player.rect.x == self.food.rect.x and self.player.rect.y == self.food.rect.y:
            self.food.delete_apple()
            self.player.snake_grow()
            self.food.create_apple()

            self.score += 1
            pygame.display.set_caption(f"Snek | Score: {self.score}")

        # Collision check for the snake touching itself
        if self.player.check_collision():
            self.quit_game()

        # Draw the food and player
        self.food.draw(self.game_window)
        self.player.draw(self.game_window)
        pygame.display.update()

    def game_loop(self):
        self.food.create_apple()  # Create the first apple
        while self.running:
            self.clock.tick(12)  # 12 FPS

            for event in pygame.event.get():
                self.player.on_event(event)

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:

                    # Escape returns to the starting screen
                    if event.key == pygame.K_ESCAPE:
                        screen = start_screen.StartScreen(350, 350)
                        screen.game_loop()
                        self.running = False

                    # R restarts game
                    if event.key == pygame.K_r:
                        self.reset_game()

            self.draw()
