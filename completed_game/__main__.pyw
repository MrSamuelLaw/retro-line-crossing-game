#!../.venv/Scripts/pythonw.exe
from pathlib import PurePath
from os import chdir
from pytron import play_pytron

if __name__ == "__main__":
    chdir(PurePath(__file__).parent)

    # create key bindings
    p1_key_bindings = {'left_btn': 'Left', 'right_btn': 'Right'}
    p2_key_bindings = {'left_btn': 'a', 'right_btn': 'd'}

    # play the game
    while play_pytron([
        p1_key_bindings, p2_key_bindings,]):
        pass
