# pyright: strict

from __future__ import annotations
from data_types import *

class ChessModel:
    def __init__(self, p1: Player, p2: Player, empty: str, chosen: str) -> None:
        # chosen: "BLACK", "WHITE", "RANDOM" -> chosen color of player 1
        self._r: int = 8
        self._c: int = 8
        self._p1 = p1
        self._p2 = p2
        self._chosen = chosen

        self._grid: list[list[ChessPieceProtocol]] = [[]]
        self._initialize_grid()

        self._empty: str = empty 

        self._pieces: dict[str, list[str]] = {} # key: players, values: pieces present
        self._initialize_pieces()

        self._turn: ChessColor = ChessColor.WHITE
        self._gameover: bool = False
        self._winner: ChessColor | None = None
        self._moves_done: list[list[ChessMove]] = [[]]

    @property
    def row(self) -> int:
        return self._r
    
    @property
    def col(self) -> int:
        return self._c
    
    @property
    def empty(self) -> str:
        return self._empty

    def _initialize_grid(self) -> None:
        final = [[EmptyPiece(self.empty) * self.col] for _ in range(self.row) ]

        top = [RookPiece, KnightPiece, ]

        self._grid = final
    
