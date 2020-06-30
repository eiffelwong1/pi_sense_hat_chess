import time
import random

import chess
from sense_hat import SenseHat

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


while True:
    sense = SenseHat()
    sense.clear()
    board = chess.Board()
    while not board.is_game_over():

        for i, p in enumerate("".join(str(board).split())): 
            sense.set_pixel(i%8, int(i/8), P_COLOR[p])
        print(list(board.legal_moves))
        board.push(random.choice(list(board.legal_moves)))
