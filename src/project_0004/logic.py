# logic.py
from typing import List, Optional

Board = List[List[str]]

def create_board() -> Board:
    """Create a 3x3 board initialized with spaces."""
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board: Board) -> None:
    """Return a string representation of the board."""
    rows = []
    for i, row in enumerate(board):
        rows.append(" | ".join(row))
        if i < 2:
            rows.append("-" * 5)
    print("\n".join(rows))

def make_move(board: Board, row: int, col: int, player: str) -> bool:
    """Place player's mark on the board. Returns True if successful."""
    if board[row][col] == " ":
        board[row][col] = player
        return True
    return False

def is_winner(board: Board, player: str) -> bool:
    # rows, columns, diagonals
    lines = (
        board[0], board[1], board[2],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    )
    return any(all(cell == player for cell in line) for line in lines)

def is_draw(board: Board) -> bool:
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board: Board) -> List[tuple]:
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]