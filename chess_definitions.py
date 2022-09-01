import numpy as np

left_border = top_border = 0
right_border = bottom_border = 7


def create_board():
    board = np.zeros([8, 8])
    return board


class Square:  # TODO FILL MEMBER OF THREATS AFTER DEFINING THE MOVEMENTS_TYPES IN NUMPY
    def __init__(self, location: list, color=None, piece_type=None):
        # default values None if the square isn't occupied.
        self.type = piece_type
        self.color = color
        self.location = location

    def get_type(self):
        return self.type

    def get_color(self):
        return self.color

    def set_type_and_color(self, new_type: str = None, new_color: int = None):
        # default values None if the square isn't occupied.
        # they both change every move for the requested square
        self.type = new_type
        self.color = new_color

    def threats(self):
        pass  # TODO FUNCTION GETS MOVEMENT TYPES AND RETURN LIST OF THREATENING SQUARES TO BE MAPPED?


class Board:
    def __init__(self, row_size: int, column_size: int):
        self.board_matrix = np.zeros([row_size, column_size])
        for row in self.board_matrix:
            for column in row:
                self.board_matrix[row, column] = None  # TODO FILL IN THE RELEVANT PARAMETERS

    def get_square_state(self, location: list):  # returns what's located in specific square
        return self.board_matrix[location]  # supposed to return an instance of Piece object, or None

    def set_square_state(self, location: list, piece: object):
        # piece object should contain the type and color of the piece
        # location contains the user's input: current square and target square
        self.board_matrix[location[0]] = None  # the current square
        self.board_matrix[location[1]] = Square(location[1]).set_type_and_color(piece.type,piece.color)  # the target square


class Piece:
    def __init__(self, piece_type: str, starting_location: list, color: int):  # colors: 0=white , 1=black
        self.location = starting_location
        self.color = color
        self.type = piece_type

    def get_location(self):
        return self.location

    def white_pawn(self): # todo add case of eating
        if self.get_location()[0] == 6:
            possible_moves = [[-2, 0], [-1, 0]]
        else:
            possible_moves = [[-1, 0]]
        return possible_moves

    def black_pawn(self):  # todo add case of eating
        if self.get_location()[0] == 1:
            possible_moves = [[2, 0], [1, 0]]
        else:
            possible_moves = [[1, 0]]
        return possible_moves

    def rook(self):
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

    def bishop(self):
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

    def knight(self):
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

    def queen(self):
        straight_line_moves = self.rook()
        diagnol_moves = self.bishop_movement()
        return (straight_line_moves + diagnol_moves)

    def king(self):  # need to fill #special case of stepping into check.
        loc = self.get_location()
        possible_moves = [[loc[0] + 1, loc[1]], [loc[0] - 1, loc[1]], [loc[0], loc[1] + 1], [loc[0], loc[1] - 1],
                          [loc[0] + 1, loc[1] + 1], [loc[0] + 1, loc[1] - 1], [loc[0] - 1, loc[1] + 1],
                          [loc[0] - 1, loc[1] - 1]]
        return possible_moves

    def available_squares(self, piece_movement: str):
        if piece_movement == "black_pawn_moves":
            possible_moves = self.black_pawn()
        elif piece_movement == "white_pawn_moves":
            possible_moves = self.white_pawn()
        elif piece_movement == "bishop_moves":
            possible_moves = self.bishop()
        elif piece_movement == "rook_moves":
            possible_moves = self.rook()
        elif piece_movement == "knight_jumps":
            possible_moves = self.knight
        elif piece_movement == "queen_moves":
            possible_moves = self.queen()
        elif piece_movement == "king_moves":
            possible_moves = self.king()
        return possible_moves

    # def set_piece_location(self, piece_movement: str, current_square: list): # this function will be called only after validation
    #     Board.set_square_state() = [self.type, self.color]


class MovementTypes:
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
        diag = np.diagonal(create_board(), axis=axis)

    def flipped_diagonal(self):  # must test it
        flipped_board = np.fliplr(create_board())
        distance = abs(self.row - 4)
        if self.row < 4:
            self.row = self.row + distance
        else:
            self.row = self.row - distance

        axis = self.find_diagonal()
        diagonal_indices = []
        # for index, x in np.ndenumerate(board, axis=axis):
        #     # diag = np.diagonal(board, axis=axis)
        #     diagonal_indices.append(index)
        # return diagonal_indices
