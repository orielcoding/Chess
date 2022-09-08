import numpy as np
import re
import chess_definitions


class Game:
    def __init__(self, color=0):
        self.gameBoard = chess_definitions.Board(8,8)
        self.curr_color = color  # color updates every turn

        for pawn_location in range(8):
            self.gameBoard.set_initial_squares((6, pawn_location), chess_definitions.Piece(0,"white_pawn"))
            self.gameBoard.set_initial_squares((1, pawn_location), chess_definitions.Piece(1,"black_pawn"))
        for bishop_location in [2, 5]:
            self.gameBoard.set_initial_squares((7, bishop_location), chess_definitions.Piece(0,"bishop"))
            self.gameBoard.set_initial_squares((0, bishop_location), chess_definitions.Piece(1,"bishop"))
        for rook_location in [0, 7]:
            self.gameBoard.set_initial_squares((7, rook_location), chess_definitions.Piece(0,"rook"))
            self.gameBoard.set_initial_squares((0, rook_location), chess_definitions.Piece(1,"rook"))
        for knight_location in [1, 6]:
            self.gameBoard.set_initial_squares((7, knight_location), chess_definitions.Piece(0,"knight"))
            self.gameBoard.set_initial_squares((0, knight_location), chess_definitions.Piece(1,"knight"))
        self.gameBoard.set_initial_squares((7, 3), chess_definitions.Piece(0,"queen"))
        self.gameBoard.set_initial_squares((0, 3), chess_definitions.Piece(1,"queen"))
        self.gameBoard.set_initial_squares((7, 4), chess_definitions.Piece(0,"king"))
        self.gameBoard.set_initial_squares((0, 4), chess_definitions.Piece(1,"king"))

    def enter_move(self, color: int):
        color_dictionary = {0: "White's turn", 1: "Black's turn"}
        move = input(f"{color_dictionary[self.curr_color]}, enter move: ")
        return move

    def move_is_in_board(self, move):  # if an input is an existing square, returns the square as int list
        a = re.match('([a-hA-H][1-8])[, \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move)
        if a: # for programmer, not user
            location_func= lambda loc_str: ((7-(int(a.group(1)[1]) - 1), (ord(a.group(1).lower()[0]) - ord("a"))),
                                            (7-(int(a.group(2)[1]) - 1), (ord(a.group(2).lower()[0]) - ord("a"))))
            print(location_func(move))
            return location_func(move)
        raise ValueError('illegal square was entered, please enter existing square')

    def color_move_validation(self, location: tuple):  # location is both the current and target squares
        color_dict={0: "white", 1:"black"}
        if self.gameBoard.get_square_state(location[0]).color != self.curr_color:
            raise TypeError(f'only {color_dict[self.curr_color]} can move, please move a piece of that color')

        if self.gameBoard.get_square_state(location[1]) is not None and self.gameBoard.get_square_state(location[1]).color == self.curr_color:
            raise TypeError("piece can't land on square populated by piece of the same color" ) # do i want type error?

    def movement_type_validation(self, location: list):
        piece=self.gameBoard.get_square_state(location[0]) # returns the object in specific square
        target_square=location[1]
        if target_square not in piece.available_squares():
            raise TypeError(f"{piece} can't move to the requested square" )

    def path_interruptions_validation(self, location: list):
        piece = self.gameBoard.get_square_state(location[0])  # returns the object in specific square
        target_square = location[1]
        if piece != "WK1" and piece != "WK2" and piece != "BK1" and piece != "BK2":  # if knight path doesn't matter
            squares_to_check = piece.available_squares()  # returns list of squares in the way

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

    def is_valid_move(self):
        location = self.move_is_in_board(move)
        try:
            self.color_move_validation(location)
        except TypeError as e:
            print(e)

    def turn(self):
        print(self.gameBoard)
        color = self.curr_color
        while True:
            try:
                move = self.enter_move(color)
                location = self.move_is_in_board( move)
                self.color_move_validation(location)
                break
            except ValueError as e:
                print(e)
            except TypeError as e:
                print(e)



    def play(self):
        game_on = True
        while game_on:
            self.turn()
            if self.is_in_checkmate():
                game_on = False
        return self.curr_color  # need to switch the integer back to str by dictionary created at enter_move


if __name__ == "__main__":
    game = Game()
    winning_color = game.play()
    print(winning_color, " WON!")
