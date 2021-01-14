#!.venv/Scripts/python.exe
import unittest
from turtle import RawTurtle
from tkinter import Tk, Canvas
from pytron import Player, Game


class TestPlayer(unittest.TestCase):
    # ============= setup =============
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.root.withdraw()
        cls.canvas = Canvas(master=cls.root)

    def setUp(self):
        # create a player with a canvas that will not show up
        self.player = Player(canvas=self.canvas)

    # ============= tests =============
    def test_get_pos(self):
        """Test that the starting position
        is zero"""
        x, y = self.player.get_pos()
        self.assertEqual(x, 0.0)
        self.assertEqual(y, 0.0)

    def test_move(self):
        """Test that the move function moves
        the player as expected"""
        self.player.move()                           # x += Player.base_speed, y += 0
        x, y = self.player.get_pos()                 # x = Player.base_speed, y = 0
        self.assertEqual(x, self.player.base_distance)  # x == Player.base_speed
        self.assertEqual(y, 0.00)                    # y == 0

    def test_turn(self):
        """Test that the move function moves
        the player as expected"""
        h = self.player.cursor.heading()  # angle in degrees
        self.assertEqual(h, 0)            # test to ensure zero
        self.player.turn_left()           # turn 90 left
        h = self.player.cursor.heading()  # angle in degrees
        self.assertEqual(h, 90)           # test to ensure point north

    def test_move_and_turn(self):
        """Test that move and turn work in tandem"""
        self.player.move()       # go forward by player.base_speed
        self.player.turn_left()  # point north
        self.player.move()       # go forward by player.base_speed
        x, y = self.player.get_pos()      # x should equal to y
        h = self.player.cursor.heading()  # heading should be 90
        self.assertEqual(x, self.player.base_distance)
        self.assertEqual(x, y)
        self.assertEqual(h, 90)

    def test_set_starting_position(self):
        """Test that the starting point is accurately recorded"""
        self.player.set_starting_pos(-5.0, 0.0)
        x, y = self.player.get_pos()
        self.assertEqual(x, -5.0)
        self.assertEqual(y, 0.0)

    def test_update_trace(self):
        """Test that the trace is updated on turns"""
        self.player.set_starting_pos()
        self.player.move()
        self.player.update_trace()
        self.assertEqual(self.player.x_vec, [0.0, self.player.base_distance])
        self.assertEqual(self.player.y_vec, [0.0, 0.0])

    def test_get_trace(self):
        """Test that the trace is accurate"""
        self.player.set_starting_pos()
        x_vec, y_vec = self.player.get_trace()
        self.assertEqual(x_vec, [0])
        self.assertEqual(y_vec, [0])
        self.player.move()
        x_vec, y_vec = self.player.get_trace()
        self.assertEqual(x_vec, [0, self.player.base_distance])
        self.assertEqual(y_vec, [0, 0])

    def test_update_score(self):
        self.assertEqual(self.player.score, 0)
        self.player.distance_per_loop = 50
        self.player.update_score()
        self.assertEqual(self.player.score, 50)





if __name__ == "__main__":
    unittest.main()