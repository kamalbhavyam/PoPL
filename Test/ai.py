import math
import time
import copy
import numpy as np

class AI():
    
    def getmove(self,state):
        bestmove,_ =self.maximise(state)
        return bestmove
    
    def evalstate(self,state,n_empty):
        grid = state.gamegrid

        utility = 0
        smoothness = 0

        big_t = np.sum(np.power(grid,2))
        s_grid = np.sqrt(grid)
        smoothness -= np.sum(np.abs(s_grid[::,0]-s_grid[::,1]))
        smoothness -= np.sum(np.abs(s_grid[::,1]-s_grid[::,2])) 
        smoothness -= np.sum(np.abs(s_grid[::,2]-s_grid[::,3]))
        smoothness -= np.sum(np.abs(s_grid[0,::]-s_grid[1,::]))
        smoothness -= np.sum(np.abs(s_grid[1,::]-s_grid[2,::]))
        smoothness -= np.sum(np.abs(s_grid[2,::]-s_grid[3,::]))
        
        empty_w=100000
        smoothness_w=3

        empty_u=n_empty*empty_w
        smoothness_u=smoothness**smoothness_w
        big_t_u=big_t

        utility += big_t
        utility += empty_u
        utility += smoothness_u

        return (utility, empty_u, smoothness_u, big_t_u)

    def maximise(self,state,depth=0):
        moves=state.getavailablemoves()
        moves_board=[]

        for m in moves:
            m_state=copy.deepcopy(state)
            if m==0:
                m_state.moveleft()
                m_state=m_state.left
            elif m==1:
                m_state.moveright()
                m_state=m_state.right
            elif m==2:
                m_state.moveup()
                m_state=m_state.up
            elif m==3:
                m_state.movedown()
                m_state=m_state.down
            if m_state is None:
                pass
            else:
                moves_board.append((m,m_state))
        
        max_utility=(float('-inf'),0,0,0)
        best_direction = None

        for mb in moves_board:
            utility = self.chance(mb[1],depth+1)

            if utility[0] >= max_utility[0]:
                max_utility = utility
                best_direction = mb[0]
        
        return best_direction,max_utility
    
    def chance(self,state,depth=0):
        empty_cells=state.getemptycells()
        n_empty=len(empty_cells)

        if n_empty >= 6 and depth >= 3:
            return self.evalstate(state,n_empty)

        if n_empty >= 0 and depth >= 5:
            return self.evalstate(state,n_empty)

        if n_empty==0:
            _,utility=self.maximise(state,depth+1)
            return utility
        
        possible_tiles=[]

        chance_2=(.9*(1/n_empty))
        chance_4=(.1*(1/n_empty))

        for empty_cell in empty_cells:
            possible_tiles.append((empty_cell,2,chance_2))
            possible_tiles.append((empty_cell,4,chance_4))

        utility_sum=[0,0,0,0]

        for t in possible_tiles:
            t_state=copy.deepcopy(state)
            t_state.insert_tile(t[0],t[1])
            _,utility=self.maximise(t_state,depth+1)

            for i in range(4):
                utility_sum[i]+=utility[i]*t[2]
        
        return tuple(utility_sum)

    # def nextmove(self,state,n=3):
    #     m, _ = self.predictmove(state,n)
    #     return m

    # def greedypredict(self,board):
    #     h_score = -100000000
    #     h_move = 0

    #     for i in range(1,5):

    #         copygrid = copy.deepcopy(board)
    #         if i==1:
    #             copygrid.moveleft()
    #             if copygrid.left is None:
    #                 continue
    #         elif i==2:
    #             copygrid.moveright()
    #             if copygrid.right is None:
    #                 continue
    #         elif i==3:
    #             copygrid.moveup()
    #             if copygrid.up is None:
    #                 continue
    #         elif i==4:
    #             copygrid.movedown()
    #             if copygrid.down is None:
    #                 continue
    #         thisscore=copygrid.score

    #         if not any(0 in row for row in board.gamegrid) and not self.horizontal_move_exits(board.gamegrid) and not self.vertical_move_exits(board.gamegrid):
    #             thisscore = -1

    #         if thisscore > h_score:
    #             h_score = thisscore
    #             h_move = i
            
    #     if h_move==0:
    #         h_move = random.randint(1,4)

    #     return (h_move, h_score)

    # def predictmove(self,board,n):
    #     h_score=-100000000
    #     h_move = 0

    #     if n==1:
    #         return self.greedypredict(board)
        
    #     for i in range(1,5):
    #         copygrid=copy.deepcopy(board)
    #         if i==1:
    #             copygrid.moveleft()
    #             if copygrid.left is None:
    #                 continue
    #         elif i==2:
    #             copygrid.moveright()
    #             if copygrid.right is None:
    #                 continue
    #         elif i==3:
    #             copygrid.moveup()
    #             if copygrid.up is None:
    #                 continue
    #         elif i==4:
    #             copygrid.movedown()
    #             if copygrid.down is None:
    #                 continue
    #         thisscore=copygrid.score

    #         tmove,tscore=self.predictmove(copygrid,n-1)

    #         thisscore+=tscore

    #         if thisscore > h_score:
    #             h_score=thisscore
    #             h_move=i

    #     if h_move==0:
    #         h_move=random.randint(1,4)

    #     return h_move,h_score


    # def nextmove(self,state,n=5):
    #     h_score = -1
    #     h_move = 0
    #     if len(state.getemptycells())>4:
    #         pass
    #     else:
    #         n=6
        
    #     for i in range(1,5):
    #         copygrid=copy.deepcopy(state)
    #         if i==1:
    #             copygrid.moveleft()
    #             if copygrid.left is None:
    #                 continue
    #         elif i==2:
    #             copygrid.moveright()
    #             if copygrid.right is None:
    #                 continue
    #         elif i==3:
    #             copygrid.moveup()
    #             if copygrid.up is None:
    #                 continue
    #         elif i==4:
    #             copygrid.movedown()
    #             if copygrid.down is None:
    #                 continue
    #         thisscore=self.expectimax(copygrid,n-1,False) + copygrid.score
    #         if thisscore > h_score:
    #             h_score = thisscore
    #             h_move=i
            
    #     return h_move

    # def patternHeuristics(self,board):

    #     cells = np.array(board.gamegrid)

    #     W = np.array([[0,0,1,3],
    #                 [0,1,3,5],
    #                 [1,3,5,15],
    #                 [3,5,15,30]])

    #     return np.sum(W*cells) #/ 16

    # def clusterHeuristics(self,board):

    #     cells = np.array(board.gamegrid)

    #     size = 4
    #     penalty = 0
    #     penalty += np.sum(np.abs(cells[:size-2,:] - cells[1:size-1,:]))
    #     penalty += np.sum(np.abs(cells[2:size,:] - cells[1:size-1,:]))
    #     penalty += np.sum(np.abs(cells[:,:size-2] - cells[:,1:size-1]))
    #     penalty += np.sum(np.abs(cells[:,2:size] - cells[:,1:size-1]))

    #     return penalty / 2
    
    # def monotonicHeuristics(self,board):

    #     cells = np.array(board.gamegrid)
    #     # print("yee",cells)
    #     size = 4
    #     cells[cells<1] = 0.1

    #     try:
    #         score1 = cells[1:size,3]/cells[:size-1,3]
    #         score2 = cells[3,1:size]/cells[3,:size-1]
    #     except:
    #         print(cells)
    #     score = np.sum(score1[score1==2])
    #     score+= np.sum(score2[score2==2])

    #     return score * 20

    # def expectimax(self,board, n, maxPlayer):
    #     if n==0:
    #         if not (self.horizontal_move_exits(board.gamegrid) and self.vertical_move_exits(board.gamegrid)):
    #             return -10000
    #         return self.patternHeuristics(board) - self.clusterHeuristics(board) + self.monotonicHeuristics(board)
    #         # return 0
        
    #     if maxPlayer:
    #         h_val=-1
    #         for i in range(1,5):
    #             copygrid=copy.deepcopy(board)
    #             if i==1:
    #                 copygrid.moveleft()
    #                 if copygrid.left is None:
    #                     continue
    #             elif i==2:
    #                 copygrid.moveright()
    #                 if copygrid.right is None:
    #                     continue
    #             elif i==3:
    #                 copygrid.moveup()
    #                 if copygrid.up is None:
    #                     continue
    #             elif i==4:
    #                 copygrid.movedown()
    #                 if copygrid.down is None:
    #                     continue
    #             print("switch")
    #             val=self.expectimax(copygrid,n-1,False)

    #             if val>h_val:
    #                 h_val=val
    #         return h_val
    #     else:
    #         sum_val=0
    #         num=0
    #         for cell in board.getemptycells():
    #             copygrid=copy.deepcopy(board)
    #             x,y =cell
    #             copygrid.gamegrid[x][y]=2

    #             print("switch back")
    #             sum_val += self.expectimax(copygrid,n-1,True)
    #             num+=1
            
    #         if num==0:
    #             print("num 0")
    #             return self.expectimax(board,n-1,True)
            
    #         return sum_val/num
