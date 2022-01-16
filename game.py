import pygame
import start_screen
import snake
import apple
import snekdb


class GameWindow(object):
    def __init__(self, width, height, title):

        pygame.font.init()

        self.font = pygame.font.SysFont("Comic Sans MS", 22)

        self.game_window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.player = snake.Snake()
        self.food = apple.Apple()

        self.running = True
        self.score = 0

        self.db = snekdb.SnekDB()

    def quit_game(self):

        insert_statement = f"INSERT INTO sys.test_table (random_string) VALUES (\"{self.score}\")"
        self.db.cursor.execute(insert_statement)
        self.db.cnx.commit()
        self.db.close_db()

        start = start_screen.StartScreen(self.score)
        start.game_loop()
        self.running = False

    def reset_game(self):
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
            self.clock.tick(15)  # 15 FPS

            for event in pygame.event.get():
                self.player.on_event(event)

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_r:
                        self.reset_game()

            self.draw()
