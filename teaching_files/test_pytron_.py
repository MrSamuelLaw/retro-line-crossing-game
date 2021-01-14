#!../.venv/Scripts/python.exe

import unittest
from os import chdir
from pathlib import PurePath
from tkinter import Tk, Canvas
from pytron_1_22_2021 import Player, Game


class TestPlayer(unittest.TestCase):
    # ============= setup =============
    @classmethod
    def setUpClass(cls):
        """This code runs before ALL of our tests
        it's primary purpose is to prevent the window
        from popping up every time we run out unit
        tests."""
        cls.root = Tk()
        cls.root.withdraw()
        cls.canvas = Canvas(master=cls.root)

    def setUp(self):
        """This code runs before EACH of our tests"""
        self.player = Player()

    def test_can_fail(self):
        """This failing unit test ensures everything is
        running correctly"""
        self.assertTrue(True)

    # ============== your code starts here ==============

    # ============== your code ends here   ==============


class TestGame(unittest.TestCase):
    # ============= setup =============
    @classmethod
    def setUpClass(cls):
        """This code runs before ALL of our tests
        it's primary purpose is to prevent the window
        from popping up every time we run out unit
        tests."""
        cls.root = Tk()
        cls.root.withdraw()
        cls.canvas = Canvas(master=cls.root)

    def setUp(self):
        """This code runs before EACH of our tests"""
        self.game = Game()

    def test_can_fail(self):
        """This failing unit test ensures everything is
        running correctly"""
        self.assertTrue(True)

    # ============== your code starts here ==============

    # ============== your code ends here   ==============


if __name__ == "__main__":
    chdir(PurePath(__file__).parent)
    unittest.main()