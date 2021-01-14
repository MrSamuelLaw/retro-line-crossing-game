#!../.venv/Scripts/python.exe
from pathlib import PurePath
from os import chdir
from pytron import start_game_loop

if __name__ == "__main__":
    chdir(PurePath(__file__).parent)
    start_game_loop()

    # from cProfile import Profile
    # from pstats import Stats, SortKey
    # profiler = Profile()
    # profiler.runcall(main)
    # stats = Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats(SortKey.TIME)
    # stats.print_stats()
