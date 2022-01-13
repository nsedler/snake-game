import pygame


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.snake_pieces = [pygame.rect.Rect(150, 150, 10, 10), pygame.rect.Rect(
            160, 150, 10, 10), pygame.rect.Rect(170, 150, 10, 10)]
        self.direction = ""
        self.rect = self.snake_pieces[-1]

    def draw(self, win):
        for coord in self.snake_pieces:
            pygame.draw.rect(win, (244, 162, 97), coord)
            pygame.draw.rect(win, (244, 162, 97), coord, 1)

    # Calculates the next snake piece position and creates a rect from it
    def next_snake_piece(self):
        next_coord = (0, 0)
        # check which is the current direction and adjust the axis accordingly
        if self.direction == "DOWN":
            next_coord = (self.snake_pieces[-1].x,
                          self.snake_pieces[-1].y + 10)
        elif self.direction == "UP":
            next_coord = (self.snake_pieces[-1].x,
                          self.snake_pieces[-1].y - 10)
        elif self.direction == "RIGHT":
            next_coord = (
                self.snake_pieces[-1].x + 10, self.snake_pieces[-1].y)
        elif self.direction == "LEFT":
            next_coord = (
                self.snake_pieces[-1].x - 10, self.snake_pieces[-1].y)

        # create and return the new piece
        new_piece = pygame.rect.Rect(next_coord[0], next_coord[1], 10, 10)
        return new_piece

    # Moves the snake in the current direction
    # pop tail and add new head to give appearance of movement

    def move_snake(self):
        new_head = self.next_snake_piece()

        self.rect = new_head

        self.snake_pieces.pop(0)
        self.snake_pieces.append(new_head)

    # Adds a piece to the snake
    def snake_grow(self):

        new_head = self.next_snake_piece()
        self.snake_pieces.append(new_head)

    # Collision check for the snake colliding with itself or the wall
    def check_collision(self):
        head = self.snake_pieces[-1]

        # collision check for the snake colliding with itself
        for piece in self.snake_pieces[:-1]:
            cur_x = piece.x
            cur_y = piece.y
            if head.x == cur_x and head.y == cur_y:
                self.direction = ""
                return True

        # collision check for the snake colliding with the wall
        if head.x > 350 or head.x < 0:
            self.direction = ""
            return True
        if head.y < 0 or head.y > 350:
            self.direction = ""
            return True
        return False

    # handles all events for Snake
    def on_event(self, event):

        # Keyboard events (key down) for snake movement direction
        # There is a check to make sure the snake cannot move into itself
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:

                if self.direction != "RIGHT":
                    print("LEFT DOWN")
                    self.direction = "LEFT"
            elif event.key == pygame.K_RIGHT:

                if self.direction != "LEFT":
                    print("RIGHT DOWN")
                    self.direction = "RIGHT"

            elif event.key == pygame.K_UP:

                if self.direction != "DOWN":
                    print("UP DOWN")
                    self.direction = "UP"

            elif event.key == pygame.K_DOWN:

                if self.direction != "UP":
                    print("DOWN DOWN")
                    self.direction = "DOWN"

            elif event.key == pygame.K_SPACE:

                self.snake_grow()
