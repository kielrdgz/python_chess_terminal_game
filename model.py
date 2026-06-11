# pyright: strict

from __future__ import annotations
import random
from copy import deepcopy


from data_types import *


class ChessModel:
    def __init__(self, p1: Player, p2: Player, empty: str, chosen: str) -> None:
        self._r: int = 8
        self._c: int = 8
        
        self._white_player: Player
        self._black_player: Player
        self._assign_players(p1, p2, chosen)

        self._grid: list[list[ChessPiece]] = [[]]
        self._initialize_grid()

        self._empty: str = empty 

        self._pieces: dict[str, list[str]] = {} # key: players, values: pieces present
        self._initialize_pieces()

        self._turn: ChessColor = ChessColor.WHITE
        self._gameover: bool = False
        self._winner: ChessColor | None = None
        self._moves_done: dict[ChessColor, list[ChessMove]] = {ChessColor.WHITE: [],
                                                   ChessColor.BLACK: [],}

    @property
    def row(self) -> int:
        return self._r
    
    @property
    def col(self) -> int:
        return self._c
    
    @property
    def empty(self) -> str:
        return self._empty
    
    @property
    def grid(self) -> list[list[ChessPiece]]:
        return deepcopy(self._grid)
    
    def _assign_players(self, p1: Player, p2: Player, chosen: str) -> None:
        if chosen.lower() == "white":
            self._white_player, self._black_player = p1, p2
        elif chosen.lower() == "black":
            self._white_player, self._black_player = p2, p1
        else:
            if random.choice([True, False]):
                self._white_player, self._black_player = p1, p2
            else:
                self._white_player, self._black_player = p2, p1

    def _initialize_grid(self) -> None:
        final: list[list[ChessPiece]] = [[EmptyPiece((r, c), self.empty) for c in range(8)] for r in range(8) ]

        for c in range(8):
            final[6][c] = PawnPiece((1, c), f"Pawn{c + 1}", ChessColor.WHITE)
            final[1][c] = PawnPiece((1, c), f"Pawn{c + 1}", ChessColor.BLACK)
        
        back: list[type[ChessPiece]] = [RookPiece, KnightPiece, BishopPiece, QueenPiece, KingPiece, BishopPiece, KnightPiece, RookPiece]
        ids: list[str] = ["Rook1", "Knight1", 'Bishop1', 'Queen', 'King', 'Bishop2', 'Knight2', 'Rook2']

        for c, (piece, name) in enumerate(zip(back, ids)):
            final[0][c] = piece((0, c), name, ChessColor.BLACK)
            final[7][c] = piece((7, c), name, ChessColor.WHITE)
        
        self._grid = final
    
    def _initialize_piece(self) -> None:
        if not self._grid:
            self._initialize_grid()

        for row in self.grid:
            for piece in row:
                if not piece.is_empty:
                    self._pieces[piece.color].append(piece.piece_id)
    
    @property
    def is_pvp(self) -> bool:
        return not (self._white_player.is_ai or self._black_player.is_ai)
    
    def get_view_grid(self) -> list[list[ChessPiece]]:
        # grid on curr_turn perspective
        white_pov: bool = True

        if self.is_pvp:
            white_pov = (self._turn == ChessColor.WHITE)
        else:
            white_pov = not self._white_player.is_ai
        
        if white_pov:
            return [list(row) for row in self._grid]
        else:
            return [list(reversed(row)) for row in reversed(self._grid)]
    
    def is_attack(self, row: int, col: int, opp_color: ChessColor) -> bool:
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if not piece.is_empty and piece.color == opp_color:
                    if (row, col) in piece.get_valid_moves(self._grid, None, None):
                        return True
        return False
    
    def find_piece(self, id: str) -> ChessPiece | None:
        for row in self._grid: # needs og piece
            for piece in row:
                if not piece.is_empty and piece.color == self._turn:
                    if piece.piece_id.lower() == id.lower():
                        return piece
        return None

    def get_last_opp_move(self) -> ChessMove | None:
        prev = self._moves_done[self._turn.opponent]
        return prev[-1] if prev else None
    
    def play_move(self, piece: ChessPiece, target_coord: tuple[int, int]) -> bool:
        last_opp_move = self.get_last_opp_move()
        valid_moves = piece.get_valid_moves(self._grid, last_opp_move, self.is_attack)

        if target_coord not in valid_moves: # invalid move
            return False
        
        fr, fc = piece.r, piece.c
        tr, tc = target_coord
        target = self._grid[tr][tc]
        is_capture = not target.is_empty
        move = MoveType.NORMAL
        char = piece.piece_id[0] if not piece.piece_id.startswith("Pawn") else "P"

        # castling
        if piece.piece_id == "King" and abs(fc - tc) == 2:
            if tc > fc: # castle kingside
                move = MoveType.CASTLE_KING
                rook = self._grid[tr][7]
                self._grid[tr][tc - 1] = rook
                self._grid[tr][7] = EmptyPiece((tr, 7), self._empty)
                rook.move((tr, tc - 1))
            else: # castle queen side
                move = MoveType.CASTLE_QUEEN
                rook = self._grid[tr][0]
                self._grid[tr][tc + 1] = rook
                self._grid[tr][0] = EmptyPiece((tr, 0), self._empty)
                rook.move((tr, tc + 1))
        
        # en passant
        elif char == 'P' and target.is_empty and fc != tc:
            move = MoveType.EN_PASSANT
            is_capture = True
            captured_pawn = self._grid[fr][tc]
            if captured_pawn.piece_id in self._pieces[captured_pawn.color]: # capture pawn
                self._pieces[captured_pawn.color].remove(captured_pawn.piece_id)
            self._grid[fr][tc] = EmptyPiece((fr, tc), self._empty) 
        
        # promote pawn to queen
        elif char == 'P' and (tr in (0, 7)):
            move = MoveType.PROMOTE
        
        if is_capture and move != MoveType.EN_PASSANT: 
            if target.piece_id in self._pieces[target.color]: # normal capture
                self._pieces[target.color].remove(target.piece_id)
        
        piece.move(target_coord)
        self._grid[tr][tc] = piece
        self._grid[fr][fc] = EmptyPiece((fr, fc), self._empty)

        if move == MoveType.PROMOTE:
            self._grid[tr][tc] = QueenPiece((tr, tc), f"Queen_Promoted_{tc}", piece.color)
        
        opp_color = self._turn.opponent
        king_coord = self.find_king(opp_color)
        is_check = self.is_attack(*king_coord, self._turn)
        is_mate = is_check and self.verify_checkmate(opp_color)

        move_record = ChessMove(char, (fr, fc), target_coord, move, is_capture, is_check, is_mate)
        self._moves_done[self._turn].append(move_record)

        if is_mate or "King" not in self._pieces[opp_color]:
            self._gameover = True
            self._winner = self._turn
        
        self._turn = opp_color
        return True

    def find_king(self, color: ChessColor) -> tuple[int, int]:
        for r in range(8):
            for c in range(8):
                p = self._grid[r][c]
                if p.piece_id == "King" and p.color == color:
                    return (r, c)
        return (0, 0)
    
    def verify_checkmate(self, color: ChessColor) -> bool:
        last_opp_move = self.get_last_opp_move()

        for r in range(8):
            for c in range(8):
                piece = self._grid[r][c]
                if not piece.is_empty and piece.color == color:
                    valid = piece.get_valid_moves(self._grid, last_opp_move, self.is_attack)
                    if valid: # there are valid moves left
                        return False 
        return True
    

        

    
