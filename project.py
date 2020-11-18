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
        self.matrix = [[0] * 4 for _ in range(4)]
        self.changeflag=False
        self.score=0
        self.add_new_tile(2)
        self.add_new_tile(2)
        self.gui.update_GUI(self.matrix,self.score)
        self.history.push(State(self.matrix,self.score),None)

    def stack(self):
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
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.changeflag=True
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1]=0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix=new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self, val=None):
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        if val is None:
            self.matrix[row][col]=random.choices([2,4],weights=(85,15))[0]
        else:
            self.matrix[row][col]=val

    def left(self, event):
        if not (self.history.history[self.history.index-1][0].left is None):
            self.matrix=self.history.history[self.history.index-1][0].left.gamegrid
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].left.score
            self.history.push(self.history.history[self.history.index-1][0].left,"left")
            self.gui.update_GUI(self.matrix,self.score)
            self.game_over()
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
        self.game_over()
        self.changeflag=False

    def right(self, event):
        if not (self.history.history[self.history.index-1][0].right is None):
            self.matrix=self.history.history[self.history.index-1][0].right.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].up=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].right.score
            self.history.push(self.history.history[self.history.index-1][0].right,"right")
            self.gui.update_GUI(self.matrix,self.score)
            self.game_over()
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
        self.game_over()
        self.changeflag=False

    def up(self, event):
        if not (self.history.history[self.history.index-1][0].up is None):
            self.matrix=self.history.history[self.history.index-1][0].up.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].down=None
            self.score=self.history.history[self.history.index-1][0].up.score
            self.history.push(self.history.history[self.history.index-1][0].up,"up")
            self.gui.update_GUI(self.matrix,self.score)
            self.game_over()
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
        self.game_over()
        self.changeflag=False

    def down(self, event):
        if not (self.history.history[self.history.index-1][0].down is None):
            self.matrix=self.history.history[self.history.index-1][0].down.gamegrid
            self.history.history[self.history.index-1][0].left=None
            self.history.history[self.history.index-1][0].right=None
            self.history.history[self.history.index-1][0].up=None
            self.score=self.history.history[self.history.index-1][0].down.score
            self.history.push(self.history.history[self.history.index-1][0].down,"down")
            self.gui.update_GUI(self.matrix,self.score)
            self.game_over()
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
        self.game_over()
        self.changeflag=False

    def horizontal_move_exits(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exits(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            self.gui.game_over_maker("You win!")
            self.overflag=True
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exits() and not self.vertical_move_exits():
            self.gui.game_over_maker("Game Over!")
            self.overflag=False

    def restart(self,event):
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
        if self.history.index>1:
            self.matrix, self.score=self.history.pop()
            self.gui.update_GUI(self.matrix,self.score)
        else:
            pass

    def look(self,event):
        k=self.gui.popup()
        if k is None or k=="":
            k=3
        else:
            k=int(k)
        statelist=[self.history.history[-1][0]]
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
            for ind,st in enumerate(templist):
                if ind>63:
                    print("Limiting print to 64 values...")
                    break
                print("Level "+str(i+1)+" "+str(st))
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
        print("___________________________________")

    def printall(self,event):
        for i in range(self.history.index):
            print(self.history.history[i])
        print("___________________________________")

    def z(self,event):
        print("matrix:")
        for row in self.matrix:
            print(row)
        print("max value",np.max(self.matrix))
        res=sum(sum(x) for x in self.matrix)
        print("tilesum:",res)

    def quit(self,event):
        exit()

def main():
    Game()

if __name__ == "__main__":
    main()