from logic import TicTacToe

def display(board):
    print('\n'.join([
        f' {board[0]} | {board[1]} | {board[2]} ',
        '---+---+---',
        f' {board[3]} | {board[4]} | {board[5]} ',
        '---+---+---',
        f' {board[6]} | {board[7]} | {board[8]} '
    ]))

def main():
    game = TicTacToe()
    while True:
        display(game.get_board())
        move = input(f"Player {game.current_player()}'s move (1-9): ")
        if not move.isdigit() or not (1 <= int(move) <= 9):
            print('Invalid input. Choose 1-9.')
            continue
        pos = int(move) - 1
        if not game.make_move(pos):
            print('Cell occupied. Try again.')
            continue
        result = game.check_winner()
        if result:
            display(game.get_board())
            if result == 'Draw':
                print('Game ends in a draw.')
            else:
                print(f'Player {result} wins!')
            break

if __name__ == '__main__':
    main()
