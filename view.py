# pyright: strict

from __future__ import annotations
from collections.abc import Sequence
#from typing import Literal

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
    
    def ask_for_move(self, valid_moves: set[tuple[int, int]]) -> tuple[int, int]:
        readable_moves = sorted([self.coords_to_notation(mv) for mv in valid_moves])
        print(f'VALID MOVES: {readable_moves}')
        
        col_ch = "abcdefgh"
        row_lvl = "87654321"
        
        while True:
            c_in = input('Choose a valid col (a-h) [-1: exit piece]: ').strip().lower()
            if c_in == '-1':
                return (-1, -1)
            if c_in not in col_ch:
                print('Invalid column letter, try again.')
                continue
                
            r_in = input('Choose a valid row/rank (1-8) [-1: exit piece]: ').strip().lower()
            if r_in == '-1':
                return (-1, -1)
            if r_in not in row_lvl:
                print('Invalid row rank digit, try again.')
                continue
            
            notation = f"{c_in}{r_in}"
            coords = self.notation_to_coords(notation)
            
            if coords is None or coords not in valid_moves:
                print('Invalid. Try again.')
                continue
                
            return coords
    
    def coords_to_notation(self, coord: tuple[int, int]) -> str:
        r, c = coord
        col_ch = "abcdefgh"
        row_lvl = "87654321" 
        if 0 <= r < 8 and 0 <= c < 8:
            return f"{col_ch[c]}{row_lvl[r]}"
        return f"({r},{c})"

    def notation_to_coords(self, notation: str) -> tuple[int, int] | None:
        notation = notation.strip().lower()
        if len(notation) != 2:
            return None
            
        col_ch = "abcdefgh"
        row_lvl = "87654321"
        
        file_char, rank_char = notation[0], notation[1]
        if file_char in col_ch and rank_char in row_lvl:
            c = col_ch.index(file_char)
            r = row_lvl.index(rank_char)
            return (r, c)
        return None
    
    def display_invalid_piece(self) -> None:
        print(f"Chosen Chess Piece has no valid moves. Choose another Chess Piece")

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
    def empty_board(self) -> tuple[tuple[str, ...], ...]:
        keys = ['█', '▒']
        row1 = tuple(keys[i % 2] for i in range(8))
        row2 = tuple(keys[(i + 1) % 2] for i in range(8))
        choices = [row1, row2]
        final = tuple(choices[i % 2] for i in range(8))
        return final

    def character_to_display(self) -> dict[ChessColor, dict[str, str]]:
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