import tkinter as tk
import numpy as np
import random
import copy

class State:
    def __init__(self,matrix,score):
        self.gamegrid=matrix
        self.left,self.right,self.up,self.down=None,None,None,None
        self.score=score
    
    def __repr__(self):
        # return 'Game grid '+str(self.gamegrid)+' Score:'+str(self.score)+' Left: '+str(self.left)+' Right: '+str(self.right)+' Up: '+str(self.up)+' Down: '+str(self.down)
        return 'Game grid '+str(self.gamegrid)+' Score:'+str(self.score)
        # ' Left: '+(str(self.left.gamegrid) if (not self.left is None) else "NA,") \
        # +' Right: '+(str(self.right.gamegrid) if (not self.right is None) else "NA") \
        # +' Up: '+(str(self.up.gamegrid) if (not self.up is None) else "NA") \
        # +' Down: '+(str(self.down.gamegrid) if (not self.down is None) else "NA")
    
    def __str__(self):
        return str(self.gamegrid)

    def stack(self,matrix):
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
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(matrix[i][3-j])
        return new_matrix

    def transpose(self,matrix):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = matrix[j][i]
        return new_matrix

    def add_new_tile(self, matrix, val=None):
        new_matrix=matrix.copy()
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(new_matrix[row][col] != 0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        if val is None:
            new_matrix[row][col]=random.choices([2,4],weights=(85,15))[0]
        else:
            new_matrix[row][col]=val
        return new_matrix

    def horizontal_move_exits_look(self,matrix):
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exits_look(self,matrix):
        for i in range(3):
            for j in range(4):
                if matrix[i][j] == matrix[i+1][j]:
                    return True
        return False

    def game_over_look(self,matrix):
        if any(2048 in row for row in matrix):
            return 0
        elif not any(0 in row for row in matrix) and not self.horizontal_move_exits_look(matrix) and not self.vertical_move_exits_look(matrix):
            return 1
        return 2

    def moveleft(self):
        if not self.left is None:
            return
        self.left=State(self.gamegrid,self.score)
        self.left.gamegrid,tempflagstack=self.stack(self.gamegrid)
        self.left.gamegrid,self.left.score,tempflagcombine=self.combine(self.left.gamegrid,self.score)
        self.left.gamegrid,_=self.stack(self.left.gamegrid)
        if tempflagstack or tempflagcombine:
            self.left.gamegrid=self.add_new_tile(self.left.gamegrid)
        else:
            self.left=None
            return
        if self.game_over_look(self.left.gamegrid)==1:
            self.left=None

    def moveright(self):
        if not self.right is None:
            return
        self.right=State(self.gamegrid,self.score)
        self.right.gamegrid=self.reverse(self.gamegrid)
        self.right.gamegrid,tempflagstack=self.stack(self.right.gamegrid)
        self.right.gamegrid,self.right.score,tempflagcombine=self.combine(self.right.gamegrid,self.score)
        self.right.gamegrid,_=self.stack(self.right.gamegrid)
        self.right.gamegrid=self.reverse(self.right.gamegrid)
        if tempflagstack or tempflagcombine:
            self.right.gamegrid=self.add_new_tile(self.right.gamegrid)
        else:
            self.right=None
            return
        if self.game_over_look(self.right.gamegrid)==1:
            self.right=None

    def moveup(self):
        if not self.up is None:
            return
        self.up=State(self.gamegrid,self.score)
        self.up.gamegrid=self.transpose(self.gamegrid)
        self.up.gamegrid,tempflagstack=self.stack(self.up.gamegrid)
        self.up.gamegrid,self.up.score,tempflagcombine=self.combine(self.up.gamegrid,self.score)
        self.up.gamegrid,_=self.stack(self.up.gamegrid)
        self.up.gamegrid=self.transpose(self.up.gamegrid)
        if tempflagstack or tempflagcombine:
            self.up.gamegrid=self.add_new_tile(self.up.gamegrid)
        else:
            self.up=None
            return
        if self.game_over_look(self.up.gamegrid)==1:
            self.up=None

    def movedown(self):
        if not self.down is None:
            return
        self.down=State(self.gamegrid,self.score)
        self.down.gamegrid=self.transpose(self.gamegrid)
        self.down.gamegrid=self.reverse(self.down.gamegrid)
        self.down.gamegrid,tempflagstack=self.stack(self.down.gamegrid)
        self.down.gamegrid,self.down.score,tempflagcombine=self.combine(self.down.gamegrid,self.score)
        self.down.gamegrid,_=self.stack(self.down.gamegrid)
        self.down.gamegrid=self.reverse(self.down.gamegrid)
        self.down.gamegrid=self.transpose(self.down.gamegrid)
        if tempflagstack or tempflagcombine:
            self.down.gamegrid=self.add_new_tile(self.down.gamegrid)
        else:
            self.down=None
            return
        if self.game_over_look(self.down.gamegrid)==1:
            self.down=None

    def checknext(self):
        if self.game_over_look(self.gamegrid)==0:
            return
        self.moveleft()
        self.moveright()
        self.moveup()
        self.movedown()

class History:
    def __init__(self):
        self.index=0
        self.history=[]
        self.history.clear()
    
    def __repr__(self):
        return str(self.history)

    def push(self,state,direction):
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
        self.history=[]
        self.index=0
    
    def pop(self):
        self.index-=1
        return self.history[self.index-1][0].gamegrid, self.history[self.index-1][0].score
