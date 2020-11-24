# POPL
2048 Game for CSF301 

## To use agent, run main.py inside Test folder

### File Structure

    /main.py    "Main Game Code"
    
    /gui.py     "Define GUI elements"

    /states.py  "Define History and State Node structure"

### Actions

- W,A,S,D or Arrow Keys to move up, left, down, right
- R to restart game
- Q to quit game
- Z to undo an action
- E to lookahead into future possibilities
- P to print entire history upto current state
- I to print state information

### Implementation Details

##### Moves
- Stack, Reverse, Transpose and Combine operations are used to calculate Left, Right, Up and Down moves.
- A new tile is randomly added from 2,4 with the probability of 0.9,0.1 respectively.
- Game over condition is checked for whether a tile of 2048 exists or if there are no possible moves.

##### State
- State Nodes store the grid of the current position, the score at this state and the Left, Right, Up and Down States achievable from here ( These are initially all None )

##### History
- History is a list that stores the States.
- In going back and forth, we just move the index of the list that we are at backward and forward if we do not change moves.

##### LookAhead
- When lookahead is implemented, State's Left Right Up Down States are made and then the Further States to these are made up to a level mentioned by user, or 3 if not specified.
- If the user now makes a move, say Left, the other 3 are destroyed and those subtrees are now deleted.
- If the user goes back, this 4-ary tree remains and will not have to be computed again if lookahead is called again.

##### Undo
- If the user goes back to a previous state, assume this state was achieved by making a Left move from said previous state. State.Left is made to be this state that we came from so that it is not recomputed if we make a Left move again now.
- If the user makes a different move now after going back, all other 3 move states are destroyed and we no longer have that path available.

