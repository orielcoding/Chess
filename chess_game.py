import numpy as np


class Board:
    pass

    def turns(self):
        pass


class Game:

    def legal_move(self):  # move is legal if none of the pieces of the same color doesn't occupy the specific cube,
        # or one of the cubes leading to the specific cube from the current location of the moving piece
        # possibly needs to be defined inside movement method in Piece class.#
        # special case for the king
        pass

    def is_in_check(self):  # if the king occupies the way of one of piece possible movement steps from opposite color,
        # and none of the pieces of the kings color doesn't stand in the "way"- (way isn't defined currently).
        # this method defines new definition for legal move for the next "turn":
        # either the king must evacuate to one of his possible squares, or one of the pieces must stand in the "way"
        # of the attacking piece
        pass

    def is_in_checkmate(self):  # occure under the same condition as is_in_check but this time the kings evacuation
        # possibilities are illegal and there is no available piece to stand in the "way" of the attacking piece. 
        pass

    def el_passant(self):  # occur only when W pawn in the 5th line(4) and the B pawn in the 4th line(3),
        # and if neighbor of opposite color jumps 2 steps forward - a specific step takes place from pawn moves.
        pass

    def eat_piece(self):  # the piece which was in the cube to which the current piece stepped into disappear.
        pass

    def castling(self):  # can happen as long as there isn't current check/the king pass underneath check,
        # and as long as the king or rook hasn't moved yet.
        pass

    def promotion(self):  # occur when a W/B pawn reach the top/bottom border accordingly.
        pass
