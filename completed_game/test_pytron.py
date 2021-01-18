#!../.venv/Scripts/python.exe
import unittest
from unittest.mock import Mock
from copy import copy
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

    # ============= unit tests =============
    def test_initial_state(self):
        p = self.player
        self.assertEqual(p.score, 0)
        self.assertEqual(p.distance_per_loop, Player.base_distance)
        self.assertEqual(len(p.x_vec), 0)
        self.assertEqual(len(p.y_vec), 0)
        self.assertIsNone(p.left_btn)
        self.assertIsNone(p.right_btn)
        self.assertEqual(p.movable, 1)

    def test_get_pos(self):
        """Test that the starting position
        is zero"""
        x, y = self.player.get_pos()
        self.assertEqual(x, 0.0)
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

    def test_turn_right(self):
        """Test that turn right
        works as expected"""
        self.player.turn_right()          # turn 90 deg right
        h = self.player.cursor.heading()  # angle in degrees
        self.assertEqual(h, 270)          # test to ensure point south

    def test_turn_left(self):
        """Test that turn left
        works as expected"""
        self.player.turn_left()           # turn 90 deg left
        h = self.player.cursor.heading()  # angle in degrees
        self.assertEqual(h, 90)           # test to ensure point north

    def test_move(self):
        """Test that the move function moves
        the player as expected"""
        self.player.move()                           # x += Player.base_speed, y += 0
        x, y = self.player.get_pos()                 # x = Player.base_speed, y = 0
        self.assertEqual(x, self.player.base_distance)  # x == Player.base_speed
        self.assertEqual(y, 0.00)                    # y == 0

    def test_update_score(self):
        self.assertEqual(self.player.score, 0)
        self.player.distance_per_loop = 50
        self.player.update_score()
        self.assertEqual(self.player.score, 50)

    def test_update_dist_per_loop(self):
        self.player.score = 1000            # (1000/1000)*0.5
        self.player.update_dist_per_loop()  # (1+0.5) * base_distance
        dpl = self.player.distance_per_loop
        self.assertEqual(dpl, 1.5*self.player.base_distance)

    def test_set_starting_position(self):
        """Test that the starting point is accurately recorded"""
        self.player.set_starting_pos(-5.0, 0.0)
        x, y = self.player.get_pos()
        self.assertEqual(x, -5.0)
        self.assertEqual(y, 0.0)

    # =========== integration tests ===========
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


class TestGame(unittest.TestCase):
    # ============= setup =============
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.root.withdraw()
        cls.canvas = Canvas(master=cls.root)

    def setUp(self):
        # create a player with a canvas that will not show up
        self.player = Player(canvas=self.canvas)
        self.game = Game(canvas=self.canvas)

    # ============= tests =============
    def test_initial_state(self):
        """Tests that the inital state
        of the game is correct."""
        self.assertTrue(self.game.paused)
        self.assertEqual(len(self.game.player_list), 0)

    def test_add_player(self):
        """Test to make sure players can be added"""
        player1 = copy(self.player)
        self.game.add_player(player1)
        self.assertEqual(len(self.game.player_list), 1)
        player2 = copy(self.player)
        self.game.add_player(player2)
        self.assertEqual(len(self.game.player_list), 2)

    def test_toggle_paused(self):
        """Test to make sure pause toggles true and
        false correctly."""
        self.game.toggle_pause()
        self.assertFalse(self.game.paused)
        self.game.toggle_pause()
        self.assertTrue(self.game.paused)

    def test_border_collision_detected(self):
        # create the screen mock methods
        screen = self.game.screen
        screen.window_width = Mock()
        screen.window_width.return_value = 100
        screen.window_height = screen.window_width
        # add the player to the game
        pos = self.player.get_pos
        self.game.add_player(self.player)
        # ========= + x-direction =========
        # test for non collision
        self.player.set_starting_pos(49, 0)
        self.assertFalse(self.game.boarder_collision_detected(*pos()))
        # test for "T" shaped collision
        self.player.set_starting_pos(50, 0)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # test for "+" shaped collision
        self.player.set_starting_pos(51, 0)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # ========= - x-direction =========
        # test for non collision
        self.player.set_starting_pos(-49, 0)
        self.assertFalse(self.game.boarder_collision_detected(*pos()))
        # test for "T" shaped collision
        self.player.set_starting_pos(-50, 0)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # test for "+" shaped collision
        self.player.set_starting_pos(-51, 0)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # ========= + y-direction =========
        # test for non collision
        self.player.set_starting_pos(0, 49)
        self.assertFalse(self.game.boarder_collision_detected(*pos()))
        # test for "T" shaped collision
        self.player.set_starting_pos(0, 50)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # test for "+" shaped collision
        self.player.set_starting_pos(0, 51)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # ========= - y-direction =========
        # test for non collision
        self.player.set_starting_pos(0, -49)
        self.assertFalse(self.game.boarder_collision_detected(*pos()))
        # test for "T" shaped collision
        self.player.set_starting_pos(0, -50)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))
        # test for "+" shaped collision
        self.player.set_starting_pos(0, -51)
        self.assertTrue(self.game.boarder_collision_detected(*pos()))

    def test_line_intersection_detected(self):
        # =========== vectors that do not intersect ===========
        x_vec, x_last_vec = [-1, 1], [0, 0]
        y_vec, y_last_vec = [0, 0], [2, 1]
        self.assertFalse(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        # =========== vectors that intersect at 0, 0 ==========
        x_vec, x_last_vec = [-1, 1], [0, 0]
        y_vec, y_last_vec = [0, 0], [-1, 1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        # =========== first quadrant intersections ==========
        #   "T" shaped intersection
        x_vec, x_last_vec = [0, 1, 1], [1, 2]
        y_vec, y_last_vec = [0, 0, 1], [1, 1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        #   "+" shaped intersection
        x_vec, x_last_vec = [0, 1, 1], [0, 2]
        y_vec, y_last_vec = [0, 0, 1], [1, 1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        # =========== second quadrant intersections ==========
        #   "T" shaped intersection
        x_vec, x_last_vec = [0, -1, -1], [-1, -2]
        y_vec, y_last_vec = [0, 0, 1], [1, 1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        #   "+" shaped intersection
        x_vec, x_last_vec = [0, -1, -1], [0, -2]
        y_vec, y_last_vec = [0, 0, 1], [1, 1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        # =========== third quadrant intersections ===========
        #   "T" shaped intersection
        x_vec, x_last_vec = [0, -1, -1], [-1, -2]
        y_vec, y_last_vec = [0, 0, -1], [-1, -1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        #   "+" shaped intersection
        x_vec, x_last_vec = [0, -1, -1], [0, -2]
        y_vec, y_last_vec = [0, 0, -1], [-1, -1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        # =========== fourth quadrant intersections ===========
        #   "T" shaped intersection
        x_vec, x_last_vec = [0, 1, 1], [1, 2]
        y_vec, y_last_vec = [0, 0, -1], [-1, -1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))
        #   "+" shaped intersection
        x_vec, x_last_vec = [0, 1, 1], [0, 2]
        y_vec, y_last_vec = [0, 0, -1], [-1, -1]
        self.assertTrue(
            self.game.line_intersection_detected(
                x_vec, y_vec, x_last_vec, y_last_vec))

    # =========== integration tests ===========
    def test_check_for_line_intersections(self):
        # ======== short setup ========
        #   create players with mock get_trace methods
        player1, player2 = copy(self.player), copy(self.player)
        player1.get_trace, player2.get_trace = Mock(), Mock()
        #   add players to game
        self.game.add_player(player1)
        self.game.add_player(player2)
        # ====== no intersection =======
        player1.get_trace.return_value = ([-1, 1], [0, 0])  # x axis trace
        player2.get_trace.return_value = ([0, 0], [1, 2])   # y axis trace
        self.game.check_for_line_intersections()
        self.assertEqual(player1.movable, 1)
        self.assertEqual(player2.movable, 1)
        # ==== player 2 runs into player1 ====
        player1.get_trace.return_value = ([-1, 1], [0, 0])  # x axis trace
        player2.get_trace.return_value = ([0, 0], [-1, 0])  # y axis trace
        self.game.check_for_line_intersections()
        self.assertEqual(player1.movable, 1)
        self.assertEqual(player2.movable, 0)


if __name__ == "__main__":
    unittest.main()