# Charbel Farah
# Elie Moutran
# Emmanuel AbdelNour 

import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy

class TicTacToe:

    def __init__(self):
        self.menu = Tk()
        self.menu.geometry("250x250")
        self.menu.title("Tic Tac Toe")
        self.menu_play = Tk()
        self.menu_play.withdraw()
        self.wpc = partial(self.withpc)
        # self.wpl = partial(self.withplayer, self.menu)

        self.head = Label(self.menu, text="---Welcome to tic-tac-toe---",
                  fg="black", width=500, font='summer', bd=5)

        self.B1 = Button(self.menu, text="Single Player", command=self.wpc,
                    activeforeground='red',
                    activebackground="yellow", bg="blue",
                    fg="yellow", width=500, font='summer', bd=5)

        self.B2 = Button(self.menu, text="Multi Player", activeforeground='red',
                    activebackground="yellow", bg="blue", fg="yellow",
                    width=500, font='summer', bd=5)

        self.B3 = Button(self.menu, text="Exit", command=self.quit_menus, activeforeground='red',
                    activebackground="yellow", bg="blue", fg="yellow",
                    width=500, font='summer', bd=5)
        
        self.button_list = []
        self.l1 = Button(self.menu_play, text="Player : X", width=10)
        self.l2 = Button(self.menu_play, text="Computer : O", width=10, state=DISABLED)
        self.r = Button(self.menu_play, text="Restart Game", width = 10, command = self.restart_game)
        self.m = Button(self.menu_play, text = "Main Menu", width = 10, command = self.back)
        self.e = Button(self.menu_play, text = "Exit", width = 10, command = self.quit_menus)

        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.ai = 'O'
        self.human = 'X'
        self.moves = 0

    def quit_menus(self):
        self.menu.quit()
        self.menu_play.quit()

    def gameboard_pc(self):
        self.button_list = []
        for i in range(3):
            m = 6 + i
            self.button_list.append([])
            for j in range(3):
                n = j
                self.button_list[i].append(j)
                get_t = partial(self.button_text, i, j)
                self.button_list[i][j] = Button(
                    self.menu_play, bd=5, command=get_t, height=4, width=8)
                self.button_list[i][j].grid(row=m, column=n)
        #self.menu_play.mainloop()

    # Initialize the game board to play with system
    def withpc(self):
        self.menu.withdraw()
        self.menu_play.deiconify()
        self.menu_play.title("Tic Tac Toe")
        self.l1.grid(row=1, column=1)
        self.l2.grid(row=2, column=1)
        self.r.grid(row =3, column=1)
        self.m.grid(row=4, column=1)
        self.e.grid(row=5, column=1)
        self.gameboard_pc()

    def restart_game(self) :
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.moves = 0
        if self.button_list:
            for i in range(3):
                for j in range(3):
                    self.button_list[i][j].destroy()
        self.button_list = []
        self.gameboard_pc()

    def back(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.moves = 0
        for i in range(3):
            for j in range(3):
                self.button_list[i][j].destroy()
        self.menu_play.withdraw()
        self.menu.deiconify()

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.button_list[i][j].config(state='disabled')

    def button_text(self, i , j):
        self.set_board(i, j, self.human)
        self.button_list[i][j].config(text = 'X')
        self.button_list[i][j].config(state='disable')
        self.moves += 1

        #checking if the player won
        if self.is_player_win(self.human):
            box = messagebox.showinfo("Winner", "Player won the match")
            self.disable_buttons()

        # Checking for a draw
        elif self.draw_check():
            box = messagebox.showinfo("Tie Game", "Tie Game")
            
        if self.moves < 8:
            (x, y) = self.bestMove(self.AlphaBetaPruning, self.ai)
            self.button_list[x][y].config(text = 'O')
            self.button_list[x][y].config(state='disable')   

            #checking if the ai won
            if self.is_player_win(self.ai):
                box = messagebox.showinfo("Winner", "Computer won the match")
                self.disable_buttons()

            elif self.draw_check():
                box = messagebox.showinfo("Tie Game", "Tie Game")

            self.moves += 1

    ##########################################

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def set_board(self, row, col, player):
        self.board[row][col] = player

    def is_player_win(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        return win

    def draw_check(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True
        
    # Testing different ways for computer decisions
    # TODO minimax
    def minimax(self, depth, isMax):
        # Base case
        if self.is_player_win(self.ai):
            return 10 - depth # win AI
        elif self.is_player_win(self.human):
            return depth - 10 # lost AI
        elif self.draw_check() :
            return 0
        
        if isMax:
            bestScore = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.ai)
                        score = self.minimax(depth + 1, False)
                        self.set_board(i, j, '-')
                        bestScore = max(score, bestScore)
            return bestScore   
        else:
            bestScore = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.human)
                        score = self.minimax(depth + 1, True)
                        self.set_board(i, j, '-')
                        bestScore = min(score, bestScore)
            return bestScore

    def AlphaBetaPruning(self, depth, isMax, alpha, beta):
        if self.is_player_win(self.ai):
            return 10 - depth # win AI
        elif self.is_player_win(self.human):
            return depth - 10 # lost AI
        elif self.draw_check() :
            return 0

        if isMax:
            BestScore= -1000   
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.ai)
                        score = self.AlphaBetaPruning(depth+1, False, alpha, beta)
                        self.set_board(i, j, '-')
                        BestScore = max(BestScore, score)   
                        alpha = max(alpha, BestScore)      
                        if beta <= alpha:
                            break
            return alpha
        else:
            BestScore = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.human)
                        score = self.AlphaBetaPruning(depth+1, True, alpha, beta)
                        self.set_board(i, j, '-')
                        BestScore = min(BestScore, score)   
                        beta = min(beta, BestScore)      
                        if beta <= alpha:
                            break
            return beta

    def bestMove2(self, f, player): # f is the decision making function (minimax, expectimax)
        bestScore = -1000
        move = (-1, -1, player)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.set_board(i,j,player)
                    score = f(0, False)
                    # Undo your move
                    self.set_board(i,j,'-')
                    if (score > bestScore):
                        bestScore = score
                        move = (i , j, player)
        self.set_board(*move)

    def bestMove(self, f, player): 
        bestScore = -1000
        x = -1
        y = -1
        move = (-1, -1, player)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.set_board(i,j,player)
                    score = f(0, False, -1000, 1000)
                    # Undo your move
                    self.set_board(i,j,'-')
                    if (score > bestScore):
                        bestScore = score
                        move = (i , j, player)
                        x = i
                        y = j
        self.set_board(*move)
        return (x , y)

    def start(self):
        self.head.pack(side='top')
        self.B1.pack(side='top')
        self.B2.pack(side='top')
        self.B3.pack(side='top')
        self.menu_play.mainloop()
        self.menu.mainloop()

# starting the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()