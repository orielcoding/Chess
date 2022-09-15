import chess_definitions
import chess_game
import pytest
import numpy as np
from numpy import testing

def test_move_is_in_board():
    game = chess_game.Game()
    input_1 = game.move_is_in_board("a2 a3")
    input_2 = game.move_is_in_board("g6a7")

    assert input_1 == ((6, 0), (5, 0))
    assert input_2 == ((2, 6), (1, 0))
    with pytest.raises(ValueError) as e_info:
        game.move_is_in_board("g7:h9")
    with pytest.raises(ValueError) as e_info:
        game.move_is_in_board("n7:h3")


def test_color_move_validation():
    game = chess_game.Game()
    with pytest.raises(chess_definitions.WrongColorError) as e_info:
        game.color_move_validation(((7, 0), (6, 0)))
    with pytest.raises(chess_definitions.WrongColorError):
        game.color_move_validation(((0, 7), (1, 6)))
    try_1 = game.color_move_validation(((6, 0), (1, 0)))
    assert try_1 == None
    try_2 = game.color_move_validation(((6, 0), (3, 3)))
    assert try_2 == None


def test_coordinates():
    vector_1 = chess_definitions.Coordinates(((6, 0), (5, 0)))
    testing.assert_array_equal(vector_1.vector , np.array([-1,0]))
    testing.assert_array_equal(vector_1.sign_vector, np.array([-1, 0]))
    vector_2 = chess_definitions.Coordinates(((7, 1), (5, 2)))
    testing.assert_array_equal(vector_2.vector, np.array([-2, 1]))
    testing.assert_array_equal(vector_2.sign_vector, np.array([-1, 1]))
    vector_3 = chess_definitions.Coordinates(((7, 0), (7, 0)))
    testing.assert_array_equal(vector_3.vector, np.array([0, 0]))
    testing.assert_array_equal(vector_3.sign_vector, np.array([0, 0]))

def test_squares_path():
    c = chess_definitions.Coordinates(((7, 1), (4, 1)))
    dist_1 = c.squares_path()
    testing.assert_array_equal(dist_1 , np.array([[6,1],[5,1]]))

# def test_movement_type_validation():
#     game = chess_game.Game()
#     with pytest.raises(ValueError) as e_info:
#         game.movement_type_validation(((6, 0), (6, 1)),chess_definitions.Pawn(0))