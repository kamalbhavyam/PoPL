from game import Game
from states import State,History
import random
import time

agenthistory=History()
visited=None

def childlist(gameObject):
    """
    Make list of possible children using actions that are possible from this state.

    Args:
        gameObject (State Object): Game State
    Returns:
        ls (List): Possible next states
    """
    ls=[]
    gameObject.checknext()
    if not gameObject.left is None:
        ls.append(gameObject.left)
    if not gameObject.right is None:
        ls.append(gameObject.right)
    if not gameObject.up is None:
        ls.append(gameObject.up)
    if not gameObject.down is None:
        ls.append(gameObject.down)
    return ls

def eventmaker(visited,gameObject):
    """
    DFS style search for a tilesum equating to value 8

    Args:
        visited (List): set of visited states.
        gameObject (State Object): current game state.
    """
    if visited is None:
        visited = []

    visited.append(gameObject)
    agenthistory.push(gameObject,None)

    if gameObject.tilesum>8:
        return -1
    if gameObject.tilesum==8:
        print("queue:")
        agenthistory.printall()
        return 1

    for elem in childlist(gameObject):
        if elem not in visited:
            val=eventmaker(visited,elem)
            if val==1:
                return 1
            elif val==-1:
                agenthistory.push(gameObject,None)

def main():
    gameObject=Game()
    gameObject.gui.after(200,eventmaker,visited,State(gameObject.matrix,gameObject.score,gameObject.tilesum))
    gameObject.gui.mainloop()

if __name__ == "__main__":
    main()