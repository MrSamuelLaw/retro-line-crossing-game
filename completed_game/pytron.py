#!.venv/Scripts/python.exe
# ============================================ #
# Author: Samuel Law                           #
# Title: Line Crossing Game                    #
#                                              #
# Description:                                 #
# A simple game where the goal is to stay      #
# alive by not allowing a line intersection    #
#                                              #
# ============================================ #

import turtle
import importlib
from tkinter import TclError
from math import floor
from itertools import zip_longest, chain


# ================== classes ==================
class Player():
    """Class that handles player state and turtle object"""
    # class wide variables
    base_distance = 2.5

    # methods
    def __init__(self, canvas=None):
        self.score = 0
        self.distance_per_loop = self.base_distance
        self.cursor = turtle.RawTurtle(canvas=canvas) if canvas else turtle.Turtle()
        self.cursor.speed(10)  # ensure the gui loop updates fast
        self.cursor.degrees()  # set the turtle module to degrees
        self.x_vec, self.y_vec = [], []

    def get_pos(self):
        """Returns the position in a way
        that will not cause errors in the line
        detection algorithm as 5.499999 will
        be rounded to 5.50 """
        x, y = self.cursor.pos()
        return (round(x, 2), round(y, 2))

    def update_trace(self):
        """Add the point to the trace"""
        x, y = self.get_pos()
        self.x_vec.append(x)
        self.y_vec.append(y)

    def get_trace(self):
        """Returns two vectors that represent the
        the "traced" image resulting from the players
        moves, does include the current position """
        x, y = self.get_pos()
        if (x == self.x_vec[-1]) and (y == self.y_vec[-1]):
            return self.x_vec, self.y_vec
        else:
            return [*self.x_vec, x], [*self.y_vec, y]

    def turn_right(self):
        """Updates the trace and turns right"""
        self.update_trace()
        self.cursor.right(90)

    def turn_left(self):
        """Updates the trace and turns left"""
        self.update_trace()
        self.cursor.left(90)

    def update_score(self):
        """Increments the score"""
        self.score += self.distance_per_loop

    def update_dist_per_loop(self):
        """Increments the speed"""
        self.distance_per_loop = self.base_distance*((floor(self.score/1000)*0.5) + 1)

    def move(self):
        """Moves the player in the current direction
        at the desired speed"""
        self.cursor.forward(self.distance_per_loop)

    def set_starting_pos(self, x=0, y=0):
        """Moves the player to the desired starting position
        with out drawing a line"""
        self.cursor.penup()       # don't draw
        self.cursor.setpos(x, y)  # go to point x, y
        self.cursor.pendown()     # get ready to draw
        self.update_trace()       # add x, y to the vectors


class Game():
    """Class that handles game state and the
    turtle packages Screen object"""

    # methods
    def __init__(self):
        self.screen = turtle.Screen()
        self.paused = True
        self.player_list = []

    def add_player(self, player: Player):
        self.player_list.append(player)

    def toggle_pause(self):
        self.paused = not self.paused

    def border_collision_detected(self):
        """checks to see if either player is out of bounds"""
        for p in self.player_list:
            x, y = p.get_pos()
            if any([(abs(x) > (self.screen.window_width()/2)),     # out of bounds width
                    (abs(y) > (self.screen.window_height()/2))]):  # out of bounds height
                return True

    def check_for_intersection(self, x_vec, y_vec, x_last_vec, y_last_vec):
        """checks to see if the line segment described by x_last_vec
        & y_last_vec cross any of the lines in x_vec & y_vec"""

        # determine the x and y intersection values
        for i in range(len(x_vec)):
            x_intersection = ((len(set(x_vec[i:i+2])) % 2) * x_vec[i]) + ((len(set(x_last_vec)) % 2) * x_last_vec[0])
            y_intersection = ((len(set(y_vec[i:i+2])) % 2) * y_vec[i]) + ((len(set(y_last_vec)) % 2) * y_last_vec[0])

            # determine if the intersection point is a part of both vectors
            if all([
                (min(x_vec[i:i+2]) <= x_intersection <= max(x_vec[i:i+2])),  # does x intersect with some line
                (min(x_last_vec) <= x_intersection <= max(x_last_vec)),      # does x intersect with current line
                (min(y_vec[i:i+2]) <= y_intersection <= max(y_vec[i:i+2])),  # does y intersect with some line
                (min(y_last_vec) <= y_intersection <= max(y_last_vec))       # does y intersect with current line
            ]):
                return True

    def line_intersection_detected(self):
        """Calls the check_for_intersection function on each
        player's last segment using all the lines from all players"""

        # collect the tails and traces
        traces = [p.get_trace() for p in self.player_list]
        tails = [(x[-2:], y[-2:]) for x, y in traces]
        for i, (x_last_vec, y_last_vec) in enumerate(tails):
            for j, (x_vec, y_vec) in enumerate(traces):
                try:
                    cutoff = -3 if i == j else None
                    if self.check_for_intersection(x_vec[:cutoff], y_vec[:cutoff], x_last_vec, y_last_vec):
                        return True
                except IndexError:
                    pass

    def save_data(self):
        """Writes out the player's x, y values
        to a csv for debugging purposes"""
        with open('log.csv', 'w') as f:
            # write out the header
            header = [f'player{i+1}_x,player{i+1}_y' for i, _ in enumerate(self.player_list)]
            f.write(','.join(header))
            f.write('\n')
            # collect the player traces
            traces = [p.get_trace() for p in self.player_list]
            traces = list(chain(*traces))
            # write out the player traces
            [f.write(str(t)[1:-1]+'\n') for t in zip_longest(*traces)]

    def game_over(self):
        self.screen.bgcolor('red')
        self.save_data()
        self.screen.exitonclick()


def game_loop():
    # ================= setup =================
    # set the title
    turtle.title("pytron")
    # create the player(s)
    player1 = Player()
    player2 = Player()
    # create the game objects
    game = Game()
    # add the player(s) to the game
    game.add_player(player1)
    game.add_player(player2)
    # set up the plyaer bindings
    game.screen.onkey(player1.turn_right, 'Right')
    game.screen.onkey(player1.turn_left, 'Left')
    game.screen.onkey(player2.turn_right, 'd')
    game.screen.onkey(player2.turn_left, 'a')
    game.screen.onkey(game.toggle_pause, 'space')
    # set the positions
    # player1.set_starting_pos()
    player1.set_starting_pos(100, 0)
    player2.set_starting_pos(-100, 0)
    player1.cursor.left(90)
    player2.cursor.left(90)
    # begin listening
    game.screen.listen()

    # =============== game loop ===============
    try:
        # start the game
        while True:
            game.screen.update()
            if not game.paused:
                # update player state
                [p.update_score() for p in game.player_list]
                [p.update_dist_per_loop() for p in game.player_list]
                [p.move() for p in game.player_list]
                # check to make sure no out of bounds
                if game.border_collision_detected():
                    print('border_collision_detected')
                    break
                if game.line_intersection_detected():
                    print('line_intersection_detected')
                    break
        # end the game
        game.game_over()
        turtle.mainloop()
        del game
    # handle window close
    except (TclError, turtle.Terminator):
        pass


def start_game_loop():
    while True:
        game_loop()
        i = str(input("play again [y, n]\n"))
        if i.lower() == 'n':
            break
        # if play again
        importlib.reload(turtle)

    # from cProfile import Profile
    # from pstats import Stats, SortKey
    # profiler = Profile()
    # profiler.runcall(main)
    # stats = Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats(SortKey.TIME)
    # stats.print_stats()
