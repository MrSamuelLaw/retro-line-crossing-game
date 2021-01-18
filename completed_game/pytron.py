# ================================================= #
# Author: Samuel Law                                #
# Title: Line Crossing Game                         #
#                                                   #
# Description:                                      #
# A simple game where the goal is to stay           #
# alive by not allowing a line intersection         #
# ================================================= #

import turtle
from timeit import default_timer as now
from tkinter import TclError
from math import floor, sqrt


# ================== classes ==================
class Player():
    """Class that handles player state and turtle object"""
    # class wide variables
    base_distance = 2.0

    # methods
    def __init__(self, canvas=None, key_bindings={}):
        self.score = 0
        self.movable = 1
        self.x_vec, self.y_vec = [], []
        self.distance_per_loop = self.base_distance
        self.cursor = turtle.RawTurtle(canvas=canvas) if canvas else turtle.Turtle()
        self.cursor.degrees()  # set the turtle module to degrees
        self.left_btn = key_bindings.get('left_btn', None)
        self.right_btn = key_bindings.get('right_btn', None)

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

    def freeze(self):
        self.movable = 0

    def update_score(self):
        """Increments the score"""
        self.score += self.distance_per_loop

    def update_dist_per_loop(self):
        """Increments the distance per loop"""
        self.distance_per_loop = self.movable*self.base_distance \
                                 *((floor(self.score/1000)*0.5) + 1)

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
        # Game stuff
        self.player_list = []        # holds the player list
        self.paused = True           # paused flag
        self.game_over_limit = None  # allows single and muli player modes
        self.play_again = None       # flag that enables the y/n selection at end of round
        # Gui stuff
        self.screen = turtle.TurtleScreen(cv=canvas) if canvas else turtle.Screen()
        self.screen.tracer(False)
        self.screen.onkey(self.toggle_pause, 'space')

    def play_again_false(self):
        self.play_again = False

    def play_again_true(self):
        self.play_again = True

    def add_player(self, player: Player):
        """Adds a Player object to the Game player_list
        and sets the game_over_limit correctly"""
        self.player_list.append(player)
        self.game_over_limit = 1 % len(self.player_list)

    def toggle_pause(self):
        self.paused = not self.paused

    def boarder_collision_detected(self, x, y):
        if any([(abs(x) >= (self.screen.window_width()/2)),     # out of bounds width
                (abs(y) >= (self.screen.window_height()/2))]):  # out of bounds height
            return True

    def check_for_border_collisions(self):
        """checks to see if either player is out of bounds"""
        [p.freeze() for p in self.player_list if self.boarder_collision_detected(*p.get_pos())]

    def line_intersection_detected(self, x_vec, y_vec, x_last_vec, y_last_vec):
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
                return (x_intersection, y_intersection)  # evaluates to true

    def magnitude(self, p1, p2):
        """Returns the magnitude of the vector between
        two points p1, and p2. Points are interables
        in the form of p = [x, y]."""
        x1, y1, x2, y2 = [*p1, *p2]
        mag = (x2 - x1)*(x2 - x1)
        mag += (y2 - y1)*(y2 - y1)
        mag = sqrt(mag)
        return mag

    def check_for_line_intersections(self):
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
                if self.line_intersection_detected(x_vec[:-3], y_vec[:-3], x_last_vec, y_last_vec):
                    self.player_list[i].freeze()
                    continue

                # check tail against other traces
                for j in [v for v in indices if v != i]:
                    x_vec, y_vec = traces[j]
                    intersection = self.line_intersection_detected(x_vec, y_vec, x_last_vec, y_last_vec)
                    if intersection:
                        # if player at index[i] is closer to the intersection point, player i should freeze
                        if self.magnitude(intersection, (x_last_vec[-1], y_last_vec[-1])) < self.magnitude(intersection, (x_vec[-1], y_vec[-1])):
                            self.player_list[i].freeze()
                        # if player at index[j] is closer to the intersection point, player j should freeze
                        elif self.magnitude(intersection, (x_last_vec[-1], y_last_vec[-1])) > self.magnitude(intersection, (x_vec[-1], y_vec[-1])):
                            self.player_list[j].freeze()
                        # if player at index[j] & player at index[i] are equidistant from intersection they both freeze
                        else:
                            self.player_list[i].freeze()
                            self.player_list[j].freeze()
            except IndexError:
                pass

    def num_players_movable(self):
        """Returns the number of players currently
        alive"""
        return sum([p.movable for p in self.player_list])

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
        # await user input
        self.screen.onkey(self.play_again_true, 'y')
        self.screen.onkey(self.play_again_false, 'n')
        while self.play_again is None:
            self.screen.update()
        # turn off y/n keys
        self.screen.onkey(None, 'y')
        self.screen.onkey(None, 'n')

    def setup_players(self):
        # calculate the starting positions
        n = len(self.player_list)       # number of players
        w = self.screen.window_width()  # total screen width
        x = round(float(w/(n+1)), 2)    # spacing between each player
        # assign starting position and key bindings
        for i, p in enumerate(self.player_list, start=1):
            p.set_starting_pos(((w/2)-(i*x)), 0)  # set starting position
            p.cursor.left(90)                     # make them point north
            # set up the key bindings
            self.screen.onkey(p.turn_right, p.right_btn)
            self.screen.onkey(p.turn_left, p.left_btn)

    def run_loop(self):
        start = now()                       # set the time stamp
        while True:                         # start the game
            self.screen.update()            # update the screen always
            while (now() - start) < 0.040:  # maintain approx 25 fps
                pass
            start = now()                   # update the time stamp
            if not self.paused:             # update the players if not paused
                # update player state
                [p.update_score() for p in self.player_list]          # update score
                [p.update_dist_per_loop() for p in self.player_list]  # update dist
                [p.move() for p in self.player_list]                  # tell everyone to move
                # check to make sure no out of bounds or intersected
                self.check_for_border_collisions()
                self.check_for_line_intersections()
                if self.num_players_movable() <= self.game_over_limit:
                    break


def play_pytron(key_bindings):
    try:
        turtle.speed(0)           # no animations
        turtle.delay(0)           # no delays
        turtle.Screen().clear()   # reset screen
        turtle.title('pytron')    # add a title
        game = Game()             # create a new game object

        for binding in key_bindings:
            game.add_player(Player(key_bindings=binding))  # add players

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
