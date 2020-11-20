from gui import GUI,Colors
from states import State,History
import tkinter as tk
import numpy as np
import random
import copy

class Game:
    def __init__(self):
        self.history=History()
        self.colors=Colors()
        
        self.gui=GUI()
        self.start_game()

        self.gui.master.bind("<Left>", self.left)
        self.gui.master.bind("<Right>", self.right)
        self.gui.master.bind("<Up>", self.up)
        self.gui.master.bind("<Down>", self.down)
        self.gui.master.bind("a", self.left)
        self.gui.master.bind("d", self.right)
        self.gui.master.bind("w", self.up)
        self.gui.master.bind("s", self.down)

        self.gui.master.bind("r", self.restart)
        self.gui.master.bind("q", self.quit)

        self.gui.master.bind("z",self.undo)
        self.gui.master.bind("p",self.printall)
        self.gui.master.bind("i",self.z)
        self.gui.master.bind("e",self.look)

        self.gui.mainloop()

    def start_game(self):
        """
        Initialise game matrix and add 2 tiles of value 2 in the game grid.
        """
        self.matrix = [[0] * 4 for _ in range(4)]
        self.changeflag=False
        self.score=0
        self.add_new_tile(2)
        self.add_new_tile(2)
        self.gui.update_GUI(self.matrix,self.score)
        self.history.push(State(self.matrix,self.score),None)

    def stack(self):
        """
        Moves tiles towards left as far as possible without overriding another tile.
        >>> [4,0,2,0] becomes [4,2,0,0]
        >>> [0,2,2,0] becomes [2,2,0,0]
        """
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    if j!=fill_position:
                        self.changeflag=True
                        new_matrix[i][fill_position] = self.matrix[i][j]
                        fill_position += 1
                    else:
                        new_matrix[i][fill_position] = self.matrix[i][j]
                        fill_position += 1

        self.matrix = new_matrix

    def combine(self):
        """
        Make a Left move and combine all the tiles that can be combined in one move.
        >>> [4,2,2,0] becomes [4,4,0,0]
        Note that it does not combine the 4 and 4 further in the above example.
        >>> [2,2,4,0] becomes [4,0,4,0]
        """
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.changeflag=True
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1]=0
                    self.score += self.matrix[i][j]

    def reverse(self):
        """
        Mirrors the game grid across a vertical mirror. Used in implementing Right and Down moves.
        """
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix=new_matrix

    def transpose(self):
        """
        Mirrors the game grid across a horizontal mirror. Used in implementing Up and Down moves.
        """
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self, val=None):
        """
        Add a new tile in an empty cell of the grid.
        2 or 4 is added with probabilities of 0.9 and 0.1 respectively.

        Args:
            Val (Integer): If no value is specified, probabilites mentioned above are used. If value is specified, tile of that value is inserted.
        """
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        if val is None:
            self.matrix[row][col]=random.choices([2,4],weights=(90,10))[0]
        else:
            self.matrix[row][col]=val

    def left(self, event):
        """
        If left state of the current state does not exist, We make a left move.
        """
        if not (self.history.history[self.history.index-1][0].left is None):
            self.matrix=self.history.history[self.history.index-1][0].left.gamegrid
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].left.score
            self.history.push(self.history.history[self.history.index-1][0].left,"left")
            self.gui.update_GUI(self.matrix,self.score)
            # self.game_over()
            self.changeflag=False
            return
        self.stack()
        self.combine()
        if self.changeflag==True:
            self.stack()
            self.add_new_tile()
            self.history.history[self.history.index-1][0].left=State(self.matrix,self.score)
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.history.push(self.history.history[self.history.index-1][0].left,"left")
        self.gui.update_GUI(self.matrix,self.score)
        # self.game_over()
        self.changeflag=False

    def right(self, event):
        """
        If right state of the current state does not exist, We make a right move.
        """
        if not (self.history.history[self.history.index-1][0].right is None):
            self.matrix=self.history.history[self.history.index-1][0].right.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].right.score
            self.history.push(self.history.history[self.history.index-1][0].right,"right")
            self.gui.update_GUI(self.matrix,self.score)
            # self.game_over()
            self.changeflag=False
            return
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        if self.changeflag==True:
            self.add_new_tile()
            self.history.history[self.history.index-1][0].right=State(self.matrix,self.score)
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.history.push(self.history.history[self.history.index-1][0].right,"right")
        self.gui.update_GUI(self.matrix,self.score)
        # self.game_over()
        self.changeflag=False

    def up(self, event):
        """
        If up state of the current state does not exist, We make an up move.
        """
        if not (self.history.history[self.history.index-1][0].up is None):
            self.matrix=self.history.history[self.history.index-1][0].up.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].up.score
            self.history.push(self.history.history[self.history.index-1][0].up,"up")
            self.gui.update_GUI(self.matrix,self.score)
            # self.game_over()
            self.changeflag=False
            return
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        if self.changeflag==True:
            self.add_new_tile()
            self.history.history[self.history.index-1][0].up=State(self.matrix,self.score)
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].down=None
            self.history.push(self.history.history[self.history.index-1][0].up,"up")
        self.gui.update_GUI(self.matrix,self.score)
        # self.game_over()
        self.changeflag=False

    def down(self, event):
        """
        If down state of the current state does not exist, We make a down move.
        """
        if not (self.history.history[self.history.index-1][0].down is None):
            self.matrix=self.history.history[self.history.index-1][0].down.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.score=self.history.history[self.history.index-1][0].down.score
            self.history.push(self.history.history[self.history.index-1][0].down,"down")
            self.gui.update_GUI(self.matrix,self.score)
            # self.game_over()
            self.changeflag=False
            return
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        if self.changeflag==True:
            self.add_new_tile()
            self.history.history[self.history.index-1][0].down=State(self.matrix,self.score)
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.history.push(self.history.history[self.history.index-1][0].down,"down")
        self.gui.update_GUI(self.matrix,self.score)
        # self.game_over()
        self.changeflag=False

    # def horizontal_move_exits(self):
    #     """
    #     Check if tiles can be combined when moving left or right.
    #     """
    #     for i in range(4):
    #         for j in range(3):
    #             if self.matrix[i][j] == self.matrix[i][j+1]:
    #                 return True
    #     return False

    # def vertical_move_exits(self):
    #     """
    #     Check if tiles can be combined when moving up or down.
    #     """
    #     for i in range(3):
    #         for j in range(4):
    #             if self.matrix[i][j] == self.matrix[i+1][j]:
    #                 return True
    #     return False

    # def game_over(self):
    #     """
    #     Check if game is over by checking if the player has already won(if 2048 has been achieved) or if no moves can be made (No empty cells and no combinations possible).
    #     """
    #     if any(2048 in row for row in self.matrix):
    #         self.gui.game_over_maker("You win!")
    #         self.overflag=True
    #     elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exits() and not self.vertical_move_exits():
    #         self.gui.game_over_maker("Game Over!")
    #         self.overflag=False

    def restart(self,event):
        """
        Remake the GUI of the grid and reset all variables and score.
        """
        for x in self.gui.main_grid.winfo_children():
            x.destroy()
        self.gui.make_GUI()
        self.matrix = [[0] * 4 for _ in range(4)]
        self.changeflag=False
        self.score=0
        self.add_new_tile(2)
        self.add_new_tile(2)
        self.gui.update_GUI(self.matrix,self.score)
        self.history.delete()
        self.history.push(State(self.matrix,self.score),None)

    def undo(self,event):
        """
        Move current index of history back and change game grid to previous state.
        """
        if self.history.index>1:
            self.matrix, self.score=self.history.pop()
            self.gui.update_GUI(self.matrix,self.score)
        else:
            pass

    def look(self,event):
        """
        Compute future possibilities from current state upto a number of steps specified by the user.
        If user does not specify an input, 3 steps further are computed.
        """
        k=self.gui.popup()
        if k is None or k=="":
            k=3
        else:
            k=int(k)
        statelist=[self.history.history[self.history.index-1][0]]
        for i in range(k):
            templist=[]
            for j in statelist:
                j.checknext()
                if not j.left is None:
                    templist.append(j.left)
                if not j.right is None:
                    templist.append(j.right)
                if not j.up is None:
                    templist.append(j.up)
                if not j.down is None:
                    templist.append(j.down)
            statelist.clear()
            statelist.extend(templist)
            if len(templist)==0:
                print("No further moves possible")
                break
            for ind,st in enumerate(templist):
                if ind>63:
                    print("Limiting print to 64 values...")
                    break
                print("Level "+str(i+1)+" "+str(st))
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
        print("___________________________________")

    def printall(self,event):
        """
        Print History of grids upto current index.
        """
        for i in range(self.history.index):
            print(self.history.history[i])
        print("___________________________________")

    def z(self,event):
        """
        Print information about the state: the game grid, the maximum value of tiles in the grid and the sum of all the tiles.
        This function can be used by the agent to compute cost of the states that it gets using lookahead.
        """
        print("matrix:")
        for row in self.matrix:
            print(row)
        print("max value",np.max(self.matrix))
        res=sum(sum(x) for x in self.matrix)
        print("tilesum:",res)

    def quit(self,event):
        """
        Exit the game.
        """
        exit()

def main():
    Game()

if __name__ == "__main__":
    main()