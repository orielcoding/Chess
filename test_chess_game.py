import chess_definitions
import chess_game
import pytest
import numpy as np
from numpy import testing


def test_move_is_in_board():
    game = chess_game
    input_1 = game.move_is_in_board("a2 a3")
    input_2 = game.move_is_in_board("g6a7")

    assert input_1 == [(6, 0), (5, 0)]
    assert input_2 == [(2, 6), (1, 0)]
    with pytest.raises(ValueError) as e_info:
        game.move_is_in_board("g7:h9")
    with pytest.raises(ValueError) as e_info:
        game.move_is_in_board("n7:h3")


def test_color_move_validation():  # todo add case of pawn steps into enemy's pawn
    game = chess_game.Game()
    with pytest.raises(chess_definitions.WrongColorError) as e_info:
        game.color_move_validation(chess_game.Locations_List([(7, 0), (6, 0)]), chess_definitions.Rook(0))
    with pytest.raises(chess_definitions.WrongColorError):
        game.color_move_validation(chess_game.Locations_List([(0, 7), (1, 6)]), chess_definitions.Bishop(1))
    try_1 = game.color_move_validation(chess_game.Locations_List([(7, 0), (1, 0)]), chess_definitions.Rook(0))
    assert try_1 is None
    try_2 = game.color_move_validation(chess_game.Locations_List([(6, 0), (3, 3)]), chess_definitions.Bishop(0))
    assert try_2 is None

    # test if pawn will not step into enemy's piece
    with pytest.raises(TypeError):
        game.color_move_validation(chess_game.Locations_List([(5, 2), (6, 2)]), chess_definitions.Pawn(1))


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


def test_movement_type_validation():
    game = chess_game.Game()
    with pytest.raises(ValueError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(6, 0), (6, 1)]), chess_definitions.Pawn(0))
    with pytest.raises(ValueError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(5, 0), (6, 1)]), chess_definitions.Knight(0))
    with pytest.raises(ValueError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(2, 0), (5, 0)]), chess_definitions.Bishop(0))
    with pytest.raises(ValueError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(6, 0), (3, 3)]), chess_definitions.Rook(0))
    # testing pawn eating:
    with pytest.raises(ValueError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(5, 0), (6, 1)]), chess_definitions.Pawn(1))
    # testing en-passant
    with pytest.raises(chess_definitions.EnPassantError) as e_info:
        game.movement_type_validation(chess_game.Locations_List([(4, 3), (3, 4)]), chess_definitions.Pawn(0))

    game.last_move = chess_definitions.Locations_List([(1,0),(3,0)])
    game.last_move_type = chess_definitions.Pawn
    assert game.movement_type_validation(chess_game.Locations_List([(3, 1), (2, 0)]), chess_definitions.Pawn(0)) is None


def test_get_square_state():
    game = chess_game.Game()
    assert type(game.gameBoard.get_square_state((0, 0))) == chess_definitions.Rook
    assert type(game.gameBoard.get_square_state((7, 0))) == chess_definitions.Rook
    assert type(game.gameBoard.get_square_state((7, 3))) == chess_definitions.Queen
    assert type(game.gameBoard.get_square_state((7, 1))) == chess_definitions.Knight
    assert type(game.gameBoard.get_square_state((0, 5))) == chess_definitions.Bishop
    assert type(game.gameBoard.get_square_state((1, 2))) == chess_definitions.Pawn


def test_path_interruptions_validation():
    game = chess_game.Game()
    assert game.path_interruptions_validation(chess_game.Locations_List([(5, 0), (6, 1)]),
                                              chess_definitions.Knight(0)) is None
    assert game.path_interruptions_validation(chess_game.Locations_List([(2, 1), (4, 3)]),
                                              chess_definitions.Bishop(0)) is None
    with pytest.raises(ValueError) as e_info:
        game.path_interruptions_validation((chess_game.Locations_List([(0, 1), (4, 5)])), chess_definitions.Bishop(0))


def test_is_revealing_king():
    game1 = chess_game.Game()
    game1.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Bishop(1))
    with pytest.raises(chess_definitions.ExposeKingError) as e_info:
        game1.is_revealing_king(chess_game.Locations_List([(6, 3), (5, 3)]))

    game2 = chess_game.Game()
    game2.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Rook(1))
    assert game2.is_revealing_king(chess_game.Locations_List([(6, 3), (5, 3)])) is None

    game3 = chess_game.Game()
    game3.gameBoard.set_square_state(((0, 5), (4, 1)), chess_definitions.Bishop(1))
    game3.gameBoard.set_square_state(((7, 2), (6, 3)), chess_definitions.Bishop(0))
    assert game3.is_revealing_king(chess_game.Locations_List([(6, 3), (5, 2)])) is None

# def test_promotion(): # need to handle input
#     game = chess_game.Game()
#     assert game.promotion(chess_game.Locations_List([(1,0),(2,0)])) is None
#     with pytest.raises(TypeError) as e_info:
#         game.promotion(chess_game.Locations_List([(1,0),(0,0)]))

# def test_legal_move():
