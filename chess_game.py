import numpy as np
import re
import chess_definitions
from chess_definitions import Location, Locations_List

color_dict = {0: "white", 1: "black"}


def move_is_in_board(move_str: str) -> Locations_List:
    match_object = re.match('([a-hA-H][1-8])[,: \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move_str)
    if match_object:
        return Locations_List([(8 - int(match_object.group(1)[1]), ord(match_object.group(1).lower()[0]) - ord("a")),
                               (8 - int(match_object.group(2)[1]), ord(match_object.group(2).lower()[0]) - ord("a"))])
    raise ValueError('illegal square was entered, please enter existing square')


class Game:
    def __init__(self, color=0):
        self.gameBoard = chess_definitions.Board(8, 8)
        self.curr_color = color  # color updates every turn
        self.kings_location = {0: Location((7, 4)), 1: Location((0, 4))}
        self.has_moved_castling = {"left_white_rook": False, "right_white_rook": False,
                                   "left_black_rook": False, "right_black_rook": False}
        self.white_cant_castle = False
        self.black_cant_castle = False
        self.last_move: Locations_List = None  # hold history one move backwards, checking possibility for an En-Passant
        self.last_move_type: chess_definitions.Piece = None
        self.check = False
        self.checkmate = False

        for pawn_location in range(8):
            self.gameBoard.set_initial_squares(Location((6, pawn_location)), chess_definitions.Pawn(0))
            self.gameBoard.set_initial_squares(Location((1, pawn_location)), chess_definitions.Pawn(1))
        for bishop_location in [2, 5]:
            self.gameBoard.set_initial_squares(Location((7, bishop_location)), chess_definitions.Bishop(0))
            self.gameBoard.set_initial_squares(Location((0, bishop_location)), chess_definitions.Bishop(1))
        for rook_location in [0, 7]:
            self.gameBoard.set_initial_squares(Location((7, rook_location)), chess_definitions.Rook(0))
            self.gameBoard.set_initial_squares(Location((0, rook_location)), chess_definitions.Rook(1))
        for knight_location in [1, 6]:
            self.gameBoard.set_initial_squares(Location((7, knight_location)), chess_definitions.Knight(0))
            self.gameBoard.set_initial_squares(Location((0, knight_location)), chess_definitions.Knight(1))
        self.gameBoard.set_initial_squares(Location((7, 3)), chess_definitions.Queen(0))
        self.gameBoard.set_initial_squares(Location((0, 3)), chess_definitions.Queen(1))
        self.gameBoard.set_initial_squares(Location((7, 4)), chess_definitions.King(0))
        self.gameBoard.set_initial_squares(Location((0, 4)), chess_definitions.King(1))

    def enter_move(self) -> str:
        color_turn_dictionary = {0: "White's turn", 1: "Black's turn"}
        move = input(f"{color_turn_dictionary[self.curr_color]}, enter move: ")
        return move

    def color_move_validation(self, move: Locations_List, piece: chess_definitions.Piece):  # move=current+target square
        if self.gameBoard.get_square_state(move[0]) is not None and \
                self.gameBoard.get_square_state(move[0]).color != self.curr_color:
            raise chess_definitions.WrongColorError(
                f'only {color_dict[self.curr_color]} can move, please move a piece of that color')

        if self.gameBoard.get_square_state(move[1]) is not None and \
                self.gameBoard.get_square_state(move[1]).color == self.curr_color:
            raise chess_definitions.WrongColorError("piece can't land on square populated by piece of the same color")
        # handle private case - pawn can't step forward to enemy's piece
        elif self.gameBoard.get_square_state(move[1]) is not None and \
                self.gameBoard.get_square_state(move[1]).color != self.curr_color:
            if type(piece) == chess_definitions.Pawn:
                raise TypeError("pawn cant step forward into enemy's piece")

    def movement_type_validation(self, move: Locations_List, piece: chess_definitions.Piece):
        if type(piece) != chess_definitions.Knight:
            direction = chess_definitions.Coordinates(move).sign_vector
        else:
            direction = chess_definitions.Coordinates(move).vector
        if not np.any([np.array_equal(direction, element) for element in list(piece.sign_vector())]):
            if type(piece) == chess_definitions.Pawn:
                self.pawn_eating(move)
            else:
                raise ValueError(f"{piece} can't reach to target square")

    def legal_distance(self, move: Locations_List, piece: chess_definitions.Piece):
        """ This function is relevant only if the selected piece is pawn / king / knight,
            whose limited with the size of their steps"""
        vector = chess_definitions.Coordinates(move).vector
        sign_vector = chess_definitions.Coordinates(move).sign_vector
        if type(piece) == chess_definitions.Pawn:
            if move[0][0] != 6 - self.curr_color * 5 or vector != np.multiply(sign_vector, np.array((2, 0))):
                # case: jump 2 steps forward from initial rank
                raise ValueError(f"{piece} can't reach to target square")
        elif type(piece) == chess_definitions.King:
            if chess_definitions.Coordinates(move).vector == np.array([0, 2]):
                self.castling(move, "right")
            elif chess_definitions.Coordinates(move).vector == np.array([0, -3]):
                self.castling(move, "left")
            else:
                raise ValueError(f"{piece} can't reach to target square")
        elif type(piece) == chess_definitions.Knight:
            if vector != sign_vector:
                raise ValueError(f"{piece} can't reach to target square")

    def pawn_eating(self, move: Locations_List):
        """ This method is called only if moving piece of type pawn, and the move was illegal because of
            sign vector validation"""
        rank_movement = {0: -1 , 1: 1}  # the rank vector for an eating pawn by color
        target_square: chess_definitions.Piece = self.gameBoard.get_square_state(Location(move[1]))
        vector: np.array = chess_definitions.Coordinates(move).vector
        if not np.any([np.array_equal(vector, element) for element in [np.array([rank_movement[self.curr_color],1]),np.array([rank_movement[self.curr_color],-1])]]):
            raise ValueError(f"{self.curr_color}_pawn can't reach to target square")
        elif target_square is None:  # assuming here by color validation if square isn't None- its of opposite color.
            if not self.en_passant(move):
                raise chess_definitions.EnPassantError("Selected pawn can't eat with en-passant at the selected square")
            self.gameBoard.set_square_state(self.last_move) # todo make sure its checked last. should i create member whose set up boolianly each turn?

    def path_interruptions_validation(self, move: Locations_List, piece: chess_definitions.Piece):
        if type(piece) != chess_definitions.Knight:
            squares_to_check: np.ndarray = chess_definitions.Coordinates(move).squares_path()
            for idx, square in enumerate(squares_to_check):
                if self.gameBoard.get_square_state(Location(tuple(square))) is not None and idx != len(
                        squares_to_check) - 1:
                    raise chess_definitions.PathError("move is not possible")

    def is_revealing_king(self, move: Locations_List):  # todo add case prevents king steps into check
        """This method assures that the move chosen doesn't expose the king to a threatening piece.
            It is done by checking whether enemy's piece located on the direction of the board which
             connects the king and the moving piece, under several limitations."""
        king_moving_piece_locations = Locations_List([self.kings_location[self.curr_color], move[0]])
        king_piece_sign_vector: np.ndarray = chess_definitions.Coordinates(king_moving_piece_locations).sign_vector
        farthest_possible_threatening_piece: np.array = chess_definitions.Coordinates(
            king_moving_piece_locations).farthest_distance()
        king_farthest_piece_locations = Locations_List([move[0], tuple(farthest_possible_threatening_piece)])
        squares_to_check: np.ndarray = chess_definitions.Coordinates(king_farthest_piece_locations).squares_path()
        future_board = self.gameBoard
        future_board.set_square_state(move, future_board.get_square_state(move[0]))
        # used to stimulate new piece location which might still block enemy's path to the king
        for square in squares_to_check:
            piece = future_board.get_square_state(Location(tuple(square)))
            if piece is not None and piece.color != self.curr_color:  # enemy's piece
                if np.any([np.array_equal(king_piece_sign_vector, element) for element in list(piece.sign_vector())]) \
                        and piece != chess_definitions.Pawn and piece != chess_definitions.King:
                    # check if piece aiming towards the king
                    raise chess_definitions.ExposeKingError("move is illegal, it exposes the king")
            elif piece is not None and piece.color == self.curr_color:
                break

    def is_in_check(self):
        """if the king occupies the way of one of piece possible movement steps from opposite color,
        and none of the pieces of the kings color doesn't stand in the "way"- (way isn't defined currently).
        this method defines new definition for legal move for the next "turn":
        either the king must evacuate to one of his possible squares, or one of the pieces must stand in the "way"
        of the attacking piece"""
        # calls to the function is_in_checkmate.
        return self.check

    def is_in_checkmate(self):
        """
        occur under the same condition as is_in_check but this time the kings evacuation
        possibilities are illegal and there is no available piece to stand in the "way" of the attacking piece.
        here i need to use recursive function - operate a future board and create fake turn which examine possibilities
        until certain possibility works.
        """
        return self.checkmate

    def en_passant(self, move: Locations_List) -> bool:
        """This method is called only from eating pawn method, and it handles the case in which enemy's pawn stepped
            2 squares to the same rank as the current moving pawn (opposite colors). In that case, the pawn allowed
            to eat even thought the relevant square is empty (and the previous pawn will disappear)."""
        if self.last_move_type != chess_definitions.Pawn or \
                list(abs(chess_definitions.Coordinates(self.last_move).vector)) != list(np.array((2, 0))) or \
                self.last_move[1][0] != move[0][0] or abs(int(self.last_move[1][1] - move[0][1])) != 1:
            return False
        else:
            return True

    def castling(self, move: Locations_List, rook_side: str):
        condition_a = f"{color_dict[self.curr_color]}_cant_castle"
        condition_b = self.has_moved_castling[f"{rook_side}_{color_dict[self.curr_color]}_rook"]
        if condition_a or condition_b:
            raise ValueError("illegal move")
        # todo check if squares are threatened
        self.gameBoard.set_square_state(move, chess_definitions.Rook(self.curr_color))

    def promotion(self, move: Locations_List):
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

    def is_valid_move(self, string_move: str) -> Locations_List:
        try:
            move = move_is_in_board(string_move)
            piece = self.gameBoard.get_square_state(move[0])
            self.color_move_validation(move, piece)
            self.movement_type_validation(move, piece)
            if type(piece) is chess_definitions.Pawn or type(piece) is chess_definitions.King or type(
                    piece) is chess_definitions.Knight:
                self.legal_distance(move, piece)
            self.path_interruptions_validation(move,piece)
            self.is_revealing_king(move)

            return move
        except chess_definitions.PathError as e:
            print(e)
        except ValueError as e:
            print(e)
        except TypeError as e:
            print(e)


    def turn(self):
        print(self.gameBoard)
        string_move = self.enter_move()  # might need to add an exception?
        locations: Locations_List = self.is_valid_move(string_move)
        piece: chess_definitions.Piece = self.gameBoard.get_square_state(locations[0])

        # turn updates

        self.gameBoard.set_square_state(locations, self.gameBoard.get_square_state(locations[0]))
        if self.gameBoard.get_square_state(locations[0]) == chess_definitions.King:
            self.kings_location[self.curr_color] = locations[0]
            self.has_moved_castling[f"{color_dict[self.curr_color]}_king"] = True
        if self.gameBoard.get_square_state(locations[0]) == chess_definitions.Rook:
            self.has_moved_castling[f"{rook_side}_{color_dict[self.curr_color]}_rook"] = True

        game.last_move = locations
        game.last_move_type = piece

    def play(self):
        game_on = True
        while game_on:
            self.turn()
            if self.checkmate:
                game_on = False
        return self.curr_color  # need to switch the integer back to str by dictionary created at enter_move


if __name__ == "__main__":
    game = Game()
    winning_color = game.play()
    print(f"{winning_color} WON!")
