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

    # לברר מה ההבדל בלקרוא למתודה דרך self או דרך הקלאס

    def get_location(self):
        return self.location

    def set_location(self, piece_movement) -> (str):  # each possible move define how much to step at the row and col.
        # must add the condition of a piece blockading the route to specific cube, which makes it illegal.
        if piece_movement == "black_pawn_moves":
            if self.get_location()[0] == 1:
                possible_moves = [[2, 0], [1, 0]]
            else:
                possible_moves = [[1, 0]]
        elif piece_movement == "white_pawn_moves":
            if self.get_location()[0] == 6:
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
        loc = self.get_location()
        while loc[0] < 7:
            loc[0] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[1] < 7:
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > 0:
            loc[0] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[1] > 0:
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        return possible_moves

    def bishop_moves(self):
        possible_moves = []
        loc = self.get_location()
        while loc[0] < top_border and loc[1] < right_border:
            loc[0] += 1
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] < 7 and loc[1] > 0:
            loc[0] += 1
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > 0 and loc[1] < 7:
            loc[0] -= 1
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > 0 and loc[1] > 0:
            loc[0] -= 1
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        return possible_moves

    def knight_jumps(self):
        possible_moves = []
        loc = self.get_location()
        while loc[0] < top_border - 1 and loc[1] < right_border:
            loc[0] += 2
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] < top_border and loc[1] < right_border - 1:
            loc[0] += 1
            loc[1] += 2
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] < top_border - 1 and loc[1] > left_border:
            loc[0] += 2
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] < top_border and loc[1] > left_border + 1:
            loc[0] += 1
            loc[1] -= 2
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > bottom_border + 1 and loc[1] < right_border:
            loc[0] -= 2
            loc[1] += 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > bottom_border and loc[1] < right_border - 1:
            loc[0] -= 1
            loc[1] += 2
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > bottom_border + 1 and loc[1] > left_border:
            loc[0] -= 2
            loc[1] -= 1
            possible_moves.append([loc[0], loc[1]])
        loc = self.get_location()
        while loc[0] > bottom_border and loc[1] > left_border + 1:
            loc[0] -= 1
            loc[1] -= 2
            possible_moves.append([loc[0], loc[1]])
        return possible_moves

    def queen_moves(self):
        straight_line_moves = self.rook_moves()
        diagnol_moves = self.bishop_movement()
        return (straight_line_moves + diagnol_moves)

    def king_moves(self):  # need to fill #special case of stepping into check.
        pass


class Moves:
    def __int__(self, loc: list):
        self.row = loc[0]
        self.column = loc[1]

    def find_diagonal(self):  # מתייחס למיקום של חייל ולא למיקום של משבצת
        if self.row < self.column:
            return self.column - self.row
        else:
            return 0

    def diagonal(self):  # must test it
        axis = self.find_diagonal()
        diag = np.diagonal(board, axis=axis)

    def flipped_diagonal(self):  # must test it
        flipped_board = np.fliplr(board)
        distance = abs(self.row - 4)
        if self.row < 4:
            self.row = self.row + distance
        else:
            self.row = self.row - distance

        axis = self.find_diagonal()
        diagonal_indices = []
        for index, x in np.ndenumerate(board, axis=axis):
            # diag = np.diagonal(board, axis=axis)
            diagonal_indices.append(index)
        return diagonal_indices


if __name__ == "__main__":  # preffered: change locations on the board not only in the piece location
    #####NEED TO DEFINE PAWNS#####
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
    WP1 = Piece([6,0],1,'white_pawn_moves')
    WP2 = Piece([6, 1], 1, 'white_pawn_moves')
    WP3 = Piece([6, 2], 1, 'white_pawn_moves')
    WP4 = Piece([6, 3], 1, 'white_pawn_moves')
    WP5 = Piece([6, 4], 1, 'white_pawn_moves')
    WP6 = Piece([6, 5], 1, 'white_pawn_moves')
    WP7 = Piece([6, 6], 1, 'white_pawn_moves')
    WP8 = Piece([6, 7], 1, 'white_pawn_moves')
    BP1 = Piece([1, 0], 2, 'black_pawn_moves')
    BP2 = Piece([1, 1], 2, 'black_pawn_moves')
    BP3 = Piece([1, 2], 2, 'black_pawn_moves')
    BP4 = Piece([1, 3], 2, 'black_pawn_moves')
    BP5 = Piece([1, 4], 2, 'black_pawn_moves')
    BP6 = Piece([1, 5], 2, 'black_pawn_moves')
    BP7 = Piece([1, 6], 2, 'black_pawn_moves')
    BP8 = Piece([1, 7], 2, 'black_pawn_moves')



