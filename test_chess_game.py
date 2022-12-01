import chess_definitions
import chess_game
import pytest
import numpy as np
from numpy import testing


def test_get_square_state():
    game = chess_game.Game()
    assert type(game.gameBoard.get_square_state((0, 0))) == chess_definitions.Rook
    assert type(game.gameBoard.get_square_state((7, 0))) == chess_definitions.Rook
    assert type(game.gameBoard.get_square_state((7, 4))) == chess_definitions.Queen
    assert type(game.gameBoard.get_square_state((7, 1))) == chess_definitions.Knight
    assert type(game.gameBoard.get_square_state((0, 5))) == chess_definitions.Bishop
    assert type(game.gameBoard.get_square_state((1, 2))) == chess_definitions.Pawn


def test_coordinates():
    vector_1 = chess_definitions.Coordinates(chess_game.Locations_List([(6, 0), (5, 0)]))
    testing.assert_array_equal(vector_1.vector, np.array([-1, 0]))
    testing.assert_array_equal(vector_1.sign_vector, np.array([-1, 0]))
    vector_2 = chess_definitions.Coordinates(chess_game.Locations_List([(7, 1), (5, 2)]))
    testing.assert_array_equal(vector_2.vector, np.array([-2, 1]))
    testing.assert_array_equal(vector_2.sign_vector, np.array([-1, 1]))
    vector_3 = chess_definitions.Coordinates(chess_game.Locations_List([(7, 0), (7, 0)]))
    testing.assert_array_equal(vector_3.vector, np.array([0, 0]))
    testing.assert_array_equal(vector_3.sign_vector, np.array([0, 0]))


def test_squares_path():  # doesn't test real moves.
    try_1 = chess_definitions.Coordinates(chess_game.Locations_List([(7, 1), (4, 1)]))
    dist_1 = try_1.squares_path()
    testing.assert_array_equal(dist_1, np.array([[6, 1], [5, 1], [4, 1]]))

    try_2 = chess_definitions.Coordinates(chess_game.Locations_List([(6, 1), (7, 5)]))
    dist_2 = try_2.squares_path()
    testing.assert_array_equal(dist_2, np.array([[7, 2], [8, 3], [9, 4], [10, 5]]))


def test_move_is_in_board():
    game = chess_game
    input_1 = game.move_is_in_board("a2 a3")
    input_2 = game.move_is_in_board("g6a7")

    assert input_1 == [(6, 0), (5, 0)]
    assert input_2 == [(2, 6), (1, 0)]
    with pytest.raises(chess_definitions.NotInBoardError) as e_info:
        game.move_is_in_board("g7:h9")
    with pytest.raises(chess_definitions.NotInBoardError) as e_info:
        game.move_is_in_board("n7:h3")


def test_color_move_validation():  # todo add case of pawn steps into enemy's pawn
    print("")
    game = chess_game.Game()
    print("try 1: ")
    try_1 = game.color_move_validation(chess_game.Locations_List([(7, 0), (1, 0)]), chess_definitions.Rook(0))
    assert try_1 is True
    print("try 2: ")
    try_2 = game.color_move_validation(chess_game.Locations_List([(6, 0), (3, 3)]), chess_definitions.Bishop(0))
    assert try_2 is True
    print("try 3: ")
    try_3 = game.color_move_validation(chess_game.Locations_List([(7, 0), (6, 0)]), chess_definitions.Rook(0))
    assert try_3 is False
    print("try 4: ")
    try_4 = game.color_move_validation(chess_game.Locations_List([(0, 7), (1, 6)]), chess_definitions.Bishop(1))
    assert try_4 is False
    # test if pawn will not step into enemy's piece
    game.curr_color = 1
    print(print("try 5: "))
    try_5 = game.color_move_validation(chess_game.Locations_List([(1, 2), (6, 2)]), chess_definitions.Pawn(1))
    assert try_5 is False  # todo check why it also returns None


def test_en_passant():
    game = chess_game.Game()
    print("")
    print("try 1: ")
    try_1 = game.en_passant(chess_game.Locations_List([(3,1),(2,0)]))
    assert try_1 is False
    game.last_move_type = chess_definitions.King
    game.last_move = chess_game.Locations_List([(1,0),(3,0)])
    print("try 2:")
    try_2 = game.en_passant(chess_game.Locations_List([(3, 1), (2, 0)]))
    assert try_2 is False
    game.last_move_type = chess_definitions.Pawn
    print("try 3: ")
    try_3 = game.en_passant(chess_game.Locations_List([(3, 1), (2, 0)]))
    assert try_3 is True
    print("try 4: ")
    try_4 = game.en_passant(chess_game.Locations_List([(3, 1), (2, 2)]))
    assert try_4 is False


def test_pawn_eating_validation():
    game = chess_game.Game()
    print("")
    print("try 1: ")
    try_1 = game.pawn_eating_validation(chess_game.Locations_List([(2, 1), (1, 0)]))
    assert try_1 is True
    print("try 2: ")
    try_2 = game.pawn_eating_validation(chess_game.Locations_List([(2, 1), (3, 0)]))
    assert try_2 is False
    game.curr_color = 1
    print("try 3: ")
    try_3 = game.pawn_eating_validation(chess_game.Locations_List([(5, 1), (6, 0)]))
    assert try_3 is True
    print("try 4: ")
    try_4 = game.pawn_eating_validation(chess_game.Locations_List([(2, 1), (4, 0)]))
    assert try_4 is False


def test_movement_type_validation():
    print("")
    game = chess_game.Game()
    print("try 1: ")
    try_1 = game.movement_type_validation(chess_game.Locations_List([(6, 0), (6, 1)]), chess_definitions.Pawn(0))
    assert try_1 is False
    print("try 2: ")
    try_2 = game.movement_type_validation(chess_game.Locations_List([(5, 0), (6, 1)]), chess_definitions.Knight(0))
    assert try_2 is False
    print("try 3: ")
    try_3 = game.movement_type_validation(chess_game.Locations_List([(2, 0), (5, 0)]), chess_definitions.Bishop(0))
    assert try_3 is False
    print("try 4: ")
    try_4 = game.movement_type_validation(chess_game.Locations_List([(6, 0), (3, 3)]), chess_definitions.Rook(0))
    assert try_4 is False
    # testing pawn eating:
    print("try 5: ")
    try_5 = game.movement_type_validation(chess_game.Locations_List([(5, 0), (6, 1)]), chess_definitions.Pawn(1))
    assert try_5 is False
    # testing en-passant
    print("try 6: ")
    try_6 = game.movement_type_validation(chess_game.Locations_List([(4, 3), (3, 4)]), chess_definitions.Pawn(0))
    assert try_6 is False
    # pawn eating
    print("try pawn eating: ")
    assert game.movement_type_validation(chess_game.Locations_List([(2, 1), (1, 0)]), chess_definitions.Pawn(0)) is True
    # en passant
    print("try en passant: ")
    game.last_move = chess_definitions.Locations_List([(1, 0), (3, 0)])
    game.last_move_type = chess_definitions.Pawn
    game.black_pieces_loc.remove(chess_game.Location((1,0)))
    game.black_pieces_loc.add(chess_game.Location((3,0)))
    assert game.movement_type_validation(chess_game.Locations_List([(3, 1), (2, 0)]), chess_definitions.Pawn(0)) is True


def test_path_interruptions_validation():
    print("")
    game = chess_game.Game()
    print("try 1: ")
    try_1 = game.path_interruptions_validation(chess_game.Locations_List([(5, 0), (6, 1)]),chess_definitions.Knight(0))
    assert try_1 is True
    print("try 2: ")
    try_2 = game.path_interruptions_validation(chess_game.Locations_List([(2, 1), (4, 3)]),chess_definitions.Bishop(0))
    assert try_2 is True
    print("try 3: ")
    try_3 = game.path_interruptions_validation((chess_game.Locations_List([(0, 1), (4, 5)])), chess_definitions.Bishop(0))
    assert try_3 is False


def test_distance_validation(): # todo complete after castlinh
    game = chess_game.Game()
    print("")
    print("pawn tests:")
    print("try_1: ")
    try_1 = game.distance_validation(chess_game.Locations_List([(6,0),(4,0)]),chess_definitions.Pawn(0))
    assert try_1 is True
    print("try_2: ")
    try_2 = game.distance_validation(chess_game.Locations_List([(5,0),(3,0)]),chess_definitions.Pawn(0))
    assert try_2 is False
    print("try_3: ")
    game.curr_color = 1
    try_3 = game.distance_validation(chess_game.Locations_List([(1, 0), (3, 0)]), chess_definitions.Pawn(1))
    assert try_3 is True
    print("try_4: ")
    try_4 = game.distance_validation(chess_game.Locations_List([(2, 0), (4, 0)]), chess_definitions.Pawn(1))
    assert try_4 is False

    print("")
    print("king tests:")


def test_promotion():
    game = chess_game.Game()
    game.promotion(chess_game.Locations_List([(1, 0), (0, 0)]))
    assert type(game.gameBoard.get_square_state(chess_definitions.Location((0,0)))) is chess_definitions.Queen


#def test_castling():

def test_is_in_check():
    game1 = chess_game.Game()
    print("")
    print("try 1: ")
    game1.gameBoard.set_square_state(chess_game.Locations_List([(6,3), (4,3)]), chess_definitions.Pawn(0))
    game1.gameBoard.set_square_state(chess_game.Locations_List([(0, 5), (4, 1)]), chess_definitions.Bishop(1))
    game1.black_pieces_loc.remove(chess_game.Location((0,5)))
    game1.black_pieces_loc.add(chess_game.Location((4,1)))
    try_1_piece, try_1_locations = game1.is_in_check()
    assert try_1_piece == chess_definitions.Bishop(1) and try_1_locations == [(4, 1), (7, 4)]

    game2 = chess_game.Game()
    print("")
    print("try 2: ")
    game2.gameBoard.set_square_state(chess_game.Locations_List([(1, 0), (5, 5)]), chess_definitions.Knight(1))
    game2.black_pieces_loc.remove(chess_game.Location((1, 0)))
    game2.black_pieces_loc.add(chess_game.Location((5, 5)))
    try_2_piece, try_2_locations = game2.is_in_check()
    assert try_2_piece == chess_definitions.Knight(1) and try_2_locations == [(5, 5), (7, 4)]

    game3 = chess_game.Game()
    print("")
    print("try 3: ")
    game3.curr_color = 1
    game3.gameBoard.set_square_state(chess_game.Locations_List([(0, 4), (4, 4)]), chess_definitions.King(1))
    game3.kings_location[game3.curr_color] = chess_game.Location((4,4))
    game3.gameBoard.set_square_state(chess_game.Locations_List([(6, 5), (5, 5)]), chess_definitions.Pawn(0))
    game3.white_pieces_loc.remove(chess_game.Location((6, 5)))
    game3.white_pieces_loc.add(chess_game.Location((5, 5)))
    try_3_piece, try_3_locations = game3.is_in_check()
    assert try_3_piece == chess_definitions.Pawn(0) and try_3_locations == [(5, 5), (4, 4)]


def test_is_not_revealing_king():
    print("")
    game1 = chess_game.Game()
    print("try 1: ")
    game1.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Bishop(1))
    game1.black_pieces_loc.remove(chess_game.Location((0,5)))
    game1.black_pieces_loc.add(chess_game.Location((4,1)))
    try_1 = game1.is_not_revealing_king(chess_game.Locations_List([(6, 3), (5, 3)]))
    assert try_1 is False

    game2 = chess_game.Game()
    print("try 2: ")
    game2.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Rook(1))
    game2.black_pieces_loc.remove(chess_game.Location((0, 5)))
    game2.black_pieces_loc.add(chess_game.Location((4, 1)))
    try_2 = game2.is_not_revealing_king(chess_game.Locations_List([(6, 3), (5, 3)]))
    assert try_2 is True

    game3 = chess_game.Game()
    print("try 3: ")
    game3.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Bishop(1))
    game3.gameBoard.set_square_state(((7, 2), (6, 3)), chess_definitions.Bishop(0))
    game3.black_pieces_loc.remove(chess_game.Location((0, 5)))
    game3.black_pieces_loc.add(chess_game.Location((4, 1)))
    assert game3.is_not_revealing_king(chess_game.Locations_List([(6, 3), (5, 2)])) is True


def test_is_in_checkmate():
    game1 = chess_game.Game()
    print("")
    print("try 1: ")
    game1.gameBoard.set_square_state(chess_game.Locations_List([(6,3), (4,3)]), chess_definitions.Pawn(0))
    game1.gameBoard.set_square_state(chess_game.Locations_List([(0, 5), (4, 1)]), chess_definitions.Bishop(1))
    game1.black_pieces_loc.remove(chess_game.Location((0,5)))
    game1.black_pieces_loc.add(chess_game.Location((4,1)))
    try_1 = game1.is_in_checkmate(chess_definitions.Bishop(1),chess_definitions.Locations_List([(4,1),(7,4)]))
    assert try_1 is False

    game2 = chess_game.Game()
    print("")
    print("try 2: ")
    game2.gameBoard.set_square_state(chess_game.Locations_List([(1, 0), (5, 5)]), chess_definitions.Knight(1))
    game2.black_pieces_loc.remove(chess_game.Location((1, 0)))
    game2.black_pieces_loc.add(chess_game.Location((5, 5)))
    try_2 = game2.is_in_checkmate(chess_definitions.Knight(1),chess_definitions.Locations_List([(5,5),(7,4)]))
    assert try_2 is False

    game3 = chess_game.Game()
    print("")
    print("try 3: ")
    game3.curr_color = 1
    game3.gameBoard.set_square_state(chess_game.Locations_List([(0, 4), (4, 4)]), chess_definitions.King(1))
    game3.kings_location[game3.curr_color] = chess_game.Location((4,4))
    game3.gameBoard.set_square_state(chess_game.Locations_List([(6, 5), (5, 5)]), chess_definitions.Pawn(0))
    game3.white_pieces_loc.remove(chess_game.Location((6, 5)))
    game3.white_pieces_loc.add(chess_game.Location((5, 5)))
    try_3 = game3.is_in_checkmate(chess_definitions.Pawn(0),chess_definitions.Locations_List([(5,5),(4,4)]))
    assert try_3 is False
