import tkinter as tk
import tkinter.simpledialog
import numpy as np
import random
import copy

class Colors:
    """
    Make variables that define colors for the background and foreground of the tiles. Also instantiates the Font, and Text color for Score and other UI elements.
    """
    def __init__(self):
        self.UIBACK='#eee4da'
        self.BACKGROUND_COLOR = '#bbada0'
        self.EMPTY_CELL_COLOR = '#cdc1b4'
        self.CELL_BACKGROUND_COLOR_DICT = {
            -1: '#3c3a32',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e',
            'beyond': '#3c3a32'
        }
        self.CELL_COLOR_DICT = {
            -1: '#f9f6f2',
            2: '#776e65',
            4: '#776e65',
            8: '#f9f6f2',
            16: '#f9f6f2',
            32: '#f9f6f2',
            64: '#f9f6f2',
            128: '#f9f6f2',
            256: '#f9f6f2',
            512: '#f9f6f2',
            1024: '#f9f6f2',
            2048: '#f9f6f2',
            'beyond': '#f9f6f2'
        }
        self.FONT = ('Verdana', 30, 'bold')
        self.SCOREFONT = ('Verdana', 25, 'bold')
        self.SCORECOLOR = '#534d46'
        self.TITLEFONT = ('Verdana', 44, 'bold')
        self.SUBTITLEFONT = ('Verdana', 10)

class GUI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.colors=Colors()
        self.config(bg=self.colors.UIBACK)
        self.grid(ipadx=50,ipady=100)
        self.master.title("2048 by Bhavyam")
        self.main_grid = tk.Frame(
            self, bg = self.colors.BACKGROUND_COLOR, bd=3, width = 480, height = 480
        )
        # self.main_grid.pack(pady=(100, 0))
        self.main_grid.pack( side= "bottom", pady=(0,30))
        self.make_GUI()

    def make_GUI(self):
        """
        Initialise Main Frame and Grid for the game.
        Also Initialise the Score, Title and Game Over frames.
        """
        self.overflag=False
        self.winflag=False
        self.bomeshflag=False
        self.cells = []
        for i in range(4):
            row=[]
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid, bg = self.colors.EMPTY_CELL_COLOR, width = 120, height = 120
                )
                cell_frame.grid(row = i, column = j, padx =5, pady =5)
                cell_number = tk.Label(self.main_grid, bg = self.colors.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame" : cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
            
        self.game_over_frame = tk.Frame(self.main_grid,width=480, height=480, borderwidth =2)
        self.game_over_frame_label=tk.Label(
            self.game_over_frame,
            bg=self.colors.CELL_BACKGROUND_COLOR_DICT["beyond"],
            fg=self.colors.CELL_COLOR_DICT["beyond"],
            font=self.colors.FONT
        )
        score_frame = tk.Frame(self, bg = self.colors.UIBACK, width = 520, height=150)
        score_frame.place(relx=0.91, width = 220, rely=0.1, anchor="center")
        self.scorename_label = tk.Label(score_frame, bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="Score", font=self.colors.SCOREFONT)
        self.scorename_label.grid(row=0,sticky='e')
        self.score_label = tk.Label(score_frame, bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="0", font=self.colors.SCOREFONT)
        self.score_label.grid(row=1,sticky='e')

        title_frame = tk.Frame(self, bg = self.colors.UIBACK, width = 520, height=150)
        title_frame.place(relx=0.33, width = 320, rely=0.13,anchor="center")
        self.title_frame_label = tk.Label(title_frame, bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="2048", font=self.colors.TITLEFONT)
        self.title_frame_label.grid(row=0,sticky='w')
        self.title_sublabel = tk.Label(title_frame,bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="Use WASD or Arrow Keys to Play", font=self.colors.SUBTITLEFONT)
        self.title_sublabel.grid(row=1, sticky='w')
        self.title_sublabel2 = tk.Label(title_frame,bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="Z to Undo, E to Lookahead Into Future States", font=self.colors.SUBTITLEFONT)
        self.title_sublabel2.grid(row=3, sticky='w')
        self.title_sublabel3 = tk.Label(title_frame,bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="Use Q to Quit, Use R to Restart Game", font=self.colors.SUBTITLEFONT)
        self.title_sublabel3.grid(row=2, sticky='w')
        self.title_sublabel4 = tk.Label(title_frame,bg = self.colors.UIBACK, fg=self.colors.SCORECOLOR, text="Use P to Print History, Use I to Print StateInfo", font=self.colors.SUBTITLEFONT)
        self.title_sublabel4.grid(row=4, sticky='w')
        self.agent_label=tk.Label(title_frame,bg=self.colors.UIBACK,fg=self.colors.SCORECOLOR,text="Or PRESS F and Sit Back...", font=self.colors.SUBTITLEFONT)
        self.agent_label.grid(row=5,sticky='w')

    def horizontal_move_exits(self,matrix):
        """
        Check if tiles can be combined when moving left or right.

        Args:
            matrix (2D List): Game grid
        
        Returns:
            Boolean value of if there exists a horizontal move
        """
        for i in range(4):
            for j in range(3):
                if matrix[i][j] == matrix[i][j+1]:
                    return True
        return False

    def vertical_move_exits(self,matrix):
        """
        Check if tiles can be combined when moving up or down.

        Args:
            matrix (2D List): Game grid

        Returns:
            Boolean value of if there exists a vertical move
        """
        for i in range(3):
            for j in range(4):
                if matrix[i][j] == matrix[i+1][j]:
                    return True
        return False

    def game_over(self,matrix):
        """
        Check if game is over by checking if the player has already won(if 2048 has been achieved) or if no moves can be made (No empty cells and no combinations possible).
        
        Args:
            matrix (2D List): Game grid
        
        Returns:
            Changes Flags based on win and game over conditions.
        """
        if any(-1 in row for row in matrix):
            self.bomeshflag=True
            return
        if any(2048 in row for row in matrix):
            self.overflag=True
            self.winflag=True
        elif not any(0 in row for row in matrix) and not self.horizontal_move_exits(matrix) and not self.vertical_move_exits(matrix):
            self.overflag=True
        else:
            self.overflag=False
            self.winflag=False

    def update_GUI(self,matrix,score):
        """
        Checks matrix and updates GUI based on the matrix.
        Checks if game is over. If game is over, generate the game over frame.

        Args:
            matrix (2D List): Game grid
            score (int): Integer score for the game state
        """
        for i in range(4):
            for j in range(4):
                cell_value = matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=self.colors.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=self.colors.EMPTY_CELL_COLOR, text ="")
                else:
                    if cell_value==-1:
                        self.cells[i][j]["frame"].configure(bg=self.colors.CELL_BACKGROUND_COLOR_DICT[cell_value])
                        self.cells[i][j]["number"].configure(
                            bg=self.colors.CELL_BACKGROUND_COLOR_DICT[cell_value],
                            fg=self.colors.CELL_COLOR_DICT[cell_value],
                            font=self.colors.FONT,
                            text="B"
                        )
                    else:
                        self.cells[i][j]["frame"].configure(bg=self.colors.CELL_BACKGROUND_COLOR_DICT[cell_value])
                        self.cells[i][j]["number"].configure(
                            bg=self.colors.CELL_BACKGROUND_COLOR_DICT[cell_value],
                            fg=self.colors.CELL_COLOR_DICT[cell_value],
                            font=self.colors.FONT,
                            text=str(cell_value)
                        )

        self.game_over(matrix)
        # if self.bomeshflag==True:
        #     for elem in self.game_over_frame.winfo_children():
        #         elem.pack_forget()
        #     self.game_over_maker("BOMESH!")
        if self.overflag==True:
            if self.winflag==True:
                for elem in self.game_over_frame.winfo_children():
                    elem.pack_forget()
                self.game_over_maker("You win!")
            else:
                for elem in self.game_over_frame.winfo_children():
                    elem.pack_forget()
                self.game_over_maker("Game Over!")
        else:
            if self.game_over_frame.winfo_ismapped():
                for elem in self.game_over_frame.winfo_children():
                    elem.pack_forget()
                self.game_over_frame.place_forget()

        self.score_label.configure(text=score)
        self.update_idletasks()

    def game_over_maker(self,textmsg):
        """
        Place the Game over frame in it's parent frame.

        Args:
            textmsg (String): Message to be put into frame.
        """
        # self.game_over_frame = tk.Frame(self.main_grid,width=480, height=480, borderwidth =2)
        self.game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.game_over_frame_label.configure(text=textmsg)
        self.game_over_frame_label.pack()
    
    def popup(self):
        """
        Create popup that takes input from user for number of steps to lookahead into.
        """
        return tkinter.simpledialog.askstring('Input Lookahead Steps', 'How many steps ahead do you wish to look\n(Large Number may result in memory issues, keep < 5 for easy output)\n(Output states possible to console, default to 3 if cancelled or nothing is entered)',parent=self.main_grid)
