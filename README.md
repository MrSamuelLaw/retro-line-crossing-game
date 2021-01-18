# retro-line-crossing-game
A game for teaching purposes that shows how to make a game where lines cannot intersect using turtle module.
Intended learning outcomes are:
* Learn to perform basic unit-tests.
* Learn to use test driven development to build algorithms from scratch.
* Learn basic object oriented programming concepts. 
* Apply basic object oriented programming concepts.

Setup:
1. Open __main__.pyw and create dictionary key bindings in the form of 
   p1_key_bindings = {"left_btn": <key to turn left>, "right_btn": <key to turn right>}
2. Put a list key bindings into the play_pytron function call.

   example:
   ```python
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
   ```
   
HOW TO PLAY:
1. Players will be setup right to left, with the right most player being player 1.
2. Press the space bar to begin the game, subsiquent presses pause/resume the game.
3. Use the key bindings specified during Setup to turn players.
