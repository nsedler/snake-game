import pygame
import snake
import apple


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

    def draw(self):
        self.game_window.fill((38, 70, 83))

        if self.player.direction != "":  # Make sure the snake should be moving
            self.player.move_snake()\

        # Collisions for checking if the player collides with the apple
        # if the snake head did collide then delete the apple, grow the snake, create a new apple and add 1 to the total score
        if self.player.rect.x == self.food.rect.x and self.player.rect.y == self.food.rect.y:
            self.food.delete_apple()
            self.player.snake_grow()
            self.food.create_apple()

            self.score += 1

        # Collision check for the snake touching itself
        if self.player.check_collision(): 
            self.score = "Game Over!"

        # Show the current score at the top middle of the screen
        score_surface = self.font.render(
            str(self.score), False, (248, 240, 227))
 
        # Draw the food and player
        self.food.draw(self.game_window)
        self.player.draw(self.game_window)

        self.game_window.blit(score_surface, (170, 20))
        pygame.display.update()

    def game_loop(self):
        self.food.create_apple() # Create the first apple 
        while self.running:
            self.clock.tick(15) # 15 FPS

            for event in pygame.event.get():
                self.player.on_event(event)

                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw()