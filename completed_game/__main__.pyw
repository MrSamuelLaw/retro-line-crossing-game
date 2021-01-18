#!../.venv/Scripts/pythonw.exe
from pathlib import PurePath
from os import chdir
from pytron import play_pytron

if __name__ == "__main__":
    chdir(PurePath(__file__).parent)

    # create key bindings
    p1_key_bindings = {'left_btn': 'Left', 'right_btn': 'Right'}
    p2_key_bindings = {'left_btn': 'j', 'right_btn': 'l'}
    p3_key_bindings = {'left_btn': 'a', 'right_btn': 'd'}
    p4_key_bindings = {'left_btn': '1', 'right_btn': '2'}

    # play the game
    while play_pytron([
        p1_key_bindings, p2_key_bindings,
        p3_key_bindings, p4_key_bindings,]):
        pass
