from logic import TicTacToe

def print_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def main():
    game = TicTacToe()
    current = "X"
    while True:
        print_board(game.get_board())
        try:
            move = int(input(f"Player {current}, enter move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid position. Choose 1-9.")
                continue
        except ValueError:
            print("Please enter a number.")
            continue
        if not game.make_move(move, current):
            print("Spot already taken.")
            continue
        result = game.check_winner()
        if result:
            print_board(game.get_board())
            if result == "Draw":
                print("It's a draw!")
            else:
                print(f"Player {result} wins!")
            break
        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    main()
