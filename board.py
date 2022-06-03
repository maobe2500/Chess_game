import itertools
import os
from more_itertools import consume
from piece import Piece

class Board:
    def __init__(self, rect_size):
        self.rows = '87654321'
        self.cols = 'abcdefgh'
        self.rect_size = rect_size
        self.fen_string = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2' #'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.active_color = ''
        self.castle_string = ''
        self.en_passant = ''
        self.halfmove_clock = ''
        self.fullmove_clock = ''
        self.positions = {}

        self.moves = []
        self.xy_to_chess = {}   # This is used for displaying moves in chess notation
        self.setup_translation()
        self.setup_starting_pos()

    # Setup translation tables for xy-coordinates to chess-coordinates and vice versa
    def setup_translation(self):
        i = 0
        for row in self.rows:
            j = 0
            for col in self.cols:
                self.xy_to_chess[(j*self.rect_size + self.rect_size/2, i*self.rect_size + self.rect_size/2)] = col + row
                j += 1
            i += 1


    # Sets up the starting positions using the fen string
    # The set up positions will be the "positions" dict and
    # the values will be the Piece objects
    def setup_starting_pos(self):
        rows, active_color, castle_sting, en_passant, halfmove_clock, fullmove_clock = self.fen_string.split(' ')
        self.active_color = active_color
        self.castle_string = castle_sting
        self.en_passant = en_passant
        self.halfmove_clock = halfmove_clock
        self.fullmove_clock = fullmove_clock
        i = 0
        for row in rows.split('/'):
            cols = list(range(8))
            print(row)
            j = 0
            for code in row:
                print(j, code)
                pos = (j*self.rect_size + self.rect_size/2, i*self.rect_size + self.rect_size/2)
                if code.isdigit():
                    number_of_skips = int(code)

                    print(f'skipping {number_of_skips} cols')
                    cols[j:j+number_of_skips] = ['X' for _ in range(number_of_skips)]
                    print(cols)
                    j += number_of_skips

                else:
                    self.positions[pos] = self.make_piece(code, pos)
                    j += 1
                #print(self.positions)
            i += 1


    def check_castle():
        return None

    def check_en_passant():
        return None

    def update(self, piece, pos):
        self.active_color = None
        self.castle_string = check_castle()
        self.en_passant = check_en_passant()
        self.halfmove_clock = None
        self.fullmove_clock = None
        
        



    # Initializes a Piece object with a fen name and position
    # and returns the piece
    def make_piece(self, fen_name, pos):
        directory = './GUI/pngs'
        for filename in os.listdir(directory):
            if fen_name == filename[0]:
                color = 'w' if fen_name.isupper() else 'b'
                piece = Piece(pos, color, fen_name, directory + '/' + filename)

                return piece
                


        

