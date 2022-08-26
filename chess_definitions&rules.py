import numpy as np

# class Board:
#     BOARD_SIZE = np.zeros([8, 8])
#
#     def __init__(self):
#         self.board = BOARD_SIZE

row=8
col=8

class Piece_movement:
    def __init__(self,moves):
        pass

    def movement(self,moves):
        if moves == "pawn_moves":
            possible_moves = 
        elif moves == "bishop_moves":
            possible_moves =
        elif moves == "rook_moves"
            possible_moves =
        elif moves == "knight_jumps"
            possible_moves =
        elif moves == "queen_moves"
            possible_moves =
        elif moves == "king_moves"
            possible_moves =



class Piece:
    def __init__(self, name, starting_location: list, piece_movement):
        self.name = name
        self.location = starting_location
        self.__movement = piece_movement  # should be a list of 2 integers, which possibly vary according to input

    def get_loc(self):
        return self.location



if __name__ == "__main__":
    board = np.zeros((row, col))
    WB1 = Piece('WB1', [-1, 2], 'bishop_moves')
    BB1 = Piece('BB1', [0, 2], 'bishop_moves')
    WB2 = Piece('WB2', [-1, 5], 'bishop_moves')
    BB2 = Piece('BB2', [0, 5], 'bishop_moves')
    WR1 = Piece('WR1', [-1, ], 'rook_moves')
    BR1 = Piece('BR1', [0, 0], 'rook_moves')
    WR2 = Piece('WR2', [-1, 7], 'rook_moves')
    BR2 = Piece('BR2', [0, 7], 'rook_moves')
    WK1 = Piece('WK1', [-1, 1], 'knight_jumps')
    BK1 = Piece('BK1', [0, 1], 'knight_jumps')
    WK2 = Piece('WK2', [-1, 6], 'knight_jumps')
    BK2 = Piece('BK2', [0, 6], 'knight_jumps')
    WQ = Piece('WQ', [-1, 4], 'queen_moves')
    BQ = Piece('BQ', [0, 4], 'queen_moves')
    WKING = Piece('WKING', [-1, 5], 'king_moves')
    BKING = Piece('BKING', [0, 5], 'king_moves')




# for i in range(row):
#     BP=Pieces(f'BP{i}',[1,i],[1,i+1])


# class Move_pieces(Piece):
