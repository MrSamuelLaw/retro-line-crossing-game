#!../.venv/Scripts/pythonw.exe
from pathlib import PurePath
from os import chdir
from pytron import play_pytron

if __name__ == "__main__":
    chdir(PurePath(__file__).parent)
    while play_pytron(number_of_players=2):
        pass

    # from cProfile import Profile
    # from pstats import Stats, SortKey
    # profiler = Profile()
    # profiler.runcall(main)
    # stats = Stats(profiler)
    # stats.strip_dirs()
    # stats.sort_stats(SortKey.TIME)
    # stats.print_stats()
