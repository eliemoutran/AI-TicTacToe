#/usr/bin/python3
class TicTacToe:

    def __init__(self):
        self.board = []
        self.ai = 'X'
        self.human = 'O'
        self.moves = {1 : [0, 0], 2 : [0, 1], 3 : [0, 2],
                      4 : [1, 0], 5 : [1, 1], 6 : [1, 2],
                      7 : [2, 0], 8 : [2, 1], 9 : [2, 2]     
                    }                  

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

    def swap_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

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

    def bestMove(self, f, player): # f is the decision making function (minimax, expectimax)
        bestScore = -1000
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
        self.set_board(*move)

    def start(self):
        self.create_board()

        player = 'O'
        while True:
            print(f"Player {player} turn")

            self.show_board()

            # taking user input
            selected_pos = False
            if player == 'O':
                while not selected_pos:
                    input_user = int(input("Enter row and column numbers to fix spot: "))
                    if (input_user > 9 or input_user < 1) :
                        print("Please enter a valid number, between 1 and 9")
                    row, col = self.moves[input_user]
                    if(self.board[row][col] != '-'):
                        print("Error: This position is invalid!")
                    else:
                        selected_pos = True
                print()

                # set X or O on the board
                self.set_board(row, col, player)
            else:
                print()
                self.bestMove(self.AlphaBetaPruning, player)

            # checking whether current player is won or not
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # Checking for a draw
            if self.draw_check():
                print("Match Draw!")
                break

            # swapping player turn
            player = self.swap_turn(player)

        print()
        self.show_board()

# starting the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()