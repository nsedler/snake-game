import start_screen

WIDTH = 350
HEIGHT = 350


# TODO leaderboard page system maybe 5 per page
if __name__ == "__main__":
    screen = start_screen.StartScreen(WIDTH, HEIGHT, 0)
    screen.game_loop()
