# pyright: strict

from __future__ import annotations
import random

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
    
    
        

    
