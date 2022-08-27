import numpy as np

row = 8
col = 8
left_border = top_border = 0
right_border = bottom_border = 7


class Piece:
    def __init__(self, starting_location: list, color: int, piece_movement):  # colors: 1=white , 2=black
        self.location = starting_location
        self.color = color

    # self.__movement = piece_movement  # should be a list of 2 integers, which possibly vary according to input

    def get_loc(self):
        return self.location

    def movement(self, piece_movement) -> (str):  # each possible move define how much to step at the row and col.
        if piece_movement == "black_pawn_moves":
            if Piece.get_loc()[0] == 1:
                possible_moves = [[2, 0], [1, 0]]
            else:
                possible_moves = [[1, 0]]
        elif piece_movement == "white_pawn_moves":
            if Piece.get_loc()[0] == 6:
                possible_moves = [[-2, 0], [-1, 0]]
            else:
                possible_moves = [[-1, 0]]
        elif piece_movement == "bishop_moves":
            possible_moves = self.bishop_moves()
        elif piece_movement == "rook_moves":
            possible_moves = self.rook_moves()
        elif piece_movement == "knight_jumps":
            possible_moves = self.knight_jumps
        elif piece_movement == "queen_moves":
            possible_moves = self.queen_moves()
        elif piece_movement == "king_moves":
            possible_moves = self.king_moves()
        return possible_moves

    def rook_moves(self):
        possible_moves = []
        loc = Piece.get_loc()
        while loc[0] < 7:
            loc[0] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[1] < 7:
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[0] > 0:
            loc[0] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[1] > 0:
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        return possible_moves

    def bishop_moves(self):  # להגדיר תנאי גבול על 4 רבעים של המרחב
        possible_moves = []
        loc = Piece.get_loc()
        while loc[0] < top_border and loc[1] < right_border:
            loc[0] += 1
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[0] < 7 and loc[1] > 0:
            loc[0] += 1
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[0] > 0 and loc[1] < 7:
            loc[0] -= 1
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = Piece.get_loc()
        while loc[0] > 0 and loc[1] > 0:
            loc[0] -= 1
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        return possible_moves

    def knight_jumps(self):  # need to fill
        pass

    def queen_moves(self):
        straight_line_moves = self.rook_moves()
        diagnol_moves = self.bishop_movement()
        return (straight_line_moves + diagnol_moves)

    def king_moves(self):  # need to fill
        pass


if __name__ == "__main__":  # preffered: change locations on the board not only in the piece location
    board = np.zeros((row, col))
    WB1 = Piece([-1, 2], 1, 'bishop_moves')
    BB1 = Piece([0, 2], 2, 'bishop_moves')
    WB2 = Piece([-1, 5], 1, 'bishop_moves')
    BB2 = Piece([0, 5], 2, 'bishop_moves')
    WR1 = Piece([-1, ], 1, 'rook_moves')
    BR1 = Piece([0, 0], 2, 'rook_moves')
    WR2 = Piece([-1, 7], 1, 'rook_moves')
    BR2 = Piece([0, 7], 2, 'rook_moves')
    WK1 = Piece([-1, 1], 1, 'knight_jumps')
    BK1 = Piece([0, 1], 2, 'knight_jumps')
    WK2 = Piece([-1, 6], 1, 'knight_jumps')
    BK2 = Piece([0, 6], 2, 'knight_jumps')
    WQ = Piece([-1, 4], 1, 'queen_moves')
    BQ = Piece([0, 4], 2, 'queen_moves')
    WKING = Piece([-1, 5], 1, 'king_moves')
    BKING = Piece([0, 5], 2, 'king_moves')
