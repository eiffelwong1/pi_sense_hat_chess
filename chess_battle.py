import time
import math
import random

import chess
from sense_hat import SenseHat

#TODO: make random best move if have multiple move with same score

#TODO: make a elo score

P_COLOR = {
        'p':(255,0,0),
        'r':(255,51,0),
        'n':(255,102,0),
        'b':(255,153,0),
        'q':(255,204,0),
        'k':(255,255,0),

        'P':(0,0,255),
        'R':(0,51,255),
        'N':(0,102,255),
        'B':(0,153,255),
        'Q':(0,204,255),
        'K':(0,255,255),

        '.':(0,0,0)
}

P_SCORE = {
        chess.PAWN: 1,
        chess.ROOK: 4,
        chess.KNIGHT: 4,
        chess.BISHOP: 4,
        chess.QUEEN:8,
        chess.KING:100,
        }

class player():
    def get_move(self):
        raise NotImplementedError

class random_player(player):
    def get_move(self, board):
        return random.choice(list(board.legal_moves))

class min_max_player(player):
    def __init__(self, depth):
        self.depth = depth

    def get_move(self, board):
        assert bool(board.legal_moves)
        value = -math.inf
        best_move = None

        for move in board.legal_moves:
            moved_board = board.copy(stack=False)
            moved_board.push(move)
            temp_value = self.min_max(moved_board, board.turn, self.depth -1)
            if temp_value > value:
                best_move = move
                value = temp_value
        return best_move

    def board_score(self, board, color):
        score = 0
        for p, p_score in P_SCORE.items():
            score += len(board.pieces(p, color)) * p_score
            score -= len(board.pieces(p, color)) * p_score
        return score
    
    def min_max(self, board, player_side, depth):
        #return condition: no legal move or depth = 0
        assert board is not None
        if depth <= 0 or not bool(board.legal_moves):
            return self.board_score(board, player_side)
        
        if player_side == board.turn:
            #maxmizing score
            value = -math.inf
            for move in board.legal_moves:
                moved_board = board.copy(stack=False)
                moved_board.push(move)
                value = max(self.min_max(moved_board, player_side, depth-1), value)
            return value
        else:
            #minimizing score
            value = math.inf
            for move in board.legal_moves:
                moved_board = board.copy(stack=False)
                moved_board.push(move)
                value = min(self.min_max(moved_board, player_side, depth-1), value)
            return value

def print_board_to_sense_hat():
    for i, p in enumerate("".join(str(board).split())): 
        sense.set_pixel(i%8, int(i/8), P_COLOR[p])

sense = SenseHat()
sense.clear()
board = chess.Board()
p1 = min_max_player(2)
p2 = random_player()
while not board.is_game_over():
    if board.turn == chess.WHITE:
        move = p1.get_move(board)
    else:
        move = p2.get_move(board)
    board.push(move)
    print_board_to_sense_hat()


print(board.result())

