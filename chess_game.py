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
                print(f'only {color_dict[self.curr_color]} can move, please move a piece of that color')
                return False
            if target_loc_piece is not None and target_loc_piece.color == self.curr_color:
                print("piece can't land on square populated by piece of the same color")
                return False
            # handle private case - pawn can't step forward to enemy's piece
            elif target_loc_piece is not None and target_loc_piece.color != self.curr_color:
                a= np.sign(np.array(move[1])-np.array(move[0]))
                b=np.array((color_sign[self.curr_color],0))
                if type(piece) == chess_definitions.Pawn and not np.array_equal(np.sign(np.array(move[1])-np.array(move[0])), np.array((color_sign[self.curr_color],0))):
                       # np.array_equal(abs(chess_definitions.Coordinates(move).sign_vector), np.array((1, 0))):
                    # the second condition is because only stepping forward would raise the following print:
                    print("pawn cant step forward into enemy's piece")
                    return False
        return True

    def movement_type_validation(self, move: Locations_List, piece: chess_definitions.Piece) -> bool:
        if type(piece) != chess_definitions.Knight:
            vector = chess_definitions.Coordinates(move).vector
            direction = chess_definitions.Coordinates(move).sign_vector
            if list(abs(direction)) != list(np.array((1, 0))) or list(abs(direction)) != list(np.array((0, 1))):
                if abs(vector[0]) != abs(vector[1]):  # checks that move is in possible direction for any piece.
                    return False
        else:
            direction = chess_definitions.Coordinates(move).vector
        if not np.any([np.array_equal(direction, element) for element in list(piece.sign_vector())]):
            if type(piece) == chess_definitions.Pawn:
                if not self.pawn_eating_validation(move):
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
            if move[0][0] != 6 - self.curr_color * 5 or not np.array_equal(vector, 2 * sign_vector):
                # case: jump 2 steps forward from initial rank
                if not self.pawn_eating:
                    print(f"{piece} can't reach to target square")
                    return False
        elif type(piece) == chess_definitions.King:
            if chess_definitions.Coordinates(move).vector == np.array([0, 2]):
                if not self.castling(move, "right"):
                    return False
            elif chess_definitions.Coordinates(move).vector == np.array([0, -2]):
                if not self.castling(move, "left"):
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
        squares_to_check: np.ndarray = chess_definitions.Coordinates(move).squares_path()
        for idx, square in enumerate(squares_to_check):
            print(tuple(square))
            if self.gameBoard.get_square_state(Location(tuple(square))) is not None and idx != len(
                    squares_to_check) - 1:
                print("move is not possible because it's way blocked by some piece/s")
                return False
        return True

    def is_not_revealing_king(self, move: Locations_List) -> bool:  # if its false: king is revealed.
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
            print("move is not possible because revealing king to check/checkmate")
            return False
        else:
            return True

    def is_in_check(self) -> bool:
        """
        There are two check cases. first case is when method called from revealing king- in that case, the current color
        checks that it isn't stepping into check- therefore piece list will be of the opposite color.
        second case is after moving the piece- check if current color is threatening the enemy's king - piece list will
        be of the current color.
        """
        if self.curr_color == 0:  # white's turn, so need to check whether black threatens
            piece_list = self.black_pieces_loc
            self.curr_color = 1
        else:  # the opposite
            piece_list = self.white_pieces_loc
            self.curr_color = 0
        for location in piece_list:
            if type(self.gameBoard.get_square_state(location)) == chess_definitions.King:
                continue
            move = Locations_List([location, self.kings_location[1 - self.curr_color]])
            if self.is_valid_move(str(move), move):
                self.check = True
                break
        else:
            self.check = False
        return self.check

    def is_in_checkmate(self) -> Locations_List:
        """
        Checkmate validation requires to check unintuitive possibility: if a move was found which protects the king from
        enemy's piece, there must be another check validation to make sure that the king is no longer threatened.
        """
        blocking_move = None
        if self.curr_color == 0:  # here passing throught possible piece that will protect the king.
            piece_list = self.white_pieces_loc
        else:
            piece_list = self.black_pieces_loc
        for location in piece_list:
            if type(self.gameBoard.get_square_state(location)) == chess_definitions.King:
                continue
            move = Locations_List([location, self.kings_location[1-self.curr_color]])
            squares_path: np.ndarray = chess_definitions.Coordinates(move).squares_path()
            squares_path = np.append(np.array([list(location)]), squares_path, axis=0)  # adds attacking piece loc to the list to check.
            for square_blocks_check in squares_path:
                move_to_block_check = Locations_List([location, tuple(square_blocks_check)])
                if move_to_block_check[1] == Location((1,7)):
                    pass
                print(move_to_block_check)
                if self.is_valid_move(str(move_to_block_check), move_to_block_check):
                    blocking_move = move_to_block_check
                    self.checkmate = False
                    break
            else:
                continue  # if the code reach this line, it won't execute the following break, as wished.
            break
        else:
            self.checkmate = True
        return blocking_move

    def en_passant(self, move: Locations_List) -> bool:
        """This method is called only from eating pawn method, and it handles the case in which enemy's pawn stepped
            2 squares to the same rank as the current moving pawn (opposite colors). In that case, the pawn allowed
            to eat even thought the relevant square is empty (and the previous pawn will disappear)."""
        if self.last_move_type != chess_definitions.Pawn or \
                self.last_move[1][0] != move[0][0] or self.last_move[1][1] != move[1][1] or \
                not np.array_equal(abs(chess_definitions.Coordinates(self.last_move).vector), np.array((2, 0))):
            print("Selected pawn can't eat with en-passant at the selected square")
            return False
        else:
            self.en_passant_ = True
            return True

    def castling(self, move: Locations_List, rook_side: str) -> bool:  # todo add case of long side rook path error(kn)
        condition_a = f"{color_dict[self.curr_color]}_cant_castle"
        condition_b = self.castling_possibilities_info[f"{rook_side}_{color_dict[self.curr_color]}_rook"]
        if condition_a or condition_b:
            print("requested castling is impossible")
            return False
        current_board = copy.deepcopy(self.gameBoard)
        king_current_loc = copy.deepcopy(self.kings_location[self.curr_color])
        side_dict = {"right": 1, "left": -1}
        # check whether king pass under check.
        self.kings_location[self.curr_color] = Location((7 - 7 * self.curr_color, 4 + side_dict[rook_side]))
        self.gameBoard.set_square_state(move, self.gameBoard.get_square_state(move[0]))
        self.is_in_check(self.kings_location[self.curr_color])
        self.gameBoard = current_board
        self.kings_location[self.curr_color] = king_current_loc
        # todo delete current board and king_current_loc from memory, it isn't required anymore? or is it deleted auto?
        if self.check:
            return False
        else:
            return True

    def promotion(self, move: Locations_List) -> None:  # these function called only once promotion is approved.
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
            if type(piece) != chess_definitions.Knight:
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
        string_move = self.enter_move()  # might need to add an exception?
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
            if self.gameBoard.get_square_state(locations[0]) == chess_definitions.Rook:
                self.castling_possibilities_info[f"{rook_side}_{color_dict[self.curr_color]}_rook"] = True

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
                self.curr_color = 1
            else:
                self.black_pieces_loc.remove(locations[0])
                self.black_pieces_loc.add(locations[1])
                if locations[1] in self.white_pieces_loc:
                    self.white_pieces_loc.remove(locations[1])
                self.curr_color = 0

            # check+checkmate validation for the next turn/endgame:
            if self.is_in_check():
                blocking_move = self.is_in_checkmate()  # would be Locations list if found blocking move, else: None
                if not self.checkmate:
                    kings_loc = copy.deepcopy(self.kings_location[self.curr_color])

                    # if self.is_in_check():

    def play(self):
        game_on = True
        while game_on:
            self.turn()
            if self.check:
                if self.checkmate:
                    game_on = False
        return self.curr_color  # need to switch the integer back to str by dictionary created at enter_move


if __name__ == "__main__":
    game = Game()
    winning_color = game.play()
    print(f"{winning_color} WON!")
