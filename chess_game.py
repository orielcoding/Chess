import numpy as np
import re
import chess_definitions


class Game:
    def __init__(self, color=0):
        self.gameBoard = chess_definitions.Board()
        self.color = color  # color updates every turn
        self.pieces = {
            "WB1": chess_definitions.Piece(0, 'bishop_moves'),
            "BB1": chess_definitions.Piece( 1, 'bishop_moves'),
            "WB2": chess_definitions.Piece( 0, 'bishop_moves'),
            "BB2": chess_definitions.Piece( 1, 'bishop_moves'),
            "WR1": chess_definitions.Piece( 0, 'rook_moves'),
            "BR1": chess_definitions.Piece( 1, 'rook_moves'),
            "WR2": chess_definitions.Piece( 0, 'rook_moves'),
            "BR2": chess_definitions.Piece( 1, 'rook_moves'),
            "WK1": chess_definitions.Piece( 0, 'knight_jumps'),
            "BK1": chess_definitions.Piece( 1, 'knight_jumps'),
            "WK2": chess_definitions.Piece( 0, 'knight_jumps'),
            "BK2": chess_definitions.Piece( 1, 'knight_jumps'),
            "WQ": chess_definitions.Piece( 0, 'queen_moves'),
            "BQ": chess_definitions.Piece( 1, 'queen_moves'),
            "WKING": chess_definitions.Piece( 0, 'king_moves'),
            "BKING": chess_definitions.Piece( 1, 'king_moves'),
            "WP1": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP2": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP3": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP4": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP5": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP6": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP7": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "WP8": chess_definitions.Piece( 0, 'white_pawn_moves'),
            "BP1": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP2": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP3": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP4": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP5": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP6": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP7": chess_definitions.Piece( 1, 'black_pawn_moves'),
            "BP8": chess_definitions.Piece( 1, 'black_pawn_moves')
        }
        for pawn in range(8):
            self.gameBoard.set_initial_squares([6, pawn], self.pieces["WP" + str(pawn + 1)])
            self.gameBoard.set_initial_squares([1, pawn], self.pieces["BP" + str(pawn + 1)])
        for bishop in (2, 5):
            self.gameBoard.set_initial_squares([7, bishop], self.pieces["WB" + str(bishop + 1)])
            self.gameBoard.set_initial_squares([0, bishop], self.pieces["BB" + str(bishop + 1)])
        for rook in (0, 7):
            self.gameBoard.set_initial_squares([7, rook], self.pieces["WR" + str(rook + 1)])
            self.gameBoard.set_initial_squares([0, rook], self.pieces["BR" + str(rook + 1)])
        for knight in (1, 6):
            self.gameBoard.set_initial_squares([7, knight], self.pieces["WK" + str(knight + 1)])
            self.gameBoard.set_initial_squares([0, knight], self.pieces["BK" + str(knight + 1)])
        self.gameBoard.set_initial_squares([7, 4], self.pieces["WQ"])
        self.gameBoard.set_initial_squares([0, 4], self.pieces["BQ"])
        self.gameBoard.set_initial_squares([7, 5], self.pieces["WKING"])
        self.gameBoard.set_initial_squares([0, 5], self.pieces["BKING"])

    def enter_move(self, color: int):
        color_dictionary = {0: "White's turn: ", 1: "Black's turn: "}
        move = input(f"{color_dictionary[self.color]} enter move. format example: A2->A3")
        return move

    def move_is_in_board(self, color, move):  # if an input is an existing square, returns the square as int list
        a = re.match('([a-hA-H][1-8])[, \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move)
        if a:
            location = lambda locStr: ([ord(locStr[0, 0].lower()) - ord("a"), int(locStr[0, 1]) - 1],
                                       [ord(locStr[1, 0].lower()) - ord("a"), int(locStr[1, 1]) - 1])
            return location(a)
        raise ValueError('ileggal square was entered, please enter existing square')

    def color_move_validation(self, location: list):  # location is both the current and target squares
        if self.gameBoard.get_square_state(location[0]).color == self.color:
            pass
        else:
            raise TypeError('only ', self.color, ' can move, please move a piece of that color')
        if self.gameBoard.get_square_state(location[1]).color != self.color:
            pass
        else:
            raise TypeError("piece can't land on square populated by piece of the same color" ) # do i want type error?

    def movement_type_validation(self, location: list):
        piece=self.gameBoard.get_square_state(location[0]) # returns the object in specific square
        target_square=location[1]
        if target_square not in piece.available_squares():
            raise TypeError(piece, " can't move to the requested square" )

    def path_interruptions_validation(self, location: list):
        piece = self.gameBoard.get_square_state(location[0])  # returns the object in specific square
        target_square = location[1]
        if piece != "WK1" and piece != "WK2" and piece != "BK1" and piece != "BK2": # if piece is knight then path doesn't matter
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

    def turn(self, color, board):
        color = self.color
        move = self.enter_move(color)
        location = self.move_is_in_board(color, move)
        self.color_move_validation(color, location)

    def play(self):
        game_on = True
        while game_on:
            self.turn()
            if self.is_in_checkmate():
                game_on = False
            return self.color  # need to switch the integer back to str by dictionary created at enter_move


if __name__ == "__main__":
    game = Game()
    winning_color = game.play()
    print(winning_color, " WON!")
