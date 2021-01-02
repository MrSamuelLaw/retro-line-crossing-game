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
from tkinter import TclError
from typing import List
from math import floor


# ================= type defs =================
Vector = List[float]


# ================== globals ==================
X_VALS, Y_VALS = [0], [0]
CURSOR = turtle.Turtle()
SCREEN = turtle.getscreen()
PAUSED = True
BASE_SPEED = 2.5
SPEED = BASE_SPEED
SCORE = 0


# ================== movement =================
def add_point(x, y):
    X_VALS.append(round(x, 2))
    Y_VALS.append(round(y, 2))


def get_point(x, y):
    return (round(x, 2), round(y, 2))


def turn_right():
    # update the points
    add_point(*CURSOR.pos())
    # call the turn function
    CURSOR.right(90)


def turn_left():
    # update the points
    add_point(*CURSOR.pos())
    # call the turn function
    CURSOR.left(90)


def pause():
    global PAUSED
    PAUSED = not PAUSED


def boarder_collision_detected():
    x, y = get_point(*CURSOR.pos())
    if (abs(x) > (SCREEN.window_width()/2)) or (abs(y) > (SCREEN.window_height()/2)):
        return True


def does_intersect(x_vec: Vector, y_vec: Vector):
    # pick out latest segment
    x, y = get_point(*CURSOR.pos())
    x_last_vec = [x_vec[-1], x]
    y_last_vec = [y_vec[-1], y]

    # determine the x and y intersection values
    for i in range(len(x_vec) - 2):
        x_intersection = ((len(set(x_vec[i:i+2])) % 2) * x_vec[i]) + ((len(set(x_last_vec)) % 2) * x_last_vec[0])
        y_intersection = ((len(set(y_vec[i:i+2])) % 2) * y_vec[i]) + ((len(set(y_last_vec)) % 2) * y_last_vec[0])

        # determine if the intersection point is a part of both vectors
        if (((min(x_vec[i:i+2]) <= x_intersection <= max(x_vec[i:i+2])) and (min(x_last_vec) <= x_intersection <= max(x_last_vec))) and
            ((min(y_vec[i:i+2]) <= y_intersection <= max(y_vec[i:i+2])) and (min(y_last_vec) <= y_intersection <= max(y_last_vec)))):
            return True


def update_state():
    global SCORE, SPEED
    SCORE += SPEED
    SPEED = BASE_SPEED * ((floor(SCORE/1000)*0.5) + 1)
    turtle.title(f"{SCORE:.2f}")


def game_over():
    global PAUSED
    PAUSED = True
    SCREEN.bgcolor('red')
    pen = turtle.Turtle()
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 0)
    pen.write("Game Over", align="center", font=("Courier", 24, "normal"))


# =================== setup ===================
def setup():
    # set the title
    turtle.title("retro-line-crossing-game")
    # set up the key bindings
    SCREEN.onkey(turn_right, 'Right')
    SCREEN.onkey(turn_left, 'Left')
    SCREEN.onkey(pause, 'space')
    # begin listening
    SCREEN.listen()


# ================ game-loop ================
def main():
    # call the setup
    setup()
    # run the game loop
    while True:
        try:
            SCREEN.update()
            if not PAUSED:
                update_state()
                CURSOR.forward(SPEED)
                if boarder_collision_detected():
                    game_over()
                    break
                if does_intersect(X_VALS, Y_VALS):
                    game_over()
                    break
        except (TclError, turtle.Terminator):
            pass
    # write out the drawing for debugging purposes
    with open('log.csv', 'w') as f:
        add_point(*CURSOR.pos())
        [f.write(f'{x},{y}\n') for x, y in zip(X_VALS, Y_VALS)]
    print(SCORE)


if __name__ == "__main__":
    main()
