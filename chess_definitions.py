import numpy as np
from typing import NewType

Locations_List = NewType('Locations_List', list[tuple[int, int]])
Location = NewType("Location", tuple[int, int])

left_border = top_border = 0
right_border = bottom_border = 7


def create_board():
    board = np.zeros([8, 8])
    return board


class NotInBoardError(ValueError):
    pass


class Piece:
    color_dict = {0: "W", 1: "B"}

    def __init__(self, color: int):
        # i will generate Piece object only when starting the game / doing promotion
        # TODO CHECK THAT ENTERING INIT METHOD WHEN PROMOTING DOESNT OVERRIDES ANYTHING
        self.color = color

    def __str__(self):
        return f"{self.color_dict[self.color]}_{type(self).__name__[0:2]}"  # todo change if needed

    def __repr__(self):
        return f"{self.color_dict[self.color]}_{type(self).__name__[0:2]}"

    def __eq__(self, other):
        return type(self) == type(other) and self.color == other.color

    def sign_vector(self):
        pass


class Pawn(Piece):
    def sign_vector(self) -> np.array:  # todo add eating case
        color_sign = {0: -1, 1: 1}
        return color_sign[self.color] * np.array((1, 0))

    # def uniqe_color_condition(self,current_color, target_color) -> bool:
    #     if target_color is not None and target_color != current_color:
    #         return False
    #     return True
    #

class Rook(Piece):
    def sign_vector(self):
        straight_lines = np.array(((1, 0), (-1, 0), (0, 1), (0, -1)))
        return straight_lines


class Bishop(Piece):
    def sign_vector(self):
        diagonals = np.array(((1, 1), (-1, 1), (1, -1), (-1, -1)))
        return diagonals


class Knight(Piece):
    def sign_vector(self):
        return np.array(((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)))


class Queen(Piece):
    def sign_vector(self):
        return np.array(((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)))


class King(Piece):
    def sign_vector(self):
        return np.array(((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)))


class Board:
    def __init__(self, row_size: int, column_size: int):
        self.board_matrix = np.empty([row_size, column_size], dtype=object)

    def get_square_state(self, location: Location) -> Piece:
        return self.board_matrix[location]  # supposed to return an instance of Piece object, or None

    def set_initial_squares(self, location: Location, piece: Piece):
        self.board_matrix[location] = piece

    def set_square_state(self, locations: Locations_List, piece: Piece = None):  # None default takes care of en-passant
        self.board_matrix[locations[0]] = None  # the current square
        if piece:
            self.board_matrix[locations[1]] = piece

    def __str__(self):
        np.set_printoptions(linewidth=120)
        return str(self.board_matrix)


class Coordinates:
    def __init__(self, locations: Locations_List):
        self.curr_location: Location = locations[0]
        self.vector: np.array = np.array(locations[1]) - np.array(locations[0])
        self.sign_vector: np.array = np.sign(self.vector)

    def squares_path_for_validation(self) -> np.ndarray:
        available_distance: np.ndarray = np.array(
            [np.multiply(self.sign_vector, np.array([i, i])) for i in range(1, max(abs(self.vector)+1))])
        squares = np.array(self.curr_location) + available_distance
        return squares

    def squares_path_for_protection(self) -> np.ndarray:
        available_distance: np.ndarray = np.array(
            [np.multiply(self.sign_vector, np.array([i, i])) for i in range(0, max(abs(self.vector)))])
        squares = np.array(self.curr_location) + available_distance
        return squares