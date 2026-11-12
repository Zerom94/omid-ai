class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current = 'X'
    def make_move(self, pos):
        if pos < 0 or pos > 8 or self.board[pos] != ' ':
            return False
        self.board[pos] = self.current
        self.current = 'O' if self.current == 'X' else 'X'
        return True
    def check_winner(self):
        b = self.board
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, i, j in lines:
            if b[a] == b[i] == b[j] != ' ':
                return b[a]
        if ' ' not in b:
            return 'Draw'
        return None
    def get_board(self):
        return self.board.copy()
    def current_player(self):
        return self.current
