from gui import GUI,Colors
from states import State,History
from ai import AI
import tkinter as tk
import numpy as np
import random
import copy
import time

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

        self.gui.master.bind("f",self.agent)

        # self.gui.mainloop()

    def start_game(self):
        """
        Initialise game matrix and add 2 tiles of value 2 in the game grid.
        """
        self.matrix = [[0] * 4 for _ in range(4)]
        self.changeflag=False
        self.ai=AI()
        self.score=0
        self.tilesum=0
        self.agentgameover=False
        self.add_new_tile()
        self.add_new_tile()
        self.gui.update_GUI(self.matrix,self.score)
        self.history.push(State(self.matrix,self.score,self.tilesum),None)

    def stack(self):
        """
        Moves tiles towards left as far as possible without overriding another tile.
        >>> [4,0,2,0] becomes [4,2,0,0]
        >>> [0,2,2,0] becomes [2,2,0,0]
        >>> [2,0,2,0] becomes [2,2,0,0]
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
            self.tilesum+=self.matrix[row][col]
        else:
            self.matrix[row][col]=val
            self.tilesum+=self.matrix[row][col]

    def left(self, event):
        """
        If left state of the current state does not exist, We make a left move.
        """
        if not (self.history.history[self.history.index-1][0].left is None):
            self.matrix=self.history.history[self.history.index-1][0].left.gamegrid
            self.history.history[self.history.index-1][0].destroychildren()
            self.score=self.history.history[self.history.index-1][0].left.score
            self.tilesum=self.history.history[self.history.index-1][0].left.tilesum
            self.history.push(self.history.history[self.history.index-1][0].left,"left")
            self.gui.update_GUI(self.matrix,self.score)
            self.changeflag=False
            return
        self.stack()
        self.combine()
        if self.changeflag==True:
            self.stack()
            self.add_new_tile()
            self.history.history[self.history.index-1][0].left=State(self.matrix,self.score,self.tilesum)
            self.history.history[self.history.index-1][0].destroychildren()
            self.history.push(self.history.history[self.history.index-1][0].left,"left")
        self.gui.update_GUI(self.matrix,self.score)
        self.changeflag=False

    def right(self, event):
        """
        If right state of the current state does not exist, We make a right move.
        """
        if not (self.history.history[self.history.index-1][0].right is None):
            self.matrix=self.history.history[self.history.index-1][0].right.gamegrid
            self.history.history[self.history.index-1][0].destroychildren()
            self.score=self.history.history[self.history.index-1][0].right.score
            self.tilesum=self.history.history[self.history.index-1][0].right.tilesum
            self.history.push(self.history.history[self.history.index-1][0].right,"right")
            self.gui.update_GUI(self.matrix,self.score)
            self.changeflag=False
            return
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        if self.changeflag==True:
            self.add_new_tile()
            self.history.history[self.history.index-1][0].right=State(self.matrix,self.score,self.tilesum)
            self.history.history[self.history.index-1][0].destroychildren()
            self.history.push(self.history.history[self.history.index-1][0].right,"right")
        self.gui.update_GUI(self.matrix,self.score)
        self.changeflag=False

    def up(self, event):
        """
        If up state of the current state does not exist, We make an up move.
        """
        if not (self.history.history[self.history.index-1][0].up is None):
            self.matrix=self.history.history[self.history.index-1][0].up.gamegrid
            self.history.history[self.history.index-1][0].destroychildren()
            self.score=self.history.history[self.history.index-1][0].up.score
            self.tilesum=self.history.history[self.history.index-1][0].up.tilesum
            self.history.push(self.history.history[self.history.index-1][0].up,"up")
            self.gui.update_GUI(self.matrix,self.score)
            self.changeflag=False
            return
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        if self.changeflag==True:
            self.add_new_tile()
            self.history.history[self.history.index-1][0].up=State(self.matrix,self.score,self.tilesum)
            self.history.history[self.history.index-1][0].destroychildren()
            self.history.push(self.history.history[self.history.index-1][0].up,"up")
        self.gui.update_GUI(self.matrix,self.score)
        self.changeflag=False

    def down(self, event):
        """
        If down state of the current state does not exist, We make a down move.
        """
        if not (self.history.history[self.history.index-1][0].down is None):
            self.matrix=self.history.history[self.history.index-1][0].down.gamegrid
            self.history.history[self.history.index-1][0].destroychildren()
            self.score=self.history.history[self.history.index-1][0].down.score
            self.tilesum=self.history.history[self.history.index-1][0].down.tilesum
            self.history.push(self.history.history[self.history.index-1][0].down,"down")
            self.gui.update_GUI(self.matrix,self.score)
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
            self.history.history[self.history.index-1][0].down=State(self.matrix,self.score,self.tilesum)
            self.history.history[self.history.index-1][0].destroychildren()
            self.history.push(self.history.history[self.history.index-1][0].down,"down")
        self.gui.update_GUI(self.matrix,self.score)
        self.changeflag=False

    def horizontal_move_exits(self,matrix):
        """
        Check if tiles can be combined when moving left or right.
        """
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exits(self,matrix):
        """
        Check if tiles can be combined when moving up or down.
        """
        for i in range(3):
            for j in range(4):
                if matrix[i][j] == matrix[i+1][j]:
                    return True
        return False

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
        self.history.push(State(self.matrix,self.score,self.tilesum),None)

    def undo(self,event):
        """
        Move current index of history back and change game grid to previous state.
        """
        if self.history.index>1:
            self.matrix, self.score, self.tilesum=self.history.pop()
            self.gui.update_GUI(self.matrix,self.score)
        else:
            pass

    def look(self,event):
        """
        Compute future possibilities from current state upto a number of steps specified by the user.
        If user does not specify an input, 3 steps further are computed.
        Prints Moves along with the states they achieve.
        """
        k=self.gui.popup()
        if k is None or k=="":
            k=3
        else:
            k=int(k)
        statelist=[("",self.history.history[self.history.index-1][0])]
        for i in range(k):
            templist=[]
            for j in statelist:
                curmove=j[0]
                j[1].checknext()
                if not j[1].left is None:
                    templist.append((curmove+"->Left",j[1].left))
                if not j[1].right is None:
                    templist.append((curmove+"->Right",j[1].right))
                if not j[1].up is None:
                    templist.append((curmove+"->Up",j[1].up))
                if not j[1].down is None:
                    templist.append((curmove+"->Down",j[1].down))
            statelist.clear()
            statelist.extend(templist)
            if len(templist)==0:
                print("No further moves possible")
                break
            for ind,st in enumerate(templist):
                if ind>63:
                    print("Limiting print to 64 values...")
                    break
                print("Level "+str(i+1)+" "+st[0]+" "+str(st[1]))
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
        return res
    
    def getemptycells(self):
        emptycellcount=0
        for row in self.matrix:
            for elem in row:
                if elem==0:
                    emptycellcount+=1
        return emptycellcount

    def agenteventmaker(self):
        """
        Helper function to make GUI run smoothly and make a while loop in agent
        """
        self.gui.event_generate("f")

    def agent(self,event):
        """
        Agent that uses expectimax to play and get to highest tile ( 2048 in 95% cases, 1024 in the rest till now)
        """
        if self.gui.overflag==False:
            mv=self.ai.getmove(self.history.history[self.history.index-1][0])
            if mv is None:
                return
            if mv==0:
                print("Agent makes a left move")
                self.gui.event_generate("a")
            elif mv==1:
                print("Agent makes a right move")
                self.gui.event_generate("d")
            elif mv==2:
                print("Agent makes a up move")
                self.gui.event_generate("w")
            elif mv==3:
                print("Agent makes a down move")
                self.gui.event_generate("s")
            self.gui.after(50,self.agenteventmaker)

    def quit(self,event):
        """
        Exit the game.
        """
        exit()