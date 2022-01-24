import start_screen

WIDTH = 350
HEIGHT = 350


if __name__ == "__main__":
    screen = start_screen.StartScreen(WIDTH, HEIGHT)
    screen.game_loop()
