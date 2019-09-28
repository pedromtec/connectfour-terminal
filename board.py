import time

class Board:
    ROWS = 6
    COLUMNS = 7
    COLORS = {0: '\x1b[100m', 1: '\x1b[47m', 2: '\x1b[44m'}
    def __init__(self, player = 1):
        self.player = player
        self.board = [[0] * Board.COLUMNS for row in range(Board.ROWS)]
        self.winner = None
        self.window_winner = []

    def tint (self, value):
        if value in Board.COLORS.keys():
             return Board.COLORS[value] + '   \x1b[0m'

        return Board.COLORS[value // 3][:-1] + ';30;1;5m @ \x1b[0m'


    def __repr__(self):
        repr = ''
        for row in self.board:
            rrow = list(map(self.tint, row))
            repr += '  '.join(rrow) + '\n\n'
        return repr

    def animation(self, col):
        pass

    def update_winner_positions(self):
        if len(self.window_winner) <= 0:
            return None
        for wn in self.window_winner:
            self.board[wn[0]][wn[1]] = self.winner * 3

    def change_player(self):
        self.player = 1 if self.player == 2 else 2

    def drop_piece(self, column):
        if self.winner:
            return None
        if column < 0 or column >= Board.COLUMNS:
            return None
        row = 0
        while row < Board.ROWS and self.board[row][column] == 0:
            print('\033c')
            self.board[row][column] = self.player
            print(self)
            self.board[row][column] = 0
            time.sleep(0.1)
            row += 1
        row-=1
        if row < 0:
            return None
        self.board[row][column] = self.player
        self.check_winner()
        self.change_player()
        return self

    def check_window(self, window):
        if window.count(self.player) == 4:
            self.winner = self.player
            return True
        return False

    def check_winner(self):
        
        for row in range(Board.ROWS):
            for col in range(Board.COLUMNS-3):
                window = (self.board[row][col],
                         self.board[row][col+1],
                         self.board[row][col+2],
                         self.board[row][col+3])
                if self.check_window(window):
                    self.window_winner = [
                        (row, col), (row, col+1), (row, col+2), (row, col+3)
                    ]
                    return True


        for row in range(Board.ROWS-3):
            for col in range(Board.COLUMNS):
                window = (self.board[row][col],
                         self.board[row+1][col],
                         self.board[row+2][col],
                         self.board[row+3][col])
                if self.check_window(window):
                    self.window_winner = [
                        (row, col), (row+1, col), (row+2, col), (row+3, col)
                    ]
                    return True


        for row in range(Board.ROWS-3):
            for col in range(Board.COLUMNS-3):
                window = (self.board[row][col],
                         self.board[row+1][col+1],
                         self.board[row+2][col+2],
                         self.board[row+3][col+3])
                if self.check_window(window):
                    self.window_winner = [
                        (row, col), (row+1, col+1), (row+2, col+2), (row+3, col+3)
                    ]
                    return True

        for row in range(Board.ROWS-3):
            for col in range(3, Board.COLUMNS):
                window = (self.board[row][col],
                         self.board[row+1][col-1],
                         self.board[row+2][col-2],
                         self.board[row+3][col-3])
                if self.check_window(window):
                    self.window_winner = [
                        (row, col), (row+1, col-1), (row+2, col-2), (row+3, col-3)
                    ]
                    return True


if __name__ == '__main__':
    board = Board()
    while True:
        print('\033c')
        print(board, end='')
        print(f'{Board.COLORS[board.player][:-1]};30;7;5mJogador {board.player}, escolha uma coluna entre 0 e 6:\x1b[0m')
        column = int(input())
        if not board.drop_piece(column):
            print('Jogada Inválida!')
        if board.winner:
            board.update_winner_positions()
            break
    print('\033c')
    print(board, end='')
    print('Fim do jogo!')
    print(f'{Board.COLORS[board.winner]}{board.winner} venceu!\x1b[0m')
    #print(board, end='')
