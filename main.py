# pyright: strict

from __future__ import annotations
from controller import *
# from model import *
from view import *

if __name__ == '__main__': # chess ver
    controller = ChessController(ChessView(styled=True))
    controller.run()