import numpy as np
import re
import chess_definitions


class Game:
    def __init__(self):
        self.board = chess_definitions.Board.create_board()
        self.piece = chess_definitions.Piece
        self.color_turn = 0

    def enter_move(self, color: int):
        color_dictionary = {0: "White's turn: ", 1: "Black's turn: "}
        move = input(f"{color_dictionary[color]} enter move. format example: A2->A3")
        return move

    def move_is_in_board(self, color, move):  # if an input is an existing square, returns the square as int list
        a = re.match('([a-hA-H][1-8])[, \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move)
        if a:
            location = lambda locStr: ([ord(locStr[0, 0].lower()) - ord("a"), int(locStr[0, 1]) - 1],
                                       [ord(locStr[1, 0].lower()) - ord("a"), int(locStr[1, 1]) - 1])
            return location(a)
        raise ValueError('ileggal square was entered, please enter existing square')

    def color_move_validation(self,color):
        pass

    def legal_move(self, Turn):  # whether specific piece can act, additional to the other conditions.
        '''# move is legal if none of the pieces of the same color doesn't occupy the specific cube,
        # or one of the cubes leading to the specific cube from the current location of the moving piece
        # possibly needs to be defined inside movement method in Piece class.#
        # special case for the king'''
        pass

    def is_in_check(self):
        '''# if the king occupies the way of one of piece possible movement steps from opposite color,
        # and none of the pieces of the kings color doesn't stand in the "way"- (way isn't defined currently).
        # this method defines new definition for legal move for the next "turn":
        # either the king must evacuate to one of his possible squares, or one of the pieces must stand in the "way"
        # of the attacking piece'''
        # returns boolean
        pass

    def is_in_checkmate(self):
        '''# occure under the same condition as is_in_check but this time the kings evacuation
        # possibilities are illegal and there is no available piece to stand in the "way" of the attacking piece.'''
        # returns boolean
        pass

    def el_passant(self):
        '''# occur only when W pawn in the 5th line(4) and the B pawn in the 4th line(3),
        # and if neighbor of opposite color jumps 2 steps forward - a specific step takes place from pawn moves.'''
        # returns additional movement option for specific pawn
        pass

    def eat_piece(self):  # the piece which was in the cube to which the current piece stepped into disappear.
        pass

    def castling(self):  # can happen as long as there isn't current check/the king pass underneath check,
        # and as long as the king or rook hasn't moved yet.
        # return additional movement option for king+rook combined.
        pass

    def promotion(self):  # occur when a W/B pawn reach the top/bottom border accordingly.
        # deletes pawn instance and create new piece instance at the same location.
        pass

    def turn(self):
        GAMEON = True
        while GAMEON:
            color = self.color_turn
            move = self.enter_move(color)
            self.move_is_in_board(color, move)  # should i call enter move from inside move is in board?


if __name__ == "__main__":
    game = Game()
    game.play()
