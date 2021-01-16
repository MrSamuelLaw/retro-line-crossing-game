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
from timeit import default_timer as now
from tkinter import TclError
from math import floor


# ================== classes ==================
class Player():
    """Class that handles player state and turtle object"""
    # class wide variables
    base_distance = 0.5

    # methods
    def __init__(self, canvas=None):
        self.score = 0
        self.distance_per_loop = self.base_distance
        self.cursor = turtle.RawTurtle(canvas=canvas) if canvas else turtle.Turtle()
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

    def reset_trace(self):
        """Clears the trace, used for starting new games"""
        self.x_vec.clear()
        self.y_vec.clear()

    def turn_right(self):
        """Updates the trace and turns right"""
        self.cursor.right(90)
        self.update_trace()

    def turn_left(self):
        """Updates the trace and turns left"""
        self.cursor.left(90)
        self.update_trace()

    def move(self):
        """Moves the player in the current direction
        at the desired speed"""
        self.cursor.forward(self.distance_per_loop)

    def update_score(self):
        """Increments the score"""
        self.score += self.distance_per_loop

    def update_dist_per_loop(self):
        """Increments the distance per loop"""
        self.distance_per_loop = self.base_distance*((floor(self.score/1000)*0.5) + 1)

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
    def __init__(self, canvas=None):
        self.screen = turtle.TurtleScreen(cv=canvas) if canvas else turtle.Screen()
        self.screen.tracer(False)
        self.player_list = []
        self.paused = True
        self.play_again = None
        self.screen.onkey(self.toggle_pause, 'space')
        self.screen.onkey(self.play_again_true, 'y')
        self.screen.onkey(self.play_again_false, 'n')

    def play_again_false(self):
        self.play_again = False

    def play_again_true(self):
        self.play_again = True

    def add_player(self, player: Player):
        self.player_list.append(player)

    def toggle_pause(self):
        self.paused = not self.paused

    def border_collision_detected(self):
        """checks to see if either player is out of bounds"""
        for p in self.player_list:
            x, y = p.get_pos()
            if any([(abs(x) >= (self.screen.window_width()/2)),     # out of bounds width
                    (abs(y) >= (self.screen.window_height()/2))]):  # out of bounds height
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

        # collect indicies & traces
        indices = [i for i in range(len(self.player_list))]
        traces = [p.get_trace() for p in self.player_list]
        # loop over the player list by index
        for i in indices:
            try:
                # collect the necessary vectors
                x_vec, y_vec = traces[i]
                x_last_vec, y_last_vec = x_vec[-2:], y_vec[-2:]
                # check tail against own trace
                if self.check_for_intersection(x_vec[:-3], y_vec[:-3], x_last_vec, y_last_vec):
                    return True
                # check tail against other traces
                for j in [v for v in indices if v != i]:
                    x_vec, y_vec = traces[j]
                    if self.check_for_intersection(x_vec, y_vec, x_last_vec, y_last_vec):
                        return True
            except IndexError:
                pass

        # # collect the tails and traces
        # traces = [p.get_trace() for p in self.player_list]
        # tails = [(x[-2:], y[-2:]) for x, y in traces]
        # for i, (x_last_vec, y_last_vec) in enumerate(tails):
        #     for j, (x_vec, y_vec) in enumerate(traces):
        #         try:
        #             cutoff = -3 if i == j else None
        #             if self.check_for_intersection(x_vec[:cutoff], y_vec[:cutoff], x_last_vec, y_last_vec):
        #                 return True
        #         except IndexError:
        #             pass

    def save_data(self):
        """Writes out the player's x, y values
        to a csv for debugging purposes"""
        for i, p in enumerate(self.player_list, start=1):
            with open(f'player{i}_trace.csv', 'w') as f:
                f.write(f"player{i}_x, player{i}_y")
                [f.write(f"{x},{y}\n") for x, y in zip(*p.get_trace())]

    def game_over(self):
        # put message on the screen
        turtle.write(
            "Play Again? [y/n]",
            align="center",
            font=("Arial", 20, "normal")
        )
        turtle.hideturtle()
        while self.play_again is None:
            self.screen.update()

    def setup_players(self):
        # set the starting positions
        n = len(self.player_list)
        w = self.screen.window_width()
        x = round(float(w/(n+1)), 2)
        for i, p in enumerate(self.player_list, start=1):
            p.set_starting_pos(((w/2)-(i*x)), 0)
            p.cursor.left(90)
            # set up the key bindings
            if i == 1:
                self.screen.onkey(p.turn_right, 'Right')
                self.screen.onkey(p.turn_left, 'Left')
            elif i == 2:
                self.screen.onkey(p.turn_right, 'd')
                self.screen.onkey(p.turn_left, 'a')

    def run_loop(self):
        # start the game
        while True:
            self.screen.update()  # update the screen always
            if not self.paused:   # update the players if not paused
                # update player state
                [p.update_score() for p in self.player_list]          # update score
                [p.update_dist_per_loop() for p in self.player_list]  # update dist
                [p.move() for p in self.player_list]                  # tell everyone to move
                # check to make sure no out of bounds or intersected
                if self.border_collision_detected():
                    print('border_collision_detected')
                    break
                if self.line_intersection_detected():
                    print('line_intersection_detected')
                    break


def play_pytron(number_of_players=1):
    try:
        turtle.speed(0)           # no animations
        turtle.delay(0)           # no delays
        turtle.Screen().clear()   # reset screen
        turtle.title('pytron')    # add a title
        game = Game()             # create a new game object

        for i in range(number_of_players):
            game.add_player(Player())  # add players

        game.setup_players()  # set up the players
        game.screen.listen()  # start listening for events
        game.run_loop()       # start the round
        game.game_over()      # handles cleanup
        if game.play_again is False:
            return False
        elif game.play_again is True:
            return True
    except (TclError, turtle.Terminator):
        pass