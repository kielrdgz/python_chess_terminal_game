# pyright: strict

from enum import StrEnum, auto, Enum
from typing import Protocol, Any

class ChessColor(StrEnum):
    WHITE = "WHITE"
    BLACK = "BLACK"
    NA = "NA"

    def opponent(self) -> ChessColor:
        return ChessColor.BLACK if self == ChessColor.WHITE \
    else ChessColor.WHITE if ChessColor.WHITE else ChessColor.NA
    
class PieceType(StrEnum):
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"

class MoveType(Enum):
    NORMAL = auto()
    EN_PASSANT = auto()
    CASTLE_KING = auto()
    CASTLE_QUEEN = auto()
    PROMOTE = auto()

class Player(Protocol):
    def name(self) -> str:
        ...
    
    def is_ai(self) -> bool:
        ...

# class BaseChessPiece:
#     @property
#     def is_empty(self) -> bool:
#         ...

#     @property
#     def color(self) -> ChessColor:
#         ...

class ChessPiece:
    def __init__(self, coord: tuple[int, int], piece_id: str, color: ChessColor) -> None:
        self.r, self.c = coord
        self.piece_id = piece_id
        self._color = color
        self._has_moved: bool = False

    @property
    def is_empty(self) -> bool:
        return False

    @property
    def color(self) -> ChessColor:
        return self._color
    
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        ...
    
    def move(self, to_coord: tuple[int, int]) -> None:
        ...
    

    def __repr__(self) -> str:
        color = 'W' if self.color == ChessColor.WHITE else 'B'
        return f"{color}_{self.piece_id}"
    
class EmptyPiece(ChessPiece):
    def __init__(self, coord: tuple[int, int], piece_id: str) -> None:
        super().__init__(coord, piece_id, ChessColor.NA)
    
    @property
    def is_empty(self) -> bool:
        return True

class ChessMove:
    def __init__(self, piece: str, _from: tuple[int, int], 
                _to: tuple[int, int], 
                move: MoveType = MoveType.NORMAL, 
                is_capture: bool = False, 
                is_check: bool = False, 
                is_checkmate: bool = False,) -> None:
        self.piece = piece
        self._to = _to
        self._from = _from
        self.move = move
        self.is_capture = is_capture
        self.is_checkmate = is_checkmate
        self.is_check = is_check
    
    def coords_to_notation(self, coord: tuple[int, int]) -> str:
        row, col = coord
        col_letters = 'abcdefgh'
        row_nums = '87654321'
        return f"{col_letters[col]}{row_nums[row]}"

    def __repr__(self) -> str:
        # handle chess move notation 
        match self.move:
            case MoveType.CASTLE_KING:
                notation = "O-O"
            case MoveType.CASTLE_QUEEN:
                notation = "O-O-O"
            case _ :
                to_square = self.coords_to_notation(self._to)
                prefix = "" if self.piece == 'P' else self.piece

                if self.is_capture:
                    if self.piece == 'P':
                        from_square = self.coords_to_notation(self._from)
                        prefix = from_square[0]
                    prefix += "x"
                
                notation = f"{prefix}{to_square}"

                if self.move == MoveType.PROMOTE:
                    notation += "=Q"

        if self.is_checkmate:
            notation += "#"
        elif self.is_check:
            notation += "+"
        
        return notation

def move_finder(coords: tuple[int, int], directions: list[tuple[int, int]], grid: list[list[ChessPiece]], opp_color: ChessColor, repeat: bool = True) -> set[tuple[int, int]]:
    moves: set[tuple[int, int]] = set()
    r, c = coords

    if repeat:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8: # hard coded but chess board won't change size anw
                target: ChessPiece = grid[nr][nc]
                if target.is_empty:
                    moves.add((nr, nc))
                elif target.color == opp_color:
                    moves.add((nr, nc)) # can take piece
                    break
                else:
                    break
                # break: stop finding new pieces
                nr += dr
                nc += dc
        
        return moves
    else:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target: ChessPiece = grid[nr][nc]
                if target.is_empty or target.color == opp_color:
                    moves.add((nr, nc))
        
        return moves
    
class RookPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        return move_finder((self.r, self.c), directions, grid, self.color.opponent())

class QueenPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        directions =  [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        return move_finder((self.r, self.c), directions, grid, self.color.opponent())

class KnightPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        return move_finder((self.r, self.c), directions, grid, self.color.opponent(), repeat=False)

class BishopPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        return move_finder((self.r, self.c), directions, grid, self.color.opponent())

class PawnPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        moves: set[tuple[int, int]] = set()
        direction = -1 if self.color == ChessCOlor.WHITE else 1

        next_r = self.r + direction
        if 0 <= next_r < 8 and grid[next_r][self.c].is_empty:
            moves.add((next_r, self.c))
            
            # handle first 2 step of pawn
            start_r = 6 if self.color == ChessColor.WHITE else 1
            two_step = self.r + (2 * direction)
            if self.r == start_r and grid[two_step][self.c].is_empty:
                moves.add(two_step, self.c)

        for dc in [-1, 1]:
            next_c = self.c + dc
            if 0 <= next_r < 8 and 0 <= next_c < 8:
                target: ChessPiece = grid[next_r][next_c]
                if not target.is_empty and target.color == self.color.opponent():
                    moves.add((next_r, next_c))

                # handle en passant
                if target.is_empty and last_move is not None:
                    adj_piece = grid[self.r][next_c] 
                    if not adj_piece.is_empty and adj_piece.piece_id.startswith("Pawn") and adj_piece.color == self.color.oppoennt() and last_move._to == (self.r, next_c) and abs(last_move._from[0] - last_move.to[0]) == 2:
                        moves.add((next_r, next_c))
        
        return moves

class KingPiece(ChessPiece):
    def get_valid_moves(self, grid: list[list[ChessPiece]], last_move: ChessMove | None = None, is_attacked_fn: Any = None) -> set[tuple[int, int]]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        moves: set[tuple[int, int]] = move_finder((self.r, self.c), directions, grid, self.color.opponent(), repeat=False)

        if not self._has_moved and is_attacked_fn is not None:
            opp_color = self.color.opponent()

            if not is_attacked_fn(self.r, self.c, opp_color):
                if grid[self.r][self.c + 1].is_empty and grid[self.r][self.c + 2].is_empty:
                    rook = grid[self.r][7]
                    if not rook.is_empty and not rook._has_moved and rook.piece_id.startswith("Rook") and not is_attacked_fn(self.r, self.c + 1, opp_color) and not is_attacked_fn(self.r, self.c + 2, opp_color):
                        moves.add((self.r, self.c + 2))
                
                if grid[self.r][self.c - 1].is_empty and grid[self.r][self.c - 2].is_empty and grid[self.r][self.c - 3].is_empty:
                    rook = grid[self.r][0]
                    if not rook.is_empty and not rook._has_moved and rook.piece_id.startswith("Rook") and not is_attacked_fn(self.r, self.c - 1, opp_color) and not is_attacked_fn(self.r, self.c - 2, opp_color):
                        moves.add((self.r, self.c - 2))
        
        return moves




