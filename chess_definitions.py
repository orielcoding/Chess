import numpy as np

left_border = top_border = 0
right_border = bottom_border = 7


def create_board():
    board = np.zeros([8, 8])
    return board


class PathError(ValueError):
    pass


class Piece:
    color_dict = {0: "white", 1: "black"}
    def __init__(self, color: int):
        # i will generate Piece object only when starting the game / doing promotion
        # TODO CHECK THAT ENTERING INIT METHOD WHEN PROMOTING DOESNT OVERRIDES ANYTHING
        self.color = color

    def __repr__(self):
        return f"{Piece.color_dict[self.color]}_{type(self)}"  # todo change if needed

    def sign_vector(self):
        pass


class Pawn(Piece):
    def sign_vector(self) -> tuple:   # todo add eating case
        color_sign = {0: -1, 1: 1}
        return color_sign[self.color] * (1, 0)


class Rook(Piece):
    def sign_vectors(self):
        straight_lines = np.array((1, 0), (-1, 0), (0, 1), (0, -1))
        return straight_lines


class Bishop(Piece):
    def sign_vectors(self):
        diagonals = np.array((1, 1), (-1, 1), (1, -1), (-1, -1))
        return diagonals


class Knight(Piece):
    def sign_vector(self):
        return np.array((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))


class Queen(Piece):
    def sign_vector(self):
        return np.array((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))


class King(Piece):
    def sign_vector(self):
        return np.array((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))


class Board:
    def __init__(self, row_size: int, column_size: int):
        self.board_matrix = np.empty([row_size, column_size], dtype=object)

    def get_square_state(self, location: tuple) -> Piece:  # returns what's located in specific square
        return self.board_matrix[location]  # supposed to return an instance of Piece object, or None

    def set_initial_squares(self, location: tuple, piece: Piece):
        self.board_matrix[location] = piece

    def set_square_state(self, location: tuple, piece: Piece):  # todo check function
        # piece object should contain the type and color of the piece
        # location contains the user's input: current square and target square
        self.board_matrix[location[0]] = None  # the current square
        self.board_matrix[location[1]] = None

    def __str__(self):  # todo decorate butyfi
        return str(self.board_matrix)


class Coordinates:
    def __init__(self, location: tuple):
        self.curr_location = np.array(location[0])
        self.vector = np.array(location[1]) - np.array(location[0])
        self.sign_vector = np.sign(self.vector)

    def squares_path(self):
        distance = [np.multiply(self.sign_vector, np.array([i, i])) for i in range(8 - max(self.curr_location))]
        squares = self.curr_location + distance
        return squares

