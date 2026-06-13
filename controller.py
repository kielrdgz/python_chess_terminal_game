# pyright: strict

from __future__ import annotations
from argparse import ArgumentParser
import random

from view import *
from model import *
from data_types import *

def chess_args() -> tuple[str, str]:
    parser = ArgumentParser(description='Game Settings')

    parser.add_argument('-o', choices = ['enemyai', 'player'], required=True, help='Choose opponent')
    parser.add_argument('-t', choices=['choose', 'random'], required=True, help='Choose turn-basis')
    # parser.add_argument('-f', choices=['1', '2'], help='Required only if turn-basis is not random')
    # parser.add_argument('c', choices = [enemies...], help='Required only if AI opponent')
    
    arguments = parser.parse_args()

    opponent = arguments.o
    turn_base = arguments.t
    # first_turn = arguments.f

    return (turn_base, opponent)

def ChessModel_factory(args: tuple[str, str], view: ChessView) -> ChessModel:
    enemy_choices = {
        'normal': ChessNormalEnemy,
    }

    turn_base, opponent = args
    chosen = 'white'

    # player chooses color
    if turn_base == 'choose':
        turn = view.configure_turn()
        if turn != 1:
            chosen = 'black'
    # random color given
    else:
        chosen = random.choice(['white', 'black'])

    # player vs ai
    # DISCLAIMER: no names yet huhu
    if opponent == 'enemyai':
        chess_ai = view.configure_enemy(enemy_choices)
        if chosen == 'white':
            p1 = ChessPlayer(ChessColor.WHITE, 'p1')
            p2 = chess_ai(ChessColor.BLACK, 'normalai')
            players = [p1, p2]
        else:
            p1 = ChessPlayer(ChessColor.BLACK, 'p1')
            p2 = chess_ai(ChessColor.WHITE, 'normalai')
            players = [p2, p1]
    # pvp
    else:
        if chosen == 'white':
            p1 = ChessPlayer(ChessColor.WHITE, 'p1')
            p2 = ChessPlayer(ChessColor.BLACK, 'p2')
            players = [p1, p2]
        else:
            p1 = ChessPlayer(ChessColor.BLACK, 'p1')
            p2 = ChessPlayer(ChessColor.WHITE, 'p2')
            players = [p2, p1]

    p1, p2 = players

    return ChessModel(p1, p2, '.', chosen)

class ChessController:
    def __init__(self, view: ChessView) -> None:
        self._model = ChessModel_factory(chess_args(), view)
        self._view = view
    
    def run(self) -> None:
        model, view = self._model, self._view

        while not model.gameover:
            curr_turn = model.turn
            view.display_turn(curr_turn)
            view.display_grid(model.get_view_grid(), curr_turn, model.empty)
            
            active_player = model.active_player
            target_piece = None
            target_coord = (-1, -1) # placeholder
            last_opp_move = model.get_last_opp_move()

            if active_player.is_ai:
                ai_move = active_player.get_move(model.grid, model.is_attack, last_opp_move)
                if ai_move is None:
                    print('This should not print')
                    print('If this prints, game should be over')
                    break
                target_piece, target_coord = ai_move
            else:
                while True:
                    valid_ids = [piece.piece_id for row in model.grid for piece in row if not piece.is_empty and piece.color == curr_turn]
                    piece_id_str = view.ask_for_piece(valid_ids)
                    target_piece = model.find_piece(piece_id_str)

                    if not target_piece:
                        continue
                    
                    valid_moves = target_piece.get_valid_moves(model.grid, last_opp_move, model.is_attack)
                    if not valid_moves:
                        view.display_invalid_piece()
                        continue
                    r, c = view.ask_for_move(valid_moves)
                    if -1 in (r, c):
                        continue # cancel move
                    
                    target_coord = (r, c)
                    break   

            if target_piece and target_coord != (-1, -1):
                tr, tc = target_coord
                target = model.grid[tr][tc]
                is_capture = not target.is_empty
                success = model.play_move(target_piece, target_coord)

                if success:
                    last_move = model.moves_done[curr_turn][-1]
                    # view.display_grid(model.get_view_grid(), model.turn, model.empty)
                    view.display_move(last_move, tr, tc, target, is_capture)
        
        view.display_winner(model.winner, model.winner_player)
        view.display_grid(model.get_view_grid(), model.turn, model.empty)
        view.display_moves_done(model.moves_done)