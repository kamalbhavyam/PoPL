import tkinter as tk
import numpy as np
import random
import copy

class State:
    """
    Define a Node to store the game grid, score, and next achievable states for a particular state.

    Args:
        matrix (2D list): Game Grid
        score (int): Score at current state
        tilesum (int): Sum of non-empty tiles at current state
    """
    def __init__(self,matrix,score,tilesum):
        self.gamegrid=matrix
        self.left,self.right,self.up,self.down=None,None,None,None
        self.score=score
        self.tilesum=tilesum
    
    def __repr__(self):
        # return 'Game grid '+str(self.gamegrid)+' Score:'+str(self.score)+' Tilesum:'+str(self.tilesum)
        return str(self.gamegrid)
    
    def __str__(self):
        return str(self.gamegrid)

    def __eq__(self,other):
        return self.gamegrid==other.gamegrid

    def stack(self,matrix):
        """
        Moves tiles towards left as far as possible without overriding another tile.
        >>> [4,0,2,0] becomes [4,2,0,0]
        >>> [0,2,2,0] becomes [2,2,0,0]

        Args:
            matrix (2D List): Game grid

        Returns:
            matrix (2D List): New changed matrix
        """
        changeflag=False
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if matrix[i][j] != 0:
                    if j!=fill_position:
                        changeflag=True
                        new_matrix[i][fill_position] = matrix[i][j]
                        fill_position += 1
                    else:
                        new_matrix[i][fill_position] = matrix[i][j]
                        fill_position += 1
        return new_matrix,changeflag

    def combine(self,matrix,score):
        """
        Make a Left move and combine all the tiles that can be combined in one move.
        >>> [4,2,2,0] becomes [4,4,0,0]
        Note that it does not combine the 4 and 4 further in the above example.
        >>> [2,2,4,0] becomes [4,0,4,0]

        Args:
            matrix (2D List): Game grid
            score (int): Score for current Game state

        Returns:
            matrix (2D List): New changed matrix
        """
        changeflag=False
        new_matrix=matrix.copy()
        score_new=score
        for i in range(4):
            for j in range(3):
                if new_matrix[i][j] != 0 and new_matrix[i][j] == new_matrix[i][j+1]:
                    changeflag=True
                    new_matrix[i][j] *= 2
                    new_matrix[i][j+1]=0
                    score_new+=matrix[i][j]
        return new_matrix,score_new,changeflag

    def reverse(self,matrix):
        """
        Mirrors the game grid across a vertical mirror. Used in implementing Right and Down moves.

        Args:
            matrix (2D List): Game grid

        Returns:
            matrix (2D List): New changed matrix
        """
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(matrix[i][3-j])
        return new_matrix

    def transpose(self,matrix):
        """
        Mirrors the game grid across a horizontal mirror. Used in implementing Up and Down moves.

        Args:
            matrix (2D List): Game grid

        Returns:
            matrix (2D List): New changed matrix
        """
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = matrix[j][i]
        return new_matrix

    def add_new_tile(self, matrix,tilesum, val=None):
        """
        Add a new tile in an empty cell of the grid.
        2 or 4 is added with probabilities of 0.9 and 0.1 respectively.

        Args:
            matrix (2D List): Game grid
            Val (Integer): If no value is specified, probabilites mentioned above are used. If value is specified, tile of that value is inserted.
            tilesum (Integer): Sum of all tiles before random tile insertion

        Returns:
            matrix (2D List): New changed matrix
        """
        new_matrix=matrix.copy()
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(new_matrix[row][col] != 0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        if val is None:
            new_matrix[row][col]=random.choices([2,4],weights=(90,10))[0]
            tilesum+=new_matrix[row][col]
        else:
            new_matrix[row][col]=val
            tilesum+=new_matrix[row][col]
        return new_matrix,tilesum

    def horizontal_move_exits_look(self,matrix):
        """
        Check if tiles can be combined when moving left or right.

        Args:
            matrix (2D List): Game grid
        """
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exits_look(self,matrix):
        """
        Check if tiles can be combined when moving up or down.

        Args:
            matrix (2D List): Game grid
        """
        for i in range(3):
            for j in range(4):
                if matrix[i][j] == matrix[i+1][j]:
                    return True
        return False

    def game_over_look(self,matrix):
        """
        Check if game is over by checking if the player has already won(if 2048 has been achieved) or if no moves can be made (No empty cells and no combinations possible).

        Args:
            matrix (2D List): Game grid
        """
        if any(2048 in row for row in matrix):
            return 0
        elif not any(0 in row for row in matrix) and not self.horizontal_move_exits_look(matrix) and not self.vertical_move_exits_look(matrix):
            return 1
        return 2

    def moveleft(self):
        """
        If left state of the current state does not exist, We make a left move.
        """
        if not self.left is None:
            return
        self.left=State(self.gamegrid,self.score,self.tilesum)
        self.left.gamegrid,tempflagstack=self.stack(self.gamegrid)
        self.left.gamegrid,self.left.score,tempflagcombine=self.combine(self.left.gamegrid,self.score)
        self.left.gamegrid,_=self.stack(self.left.gamegrid)
        if tempflagstack or tempflagcombine:
            self.left.gamegrid,self.left.tilesum=self.add_new_tile(self.left.gamegrid,self.left.tilesum)
        else:
            self.left=None
            return
        if self.game_over_look(self.left.gamegrid)==1:
            self.left=None

    def moveright(self):
        """
        If right state of the current state does not exist, We make a right move.
        """
        if not self.right is None:
            return
        self.right=State(self.gamegrid,self.score,self.tilesum)
        self.right.gamegrid=self.reverse(self.gamegrid)
        self.right.gamegrid,tempflagstack=self.stack(self.right.gamegrid)
        self.right.gamegrid,self.right.score,tempflagcombine=self.combine(self.right.gamegrid,self.score)
        self.right.gamegrid,_=self.stack(self.right.gamegrid)
        self.right.gamegrid=self.reverse(self.right.gamegrid)
        if tempflagstack or tempflagcombine:
            self.right.gamegrid,self.right.tilesum=self.add_new_tile(self.right.gamegrid,self.right.tilesum)
        else:
            self.right=None
            return
        if self.game_over_look(self.right.gamegrid)==1:
            self.right=None

    def moveup(self):
        """
        If up state of the current state does not exist, We make an up move.
        """
        if not self.up is None:
            return
        self.up=State(self.gamegrid,self.score,self.tilesum)
        self.up.gamegrid=self.transpose(self.gamegrid)
        self.up.gamegrid,tempflagstack=self.stack(self.up.gamegrid)
        self.up.gamegrid,self.up.score,tempflagcombine=self.combine(self.up.gamegrid,self.score)
        self.up.gamegrid,_=self.stack(self.up.gamegrid)
        self.up.gamegrid=self.transpose(self.up.gamegrid)
        if tempflagstack or tempflagcombine:
            self.up.gamegrid,self.up.tilesum=self.add_new_tile(self.up.gamegrid,self.up.tilesum)
        else:
            self.up=None
            return
        if self.game_over_look(self.up.gamegrid)==1:
            self.up=None

    def movedown(self):
        """
        If down state of the current state does not exist, We make a down move.
        """
        if not self.down is None:
            return
        self.down=State(self.gamegrid,self.score,self.tilesum)
        self.down.gamegrid=self.transpose(self.gamegrid)
        self.down.gamegrid=self.reverse(self.down.gamegrid)
        self.down.gamegrid,tempflagstack=self.stack(self.down.gamegrid)
        self.down.gamegrid,self.down.score,tempflagcombine=self.combine(self.down.gamegrid,self.score)
        self.down.gamegrid,_=self.stack(self.down.gamegrid)
        self.down.gamegrid=self.reverse(self.down.gamegrid)
        self.down.gamegrid=self.transpose(self.down.gamegrid)
        if tempflagstack or tempflagcombine:
            self.down.gamegrid,self.down.tilesum=self.add_new_tile(self.down.gamegrid,self.down.tilesum)
        else:
            self.down=None
            return
        if self.game_over_look(self.down.gamegrid)==1:
            self.down=None

    def checknext(self):
        """
        Check if a gameover state is reached. If not, make the next 4 direction states.
        """
        if self.game_over_look(self.gamegrid)==0:
            return
        self.moveleft()
        self.moveright()
        self.moveup()
        self.movedown()

    def getemptycells(self):
        """
        Get a list of empty cells.

        Returns:
            (List) List of indices of empty cells.
        """
        return [(x,y) for x in range(4) for y in range(4) if self.gamegrid[x][y]==0]

    def destroychildren(self):
        """
        Destroy children of children to maintain memory.
        """
        if self.left is None:
            pass
        else:
            self.left.left=None
            self.left.right=None
            self.left.up=None
            self.left.down=None
        if self.right is None:
            pass
        else:
            self.right.left=None
            self.right.right=None
            self.right.up=None
            self.right.down=None
        if self.up is None:
            pass
        else:
            self.up.left=None
            self.up.right=None
            self.up.up=None
            self.up.down=None
        if self.down is None:
            pass
        else:
            self.down.left=None
            self.down.right=None
            self.down.up=None
            self.down.down=None
        
    def insert_tile(self,pos,value):
        """
        Insert tile at a given position.
        
        Args:
            pos (tuple<int,int>): (x,y) position.
            value (int): The value to be inserted.
        """
        self.gamegrid[pos[0]][pos[1]]=value

    def get_available_from_zeros(self,a):
        """
        See if a shift operation can be made in the gamegrid.

        Args:
            a (2D list): Gamegrid
        """
        uc, dc, lc, rc = False, False, False, False

        v_saw_0 = [False, False, False, False]
        v_saw_1 = [False, False, False, False]

        for i in [0,1,2,3]:
            saw_0 = False
            saw_1 = False

            for j in [0,1,2,3]:

                if a[i][j] == 0:
                    saw_0 = True
                    v_saw_0[j] = True

                    if saw_1:
                        rc = True
                    if v_saw_1[j]:
                        dc = True

                if a[i][j] > 0:
                    saw_1 = True
                    v_saw_1[j] = True

                    if saw_0:
                        lc = True
                    if v_saw_0[j]:
                        uc = True

        return [uc, dc, lc, rc]

    def getavailablemoves(self):
        """
        Get a list of possible moves at a given State.

        Returns:
        available_moves (list of tuple<int,int>): List of available moves for a given state.
        """
        available_moves=[]

        a1 = self.get_available_from_zeros(self.gamegrid)

        for x in range(4):
            if not a1[x]:
                board_clone=copy.deepcopy(self)

                if x==0:
                    board_clone.moveleft()
                    if not board_clone.left is None:
                        available_moves.append(x)
                elif x==1:
                    board_clone.moveright()
                    if not board_clone.right is None:
                        available_moves.append(x)
                elif x==2:
                    board_clone.moveup()
                    if not board_clone.up is None:
                        available_moves.append(x)
                elif x==3:
                    board_clone.movedown()
                    if not board_clone.down is None:
                        available_moves.append(x)
            else:
                available_moves.append(x)
        return available_moves

class History:
    """
    History Object that is a list that stores State objects
    """
    def __init__(self):
        self.index=0
        self.history=[]
        self.history.clear()
    
    def __repr__(self):
        return str(self.history)

    def printall(self):
        """
        Print all elements of history to console.
        """
        for x in self.history:
            print(x[0],x[0].tilesum)

    def push(self,state,direction):
        """
        Move the index forward and add state to history.
        If index is not equal to the length of the history list, check if direction being put in is same as the one of next state. If direction is different, then delete the history list ahead and append this state.

        Args:
            state (2D Matrix): Game grid
            direction (string): Direction move that was just made
        """
        if len(self.history)==self.index:
            self.history.append((state,direction))
        else:
            if self.history[self.index][1]==direction:
                if direction=='down':
                    if self.history[self.index-1][0].down is None:
                        del self.history[self.index:]
                        self.history.append((state,direction))
                elif direction=='up':
                    if self.history[self.index-1][0].up is None:
                        del self.history[self.index:]
                        self.history.append((state,direction))
                elif direction=='right':
                    if self.history[self.index-1][0].right is None:
                        del self.history[self.index:]
                        self.history.append((state,direction))
                elif direction=='left':
                    if self.history[self.index-1][0].left is None:
                        del self.history[self.index:]
                        self.history.append((state,direction))
                pass
            else:
                del self.history[self.index:]
                self.history.append((state,direction))
        self.index+=1
    
    def delete(self):
        """
        Clear the history list. Used for restart.
        """
        self.history=[]
        self.index=0
    
    def pop(self):
        """
        Move the current index back by 1.

        Returns:
            Game grid (2D Matrix): The 2D matrix of the previous state.
        """
        self.index-=1
        return self.history[self.index-1][0].gamegrid, self.history[self.index-1][0].score, self.history[self.index-1][0].tilesum

