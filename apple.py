import pygame
import random


class Apple(object):
    def __init__(self):
        # Empty array of apples (should only ever contain 1 apple)
        self.apple = []

    # Creates an apple at a random location

    def create_apple(self):

        # Get the random coords for the apple
        random_x = random.randrange(0, 350, 10)
        random_y = random.randrange(0, 350, 10)

        self.apple.append(pygame.rect.Rect(random_x, random_y, 10, 10))
        self.rect = self.apple[-1]  # Sets self.rect to the current apple

    # Deletes the current apple
    def delete_apple(self):
        self.apple.pop(0)

    def draw(self, win):

        pygame.draw.rect(win, (151, 184, 93), self.apple[0])
