#/usr/bin/python3
class TicTacToe:

    def __init__(self):
        self.board = []
        self.ai = 'X'
        self.human = 'O'

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
        if self.draw_check() :
            return 0
        elif self.is_player_win(self.ai):
            return 1 # win AI
        elif self.is_player_win(self.human):
            return -1 # lost AI
        
        if isMax:
            bestScore = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.ai)
                        score = self.minimax(depth + 1, False)
                        self.set_board(i, j, '-')
                        bestScore = max(score, bestScore)
            return bestScore   
        else:
            bestScore = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.set_board(i, j, self.human)
                        score = self.minimax(depth + 1, True)
                        self.set_board(i, j, '-')
                        bestScore = min(score, bestScore)
            return bestScore

    def bestMove(self, f, player): # f is the decision making function (minimax, expectimax)
        bestScore = -float('inf')
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
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    if(row > 3 or col > 3 or self.board[row-1][col-1] != '-'):
                        print("Error: This position is invalid!")
                    else:
                        selected_pos = True
                print()

                # set X or O on the board
                self.set_board(row - 1, col - 1, player)
            else:
                print()
                self.bestMove(self.minimax, player)

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