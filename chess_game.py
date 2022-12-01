import numpy as np
import re
import chess_definitions
from chess_definitions import Location, Locations_List
import copy

color_dict = {0: "white", 1: "black"}


def move_is_in_board(move_str: str) -> Locations_List:
    match_object = re.match('([a-hA-H][1-8])[,: \->]{0,4}([a-hA-H][1-8])[,. ]{0,2}$', move_str)
    if match_object:
        return Locations_List([(8 - int(match_object.group(1)[1]), ord(match_object.group(1).lower()[0]) - ord("a")),
                               (8 - int(match_object.group(2)[1]), ord(match_object.group(2).lower()[0]) - ord("a"))])
    raise chess_definitions.NotInBoardError('illegal square was entered, please enter existing square')


class Game:
    def __init__(self, color=0):
        self.gameBoard = chess_definitions.Board(8, 8)
        self.curr_color: int = color  # color updates every turn
        self.kings_location = {0: Location((7, 4)), 1: Location((0, 4))}
        self.castling_possibilities_info = {"left_white_rook": False, "right_white_rook": False,
                                            "left_black_rook": False, "right_black_rook": False}
        self.white_cant_castle = False
        self.black_cant_castle = False
        self.last_move: Locations_List = None  # hold history one move backwards, checking possibility for an En-Passant
        self.last_move_type: chess_definitions.Piece = None
        self.en_passant_ = False
        self.pawn_eating = False
        self.check_testing: bool = False
        self.check = False
        self.checkmate = False
        self.black_pieces_loc = set()
        self.white_pieces_loc = set()

        for pawn_location in range(8):
            self.gameBoard.set_initial_squares(Location((6, pawn_location)), chess_definitions.Pawn(0))
            self.white_pieces_loc.add(Location((6, pawn_location)))
            self.gameBoard.set_initial_squares(Location((1, pawn_location)), chess_definitions.Pawn(1))
            self.black_pieces_loc.add(Location((1, pawn_location)))
        for bishop_location in [2, 5]:
            self.gameBoard.set_initial_squares(Location((7, bishop_location)), chess_definitions.Bishop(0))
            self.white_pieces_loc.add(Location((7, bishop_location)))
            self.gameBoard.set_initial_squares(Location((0, bishop_location)), chess_definitions.Bishop(1))
            self.black_pieces_loc.add(Location((0, bishop_location)))
        for rook_location in [0, 7]:
            self.gameBoard.set_initial_squares(Location((7, rook_location)), chess_definitions.Rook(0))
            self.white_pieces_loc.add(Location((7, rook_location)))
            self.gameBoard.set_initial_squares(Location((0, rook_location)), chess_definitions.Rook(1))
            self.black_pieces_loc.add(Location((0, rook_location)))
        for knight_location in [1, 6]:
            self.gameBoard.set_initial_squares(Location((7, knight_location)), chess_definitions.Knight(0))
            self.white_pieces_loc.add(Location((7, knight_location)))
            self.gameBoard.set_initial_squares(Location((0, knight_location)), chess_definitions.Knight(1))
            self.black_pieces_loc.add(Location((0, knight_location)))
        self.gameBoard.set_initial_squares(Location((7, 3)), chess_definitions.Queen(0))
        self.white_pieces_loc.add(Location((7, 3)))
        self.gameBoard.set_initial_squares(Location((0, 3)), chess_definitions.Queen(1))
        self.black_pieces_loc.add(Location((0, 3)))
        self.gameBoard.set_initial_squares(Location((7, 4)), chess_definitions.King(0))
        self.white_pieces_loc.add(Location((7, 4)))
        self.gameBoard.set_initial_squares(Location((0, 4)), chess_definitions.King(1))
        self.black_pieces_loc.add(Location((0, 4)))

    def enter_move(self) -> str:
        color_turn_dictionary = {0: "White's turn", 1: "Black's turn"}
        move = input(f"{color_turn_dictionary[self.curr_color]}, enter move: ")
        return move

    def color_move_validation(self, move: Locations_List,
                              piece: chess_definitions.Piece) -> bool:  # move=current+target square
        color_sign = {0: -1, 1: 1}
        curr_loc_piece = self.gameBoard.get_square_state(move[0])
        target_loc_piece = self.gameBoard.get_square_state(move[1])
        if curr_loc_piece is not None:
            if curr_loc_piece.color != self.curr_color:
                if self.check_testing:
                    return False
                else:
                    print(f'only {color_dict[self.curr_color]} can move, please move a piece of that color')
                    return False
            if target_loc_piece is not None and target_loc_piece.color == self.curr_color:
                if self.check_testing:
                    return False
                else:
                    print("piece can't land on square populated by piece of the same color")
                    return False
            # handle private case - pawn can't step forward to enemy's piece
            elif target_loc_piece is not None and target_loc_piece.color != self.curr_color:
                if type(piece) == chess_definitions.Pawn:
                    if np.array_equal(np.sign(np.array(move[1])-np.array(move[0])), np.array((color_sign[self.curr_color],0))):
                        # the second condition is because only stepping forward would raise the following print:
                        if self.check_testing:
                            return False
                        else:
                            print("pawn cant step forward into enemy's piece")
                            return False
            return True
        return False  # this case occur when player tries to make move from empty square.

    def movement_type_validation(self, move: Locations_List, piece: chess_definitions.Piece) -> bool:
        if type(piece) != chess_definitions.Knight:
            vector: np.array = chess_definitions.Coordinates(move).vector
            direction: np.array = chess_definitions.Coordinates(move).sign_vector
            if not np.array_equal(abs(direction),np.array((1, 0))) and not np.array_equal(abs(direction),np.array((0, 1))):
                if abs(vector[0]) != abs(vector[1]):  # checks that move is in possible direction for any piece.
                    return False
        else:
            direction = chess_definitions.Coordinates(move).vector
        if piece.sign_vector().ndim == 1:  # pawn's sign vector is 1d array
            if not np.array_equal(direction, piece.sign_vector()):
                if not self.pawn_eating_validation(move):
                    return False
        else:  # all pieces but pawn has a 2d array sign vector
            if not np.any([np.array_equal(direction, element) for element in piece.sign_vector()]):
                if self.check_testing:
                    return False
                else:
                    print(f"{piece} can't reach to target square")
                    return False
        return True

    def distance_validation(self, move: Locations_List, piece: chess_definitions.Piece) -> bool:
        """ This function is relevant only if the selected piece is pawn / king,
            whose limited with the size of their steps.
            The private case for knight already treated at movement type validation"""
        color_sign = {0: -1, 1: 1}
        vector = chess_definitions.Coordinates(move).vector
        sign_vector = chess_definitions.Coordinates(move).sign_vector
        if type(piece) == chess_definitions.Pawn:
            if not np.array_equal(vector,np.array([color_sign[self.curr_color],0])):
                if move[0][0] != 6 - self.curr_color * 5 and not np.array_equal(vector, 2 * sign_vector):
                    # case: jump 2 steps forward from initial rank
                    if not self.pawn_eating:
                        if self.check_testing:
                            return False
                        else:
                            print(f"{piece} can't reach to target square")
                            return False
        elif type(piece) == chess_definitions.King:
            if np.array_equal(chess_definitions.Coordinates(move).vector, np.array([0, 2])):
                if not self.castling(move):
                    return False
            elif np.array_equal(chess_definitions.Coordinates(move).vector, np.array([0, -2])):
                if not self.castling(move):
                    return False
            else:
                if self.check_testing:
                    return False
                else:
                    print(f"{piece} can't reach to target square")
                    return False
        return True

    def pawn_eating_validation(self, move: Locations_List) -> bool:
        """ This method is called only if moving piece of type pawn, and the move was illegal because of
            sign vector validation"""
        rank_movement = {0: -1, 1: 1}  # the rank vector for an eating pawn by color
        target_square: chess_definitions.Piece = self.gameBoard.get_square_state(Location(move[1]))
        vector: np.array = chess_definitions.Coordinates(move).vector
        if not np.array_equal(vector, np.array((rank_movement[self.curr_color], 1))) and \
                not np.array_equal(vector, np.array((rank_movement[self.curr_color], -1))):
            if self.check_testing:
                self.pawn_eating = False
                return False
            else:
                print("pawn can't reach to target square")
                self.pawn_eating = False
                return False
        elif target_square is None:  # assuming here by color validation if square isn't None- its of opposite color.
            if not self.en_passant(move):
                self.pawn_eating = False
                return False
        self.pawn_eating = True
        return True

    def path_interruptions_validation(self, move: Locations_List, piece: chess_definitions.Piece) -> bool:
        squares_to_check: np.ndarray = chess_definitions.Coordinates(move).squares_path_for_validation()
        for idx, square in enumerate(squares_to_check):
            if self.gameBoard.get_square_state(Location(tuple(square))) is not None and idx != len(
                    squares_to_check) - 1:
                if self.check_testing:
                    return False
                else:
                    print("move is not possible because it's way blocked by some piece/s")
                    return False
        return True

    def is_not_revealing_king(self, move: Locations_List) -> bool:  # if return false: king is revealed.
        """
        This method assures that the move chosen doesn't expose the king to a threatening piece.
        It is done by checking whether enemy's piece located on the direction of the board which
        connects the king and the moving piece, depending on the enemy's piece movement type.
        """
        current_board = copy.deepcopy(self.gameBoard)
        king_current_loc = copy.deepcopy(self.kings_location[self.curr_color])
        if type(self.gameBoard.get_square_state(move[0])) == chess_definitions.King:
            self.kings_location[self.curr_color] = move[1]
        self.gameBoard.set_square_state(move, self.gameBoard.get_square_state(move[0]))  # stimulate new piece location
        self.is_in_check()
        self.gameBoard = current_board
        self.kings_location[self.curr_color] = king_current_loc
        if self.check:
            if self.check_testing:
                return False
            else:
                print("move is not possible because revealing king to check/checkmate")
                return False
        else:
            return True

    def is_in_check(self) -> (chess_definitions.Piece, chess_definitions.Locations_List):
        """
        There are two check cases. first case is when method called from revealing king- in that case, the current color
        checks that it isn't stepping into check- therefore piece list will be of the opposite color.
        second case is after moving the piece- check if current color is threatening the enemy's king - piece list will
        be of the current color.
        in this method "piece list" relates to the pieces who might threaten the current color king
        """
        if self.curr_color == 0:  # white's turn, so need to check whether black threatens
            piece_list = self.black_pieces_loc
        else:
            piece_list = self.white_pieces_loc
        self.curr_color = 1 - self.curr_color  # changes for color validation later on
        for location in piece_list:
            if type(self.gameBoard.get_square_state(location)) == chess_definitions.King:
                continue
            move = Locations_List([location, self.kings_location[1-self.curr_color]])
            self.check_testing = True
            if self.is_valid_move(str(move), move):
                self.check = True
                self.curr_color = 1 - self.curr_color
                self.check_testing = False
                return self.gameBoard.get_square_state(location), move
        else:
            self.check = False
        self.curr_color = 1 - self.curr_color  # returning to the current playing color
        self.check_testing = False
        return None, None

    def is_in_checkmate(self, threatening_move: chess_definitions.Locations_List) -> bool:
        """
        Checkmate validation requires checking unintuitive possibility: if a move was found which protects the king from
        enemy's piece, there must be another check validation to make sure that the king is no longer threatened.
        in this method "piece list" relates to the pieces who might be able to protect the current color king
        """

        if self.curr_color == 0:
            piece_list = self.white_pieces_loc
        else:
            piece_list = self.black_pieces_loc
        squares_path: np.ndarray = chess_definitions.Coordinates(threatening_move).squares_path_for_protection()
        for location in piece_list:
            if type(self.gameBoard.get_square_state(location)) == chess_definitions.King:
                escaping_vectors = chess_definitions.King.sign_vector(1-self.curr_color)
                for vector in escaping_vectors:
                    target_loc = tuple(vector+self.kings_location[1-self.curr_color])
                    if target_loc[0] > 7 or target_loc[0] < 0 or target_loc[1] > 7 or target_loc[1] < 0:
                        continue
                    move: Locations_List = Locations_List([location, target_loc])
                    self.curr_color = 1 - self.curr_color  # changes for color validation, then returns to current color
                    self.check_testing = True
                    if not self.color_move_validation(move,self.gameBoard.get_square_state(location)):
                        self.curr_color = 1 - self.curr_color
                        continue
                    if self.is_not_revealing_king(move):  # check whether the king is still revealed after escaping
                        self.curr_color = 1 - self.curr_color
                        self.check_testing = False
                        return False  # not checkmate
                    self.curr_color = 1 - self.curr_color
            else:
                for square_blocks_check in squares_path:
                    move_to_block_check = Locations_List([location, tuple(square_blocks_check)])
                    self.curr_color = 1 - self.curr_color
                    self.check_testing = True
                    if self.is_valid_move(str(move_to_block_check), move_to_block_check):
                        self.curr_color = 1 - self.curr_color
                        # current_board = copy.deepcopy(self.gameBoard)
                        # self.gameBoard.set_square_state(move_to_block_check, self.gameBoard.get_square_state(move_to_block_check[0]))
                        # self.check_testing = True
                        # self.is_in_check()
                        # self.check_testing = False
                        # if self.check:
                        #     self.gameBoard = current_board
                        #     continue
                        self.check_testing = False
                        return False  # not checkmate
                    else:
                        self.curr_color = 1 - self.curr_color
                        continue  # the specific move isn't available to protect the king
        self.check_testing = False
        return True

    def en_passant(self, move: Locations_List) -> bool:
        """This method is called only from eating pawn method, and it handles the case in which enemy's pawn stepped
            2 squares to the same rank as the current moving pawn (opposite colors). In that case, the pawn allowed
            to eat even thought the relevant square is empty (and the previous pawn will disappear)."""
        if self.last_move_type != chess_definitions.Pawn or \
                self.last_move[1][0] != move[0][0] or self.last_move[1][1] != move[1][1] or \
                not np.array_equal(abs(chess_definitions.Coordinates(self.last_move).vector), np.array((2, 0))):
            if self.check_testing:
                return False
            else:
                print("Selected pawn can't eat with en-passant at the selected square")
                return False
        else:
            self.en_passant_ = True
            return True

    def castling(self, move: Locations_List) -> bool:  # todo add case of long side rook path error(kn)
        if self.curr_color == 0:
            condition_a = self.white_cant_castle
            if move[1][1] == 2:
                condition_b = self.castling_possibilities_info["left_white_rook"]
            else:
                condition_b = self.castling_possibilities_info["right_white_rook"]
        else:
            condition_a = self.black_cant_castle
            if move[1][1] == 2:
                condition_b = self.castling_possibilities_info["left_black_rook"]
            else:
                condition_b = self.castling_possibilities_info["right_black_rook"]
        if condition_a or condition_b:  # then can't castle.
            if self.check_testing:
                return False
            else:
                print("requested castling is impossible")
                return False
        current_board = copy.deepcopy(self.gameBoard)
        king_current_loc = copy.deepcopy(self.kings_location[self.curr_color])
        # check whether king pass under check.
        if move[1][1] == 2:
            if self.gameBoard.get_square_state(Location((7 - 7*self.curr_color, 1))) is not None:
                return False  # because a piece is blocking the rook from the king where only the rook passes.
            self.kings_location[self.curr_color] = Location((7 - 7 * self.curr_color, 2))
        else:
            self.kings_location[self.curr_color] = Location((7 - 7 * self.curr_color, 6))
        self.gameBoard.set_square_state(move, self.gameBoard.get_square_state(move[0]))
        self.is_in_check()
        self.gameBoard = current_board
        self.kings_location[self.curr_color] = king_current_loc
        if self.check:
            return False
        else:  # update member for future attempts to castle
            return True

    def promotion(self, move: Locations_List) -> None:
        piece = self.gameBoard.get_square_state(move[0])
        if move[1][0] == 0 and type(piece) == chess_definitions.Pawn:  # asume no piece on first rank
            new_piece = input("choose number of the desired piece type to promote to: 1.Queen 2.Rook 3.Knight 4.Bishop")
        elif move[1][0] == 7 and type(piece) == chess_definitions.Pawn:
            new_piece = input("choose number of the desired piece type to promote to: 1.Queen 2.Rook 3.Knight 4.Bishop")
            while new_piece != 1 or new_piece != 2 or new_piece != 3 or new_piece != 4:
                print("please choose a number between 1 and 4")
                new_piece = input(
                    "choose number of the desired piece type to promote to: 1.Queen 2.Rook 3.Knight 4.Bishop")
            if new_piece == 1:
                self.gameBoard.set_square_state(move[1], chess_definitions.Queen(self.curr_color))
            elif new_piece == 2:
                self.gameBoard.set_square_state(move[1], chess_definitions.Rook(self.curr_color))
            elif new_piece == 3:
                self.gameBoard.set_square_state(move[1], chess_definitions.Knight(self.curr_color))
            elif new_piece == 4:
                self.gameBoard.set_square_state(move[1], chess_definitions.Bishop(self.curr_color))

    def is_valid_move(self, string_move: str, move: Locations_List = None) -> bool:
        is_not_check_examination = move is None  # prevents undesired validations when checking check.
        try:
            if is_not_check_examination:
                move = move_is_in_board(string_move)
            piece = self.gameBoard.get_square_state(move[0])
            if not self.color_move_validation(move, piece):
                return False
            if not self.movement_type_validation(move, piece):
                return False
            if type(piece) is chess_definitions.Pawn or type(piece) is chess_definitions.King:
                if not self.distance_validation(move, piece):
                    return False
            if type(piece) is not chess_definitions.Knight:
                if not self.path_interruptions_validation(move, piece):
                    return False
            if is_not_check_examination:
                if not self.is_not_revealing_king(move):
                    return False
        except chess_definitions.NotInBoardError as e:
            return False
        return True

    def turn(self) -> None:
        print(self.gameBoard)
        string_move = self.enter_move()
        if self.is_valid_move(string_move):
            locations: Locations_List = move_is_in_board(string_move)
            piece: chess_definitions.Piece = self.gameBoard.get_square_state(locations[0])

            # turn updates
            # piece location update:
            self.gameBoard.set_square_state(locations, piece)
            # castling updates:
            if type(self.gameBoard.get_square_state(locations[0])) == chess_definitions.King:
                # self.kings_location[self.curr_color] = locations[1]  # todo supposed to be rook loc update
                self.gameBoard.set_square_state(locations, chess_definitions.Rook(self.curr_color))
                if self.curr_color:
                    self.white_cant_castle = True
                else:
                    self.black_cant_castle = True
            if locations[1][1] == 2 and self.curr_color == 0:
                self.castling_possibilities_info["left_white_rook"] = True
            elif locations[1][1] == 2 and self.curr_color == 1:
                self.castling_possibilities_info["left_black_rook"] = True
            elif locations[1][1] == 6 and self.curr_color == 0:
                self.castling_possibilities_info["right_white_rook"] = True
            else:
                self.castling_possibilities_info["right_black_rook"] = True


            # History updates for en passant:
            game.last_move = locations
            game.last_move_type = piece

            # en passant updates
            if self.en_passant_:
                self.gameBoard.set_square_state(self.last_move)
                if self.curr_color == 0:
                    self.black_pieces_loc.remove(Location((locations[0][0], locations[1][1])))
                else:
                    self.white_pieces_loc.remove(Location((locations[0][0], locations[1][1])))

            # pieces location set updates + updating current player turn:
            if self.curr_color == 0:
                self.white_pieces_loc.remove(locations[0])
                self.white_pieces_loc.add(locations[1])
                if locations[1] in self.black_pieces_loc:
                    self.black_pieces_loc.remove(locations[1])

            else:
                self.black_pieces_loc.remove(locations[0])
                self.black_pieces_loc.add(locations[1])
                if locations[1] in self.white_pieces_loc:
                    self.white_pieces_loc.remove(locations[1])

            # check promotion
            self.promotion(locations)

            # update the color
            self.curr_color = 1 - self.curr_color

    def play(self):
        game_on = True
        while game_on:
            self.turn()
            threatening_piece, threatening_move = self.is_in_check()
            if self.check:
                if self.is_in_checkmate(threatening_move):
                    print(self.gameBoard)
                    game_on = False
                else:
                    self.check = False  # update for the next turn
        return 1-self.curr_color


if __name__ == "__main__":
    game = Game()
    winning_color = game.play()
    winning_color_dict = {0: "White", 1: "Black"}
    print(f"{winning_color_dict[winning_color]} WON!")
