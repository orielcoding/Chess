import numpy as np
import re
import chess_definitions


class Game:
    def __init__(self, color=0):
        self.gameBoard = chess_definitions.Board(8, 8)
        self.curr_color = color  # color updates every turn

        for pawn_location in range(8):
            self.gameBoard.set_initial_squares((6, pawn_location), chess_definitions.Pawn(0))
            self.gameBoard.set_initial_squares((1, pawn_location), chess_definitions.Pawn(1))
        for bishop_location in [2, 5]:
            self.gameBoard.set_initial_squares((7, bishop_location), chess_definitions.Bishop(0))
            self.gameBoard.set_initial_squares((0, bishop_location), chess_definitions.Bishop(1))
        for rook_location in [0, 7]:
            self.gameBoard.set_initial_squares((7, rook_location), chess_definitions.Rook(0))
            self.gameBoard.set_initial_squares((0, rook_location), chess_definitions.Rook(1))
        for knight_location in [1, 6]:
            self.gameBoard.set_initial_squares((7, knight_location), chess_definitions.Knight(0))
            self.gameBoard.set_initial_squares((0, knight_location), chess_definitions.Knight(1))
        self.gameBoard.set_initial_squares((7, 3), chess_definitions.Queen(0))
        self.gameBoard.set_initial_squares((0, 3), chess_definitions.Queen(1))
        self.gameBoard.set_initial_squares((7, 4), chess_definitions.King(0))
        self.gameBoard.set_initial_squares((0, 4), chess_definitions.King(1))

    color_dict = {0: "white" , 1: "black"}
    kings_location = {0: (7, 4), 1: (0, 4)}  # needs to be updated every time king is moving
    has_moved_castling = {"white_king": False, "black_king": False,
                          "left_white_rook": False, "right_white_rook": False,
                          "left_black_rook": False, "right_black_rook": False}
    white_castled = False
    black_castled = False

    def enter_move(self):
        color_dictionary = {0: "White's turn", 1: "Black's turn"}
        move = input(f"{color_dictionary[self.curr_color]}, enter move: ")
        return move

    def move_is_in_board(self, move: str):  # if an input is an existing square, returns the square as int list
        a = re.match('([a-hA-H][1-8])[,: \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move)
        if a:  # for programmer, not user
            location_func = lambda loc_str: ((8-int(a.group(1)[1]), (ord(a.group(1).lower()[0]) - ord("a"))),
                                             (8-int(a.group(2)[1]), (ord(a.group(2).lower()[0]) - ord("a"))))
            return location_func(move)
        raise ValueError('illegal square was entered, please enter existing square')

    def color_move_validation(self, move: tuple):  # move is both the current and target squares
        # todo fix pawn- it cant go forward to piece of any color (not even enemy piece)
        if self.gameBoard.get_square_state(move[0]) is not None and \
                self.gameBoard.get_square_state(move[0]).color != self.curr_color:
            raise chess_definitions.WrongColorError(f'only {Game.color_dict[self.curr_color]} can move, please move a piece of that color')

        if self.gameBoard.get_square_state(move[1]) is not None and \
                self.gameBoard.get_square_state(move[1]).color == self.curr_color:
            raise chess_definitions.WrongColorError("piece can't land on square populated by piece of the same color")

    def movement_type_validation(self, move: tuple, piece: chess_definitions.Piece):
        if type(piece) != chess_definitions.Knight:
            direction = chess_definitions.Coordinates(move).sign_vector
        else:
            direction = chess_definitions.Coordinates(move).vector
        if not np.any([np.array_equal(direction, element) for element in list(piece.sign_vector())]):
            # todo check alternative
            raise ValueError(f"{piece} can't move to the requested square")

    def path_interruptions_validation(self, move: tuple, piece: chess_definitions.Piece):
        if type(piece) != chess_definitions.Knight:
            squares_to_check: np.ndarray = chess_definitions.Coordinates(move).squares_path()
            for idx, square in enumerate(squares_to_check):
                if self.gameBoard.get_square_state(tuple(square)) is not None and idx != len(squares_to_check)-1:
                    raise chess_definitions.PathError("move is not possible")

    def is_revealing_king(self, move: tuple):  # todo add case prevents king steps into check
        '''this method assures that the move chosen doesn't expose the king to a threatening piece.
            it is done by checking the direction of the board which connects the king and the moving piece.'''
        locations_king_moving_piece: tuple = (Game.kings_location[self.curr_color], move[0])
        direction_from_king: np.ndarray = chess_definitions.Coordinates(locations_king_moving_piece).sign_vector
        farthest_possible_threatening_piece = chess_definitions.Coordinates(locations_king_moving_piece).farthest_distance()
        locations_king_farthest_piece = (move[0],tuple(farthest_possible_threatening_piece))
        squares_to_check: np.ndarray = chess_definitions.Coordinates(locations_king_farthest_piece).squares_path()
        future_board = self.gameBoard
        future_board.set_square_state(move,future_board.get_square_state(move[0]))
        # used to stimulate new piece location which might still block enemy path to the king
        for square in squares_to_check:
            piece = future_board.get_square_state(tuple(square))
            if piece is not None and piece.color != self.curr_color:
                if np.any([np.array_equal(direction_from_king, element) for element in list(piece.sign_vector())])\
                        and piece != chess_definitions.Pawn and piece != chess_definitions.King:
                    # checks that enemy piece can't reach the exposed king
                    raise chess_definitions.ExposeKingError("move is illegal, it exposes the king")
            elif piece is not None and piece.color == self.curr_color:
                break

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

    def el_passant(self):  # need to be called from movement_type_validation
        '''# occur only when W pawn in the 5th line(4) and the B pawn in the 4th line(3),
        # and if neighbor of opposite color jumps 2 steps forward - a specific step takes place from pawn moves.'''
        # returns additional movement option for specific pawn
        pass

    def __castling(self,move: tuple, rook_side: str):  # called from inside the class for relevant user input
        condition_a = f"{Game.color_dict[self.curr_color]}_castled"
        condition_b = Game.has_moved_castling[f"{Game.color_dict[self.curr_color]}_king"]
        condition_c = Game.has_moved_castling[f"{rook_side}_{Game.color_dict[self.curr_color]}_rook"]
        if condition_a or condition_b or condition_c:
            raise ValueError("illegal move")
        # todo check if square is threatened
        self.gameBoard.set_square_state(move, chess_definitions.Rook(self.curr_color))

    def promotion(self, move: tuple):
        new_piece = None
        piece = self.gameBoard.get_square_state(move[0])
        if move[1][0] == 0 and self.curr_color == 0 and piece == chess_definitions.Pawn:  # asume no piece on first rank
            new_piece = input("choose promoted piece: (Q / R / K / B) ")
        elif move[1][0] == 7 and self.curr_color == 1 and piece == chess_definitions.Pawn:
            new_piece = input("choose promoted piece: (Q / R / K / B) ")
        if new_piece:
            a = re.match('^[ ]{0,3}(Q|q|R|r|K|k|B|b)[ ]{0,3}$', new_piece)
            if not a:
                raise TypeError("please choose one of the following characters: Q / R / K / B ")
            if new_piece == ("Q" or "q"):
                self.gameBoard.set_square_state(move[1], chess_definitions.Queen(self.curr_color))
            elif new_piece == ("R" or "r"):
                self.gameBoard.set_square_state(move[1], chess_definitions.Rook(self.curr_color))
            elif new_piece == ("K" or "k"):
                self.gameBoard.set_square_state(move[1], chess_definitions.Knight(self.curr_color))
            elif new_piece == ("B" or "b"):
                self.gameBoard.set_square_state(move[1], chess_definitions.Bishop(self.curr_color))

    def is_valid_move(self, move: str):
        try:
            locations = self.move_is_in_board(move)
            piece = self.gameBoard.get_square_state(locations[0])
            # self.color_move_validation(locations)
            if piece == chess_definitions.King and chess_definitions.Coordinates(locations).vector == np.array([0,2]):
                self.__castling(locations, "right")
            elif piece == chess_definitions.King and chess_definitions.Coordinates(locations).vector == np.array([0,-3]):
                self.__castling(locations, "left")
        except chess_definitions.PathError as e:
            print(e)
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)

    def turn(self):
        print(self.gameBoard)
        move = self.enter_move() # might need to add an exception?
        self.is_valid_move(move)
        locations = self.move_is_in_board(move)
        self.gameBoard.set_square_state(locations,self.gameBoard.get_square_state(locations[0]))
        # turn updates
        if self.gameBoard.get_square_state(locations[0]) == chess_definitions.King:
            Game.kings_location[self.curr_color] = tuple(locations[0])
            Game.has_moved_castling[f"{Game.color_dict[self.curr_color]}_king"] = True
        if self.gameBoard.get_square_state(locations[0]) == chess_definitions.Rook:
            Game.has_moved_castling[f"{rook_side}_{Game.color_dict[self.curr_color]}_rook"] = True

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


