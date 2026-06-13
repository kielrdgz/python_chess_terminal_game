# pyright: strict

from __future__ import annotations
from collections.abc import Sequence
from typing import Literal

from data_types import *

class ChessView:
    def __init__(self, styled: bool = False) -> None:
        self.styled = styled

    def display_grid(self, grid: Sequence[Sequence[ChessPiece]], turn: ChessColor, empty: str) -> None:
        emojis = self.character_to_display()
        col_ch = 'abcdefgh'

        emoji_grid: list[list[str]] = []
        styled_board = self.empty_board

        if self.styled:
            for r in range(8):
                row: list[str] = []
                for c in range(8):
                    p = grid[r][c]
                    styled_tile = styled_board[r][c]

                    if not p.is_empty:
                        char = p.piece_id[0] if not p.piece_id.startswith("Pawn") else 'P'
                        row.append(emojis[p.color][char])
                    else:
                        row.append(styled_tile)
                emoji_grid.append(row)
        else:
            for row_p in grid:
                temp: list[str] = []
                for p in row_p:
                    if not p.is_empty:
                        char = p.piece_id[0] if not p.piece_id.startswith("Pawn") else 'P'
                        temp.append(emojis[p.color][char])
                    else:
                        temp.append(empty)
                    emoji_grid.append(temp)
        
        if turn == ChessColor.BLACK:
            print('< BLACK POV >')
            for i, r in enumerate(emoji_grid):
                label = i + 1
                str = '   '.join(r)
                print(f"{label}   {str}")
            print(f"    {'   '.join(col_ch[::-1])}")
        else:
            print('< WHITE POV >')
            for i, r in enumerate(emoji_grid):
                label = 8 - i
                str = '   '.join(r)
                print(f"{label}   {str}")
            print(f"    {'   '.join(col_ch)}")

    def display_turn(self, player_turn: ChessColor) -> None:
        print(f'Current Turn: {player_turn}')

    def display_winner(self, winner: ChessColor, name: str) -> None:
        print(f'Congratulations!')
        print(f'Winner: < {winner} > {name}\n')

    def display_move(self, move: ChessMove, r: int, c: int, cell: ChessPiece, taken: bool) -> None:
        col_ch = 'abcdefgh'
        row_lvl = '87654321'

        move_str = str(move)
        move_msg = f"{move_str} to {col_ch[c]}{row_lvl[r]}"
        print(move_msg)
        print(move.__repr__())

        if taken and not cell.is_empty:
            print(f"{cell.piece_id} has been taken!")

    def display_moves_done(self, moves_done: dict[ChessColor, list[ChessMove]]) -> None:
        print(f'White: {moves_done[ChessColor.WHITE]}\n')
        print(f'Black: {moves_done[ChessColor.BLACK]}')
    
    def ask_for_piece(self, valid_pieces: list[str]) -> str:
        while True:
            print(f'CHOICES: {valid_pieces}')
            piece = input('Choose a valid chess piece: ').strip()
            
            matched = next((p for p in valid_pieces if p.lower() == piece.lower()), None)
            if matched is None:
                print("Invalid choice. Try again.")
                continue
            return matched
    
    def ask_for_move(self, valid_moves: Set[Tuple[int, int]], grid_r: int, grid_c: int) -> Tuple[int, int]:
        print(f'VALID MOVES: {valid_moves}')
        while True:
            r_in = input('Choose a valid row [-1: exit piece]: ').strip()
            try:
                r = int(r_in)
            except ValueError:
                print('Invalid input, try again.')
                continue
            if r == -1 or 0 <= r < grid_r:
                break
            print('Out of bounds, try again.')
            
        if r == -1:
            return (-1, -1)
            
        while True:
            c_in = input('Choose a valid col [-1: exit piece]: ').strip()
            try:
                c = int(c_in)
            except ValueError:
                print('Invalid input, try again.')
                continue
            if c == -1 or 0 <= c < grid_c:
                break
            print('Out of bounds, try again.')
            
        if c == -1: # cancel move
            return (-1, -1)
            
        return (r, c)

    def configure_enemy(self, choices: dict[str, Any]) -> Any:
        print('CHOICES:')
        for k, v in choices.items():
            print(f'\t{k}: {v.__name__}')
        while True:
            choice = input('Choose a valid enemy ai key: ').strip().lower()
            if choice not in choices:
                print('Invalid choice, try again!')
                continue
            return choices[choice]
        
    def configure_turn(self) -> int:
        while True:
            choice = input('Choose which player is playing White [1, 2]: ').strip()
            try:
                turn = int(choice)
            except ValueError:
                print('Invalid input, try again!')
                continue
            if turn not in {1, 2}:
                print('Invalid turn, try again!')
                continue
            return turn
    
    @property
    def empty_board(self) -> Tuple[Tuple[str, ...], ...]:
        keys = ['█', '▒']
        row1 = tuple(keys[i % 2] for i in range(8))
        row2 = tuple(keys[(i + 1) % 2] for i in range(8))
        choices = [row1, row2]
        final = tuple(choices[i % 2] for i in range(8))
        return final

    def character_to_display(self) -> Dict[ChessColor, Dict[str, str]]:
        return {
            ChessColor.WHITE: {
                'Q': '♛',
                'K': '♚',
                'R': '♜',
                'B': '♝',
                'N': '♞',
                'P': '♟',
            },
            ChessColor.BLACK: {
                'Q': '♕',
                'K': '♔',
                'R': '♖',
                'B': '♗',
                'N': '♞',
                'P': '♙',
            },
        }