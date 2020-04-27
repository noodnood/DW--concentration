# [DW-concentration ](https://github.com/noodnood/DW-concentration)
A simple python implementation of the card game Concentration!

### How to play
There are 52  playing cards in a 4x13 layout.
The goal of the game is to turn over pairs of cards with matching ranks.

If you feel that you are spending too much time trying to complete the game, you can enter "end" when selecting a card to activate the self-solver.


#### ``class card``
Has a rank and suit



#### ``class deck``
Class that initiates the deck of 52 playing cards

- ##### ``__init__()``
    Initializes the 52 playing cards
- ##### ``deckGrid()``
    returns a 4x13 numpy array which represents the layout of the 52 playing cards
- ##### ``shuffle()``
    Uses random.shuffle() function to shuffle the deck of cards
- ##### ``show()``
    prints the deck, used for testing purposes


#### ``class Board``
Class to store player variables. Inherits ``bjsm``.

- ##### ``__init__()``
    Initialises the variables required for this class.
    This class is what the player will see on their screen

- ##### ``progress()``
    Updates the player's screen with the game progress
- ##### ``build()``
    Updates the board behind the scenes, translates to flipping of the selected pair on the board
- ##### ``create()``
    Initializes the initial board, only runs once

#### ``class Coordinate``
The input selected by the player, represents which card the player wants to flip

##### ``class game()``
The main class

