import itertools
import unittest


def coords_calculation(coord_1, coord_2):
    """
    Static function that calculates the variation of coord_1 based on coord_2 displacement.
    """

    coord_X = int(coord_1[0]) + int(coord_2[0])
    coord_Y = int(coord_1[1]) + int(coord_2[1])
    return [coord_X, coord_Y]


def snake_movement(initial_position, movement):
    """
    Static function that calculates the new position of the snake from initial_position based on the movement.
    """

    final_position = []
    snake_head = coords_calculation(initial_position[0], movement)
    final_position.append(snake_head)
    for i in range(0, len(initial_position) - 1):
        final_position.append(initial_position[i])
    return final_position


class numberOfAvailableDifferentPaths:
    def __init__(self, b, s, d):
        """
        Class that obtains the number of available different paths with length depth that a snake could perform in a
        board.
        :param b: board size [r, c]
        :param s: snake array
        :param d: depth or path length
        """
        # INPUTS
        self.board = b
        self.snake = s
        self.depth = d

        # INPUTS VALIDATION BLOCK
        self.board_input_validation()
        self.snake_input_validation()
        self.depth_input_validation()

        # Problem solving
        self.result = None
        self.solve_problem()

    def board_input_validation(self):
        """
        Function that validates board input.
        :return: boolean result.
        """

        board_validation_list = []
        if len(self.board) == 2:
            for i in self.board:
                if 1 <= i <= 10 and type(i) is int:
                    board_validation_list.append(True)
                else:
                    board_validation_list.append(False)
            if False in board_validation_list:
                print("Constraint error: rows and columns of the board must be an integer number between 1 and 10.")
                return

        else:
            print("Constraint error: board length must be 2 (rows and columns).")

    def snake_input_validation(self):
        """
        Function that validates snake input.
        :return: boolean result.
        """
        snake_validation_list = []
        if 3 <= len(self.snake) <= 7:
            for i in range(0, len(self.snake)):
                if len(self.snake[i]) == 2:
                    if self.snake[i][0] <= self.board[0] - 1 and self.snake[i][1] <= self.board[1] - 1:
                        if i == 0:
                            snake_validation_list.append(True)
                        elif i != 0:
                            correlative_cell_0 = abs(self.snake[i][0] - self.snake[i - 1][0])
                            correlative_cell_1 = abs(self.snake[i][1] - self.snake[i - 1][1])
                            correlative_cell = correlative_cell_0 + correlative_cell_1

                            if correlative_cell == 1:
                                snake_validation_list.append(True)
                            else:
                                snake_validation_list.append(False)
                else:
                    print("Constraint error: coordinates of the snake part must be two (row and column).")

            if False in snake_validation_list:
                print("Constraint error: this snake cannot be fitted into the board.")
                return

        else:
            print("Constraint error: snake length must be a number between 3 and 7.")

    def depth_input_validation(self):
        """
        Function that validates depth input.
        :return: boolean result.
        """

        if 1 <= self.depth <= 20 and type(self.depth) is int:
            pass
        else:
            print("Constraint error: depth number must be an integer number between 1 and 20.")

    def solve_problem(self):
        """
        Main function that resolves the problem.
        :return: number of distinct valid paths of length *depth* that the *snake* could perform inside the *board*.
        """

        movements = 'LRDU'
        movements_coords = {'L': '[0, -1]', 'R': '[0, 1]', 'D': '[1, 0]', 'U': '[-1, 0]'}
        all_possible_movements = itertools.product(movements, repeat=self.depth)

        available_paths = 0

        for n in all_possible_movements:
            movement_legality = []
            snake_position = self.snake
            matrix = self.matrix_generator(snake_position)

            for k in n:
                snake_mov = snake_movement(snake_position, movements_coords[k].strip('][').split(', '))
                position_validation = self.snake_position_validation(snake_mov, matrix)
                if position_validation is True:
                    snake_position = snake_mov
                    movement_legality.append(True)
                    matrix = self.matrix_generator(snake_position)
                else:
                    break

            if len(movement_legality) == self.depth:
                available_paths += 1

        self.result = available_paths

    def matrix_generator(self, s):
        """
        Auxiliary function of solve_problem.
        Generates a matrix that represents the board, 0 is an empty cell, 1 is a snake cell.

        :param s: snake array
        :return: matrix array or False if there is an incorrect movement of the snake.
        """
        matrix = []
        for _ in range(0, self.board[0]):
            matrix_row = []
            for _ in range(0, self.board[1]):
                matrix_row.append(0)
            matrix.append(matrix_row)
        for i in s:
            if i[0] < 0 or i[1] < 0:
                return False
            else:
                matrix[i[0]][i[1]] = 1

        return matrix

    def matrix_calculation(self, matrix1, matrix2):
        """
        Auxiliary function of snake_position_validation.
        Generates a boolean return depending of the movement's correctness.
        :param matrix1: matrix generated before the movement.
        :param matrix2: matrix generated after the movement.
        :return: True if the movement is correct or False if it is not.
        """
        matrix = []
        for r in range(0, self.board[0]):
            row_matrix = []
            for c in range(0, self.board[1]):
                row_matrix.append(matrix1[r][c] - matrix2[r][c])
            matrix.append(row_matrix)

        result = 0
        for row in matrix:
            result += sum(row)

        if result == 0:
            return True
        else:
            return False

    def snake_position_validation(self, position, matrix):
        """
        Auxiliary function of solve_problem.
        Generates a boolean return depending of the movement's correctness.

        :param position: current position of the snake after the movement.
        :param matrix: matrix generated before the movement.
        :return: matrix_calculation result or False if the snake is out of the board.
        """
        try:
            new_matrix = self.matrix_generator(position)
            if new_matrix is False:
                return False
            result = self.matrix_calculation(matrix, new_matrix)
        except IndexError:
            return False

        return result

    def get_result(self):
        """
        Function that returns the result of the problem.
        :return: number of distinct valid paths of length *depth* that the *snake* could perform inside the *board*.
        """
        return self.result


class TestCase(unittest.TestCase):

    def test1(self):

        board_TC1 = [4, 3]
        snake_TC1 = [[2, 2], [3, 2], [3, 1], [3, 0], [2, 0], [1, 0], [0, 0]]
        depth_TC1 = 3

        result_TC1 = numberOfAvailableDifferentPaths(board_TC1, snake_TC1, depth_TC1).result
        expected_result_TC1 = 7

        self.assertEqual(expected_result_TC1, result_TC1)

    def test2(self):
        board_TC2 = [2, 3]
        snake_TC2 = [[0, 2], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2]]
        depth_TC2 = 10

        result_TC2 = numberOfAvailableDifferentPaths(board_TC2, snake_TC2, depth_TC2).result
        expected_result_TC2 = 1

        self.assertEqual(expected_result_TC2, result_TC2)

    def test3(self):
        board_TC3 = [10, 10]
        snake_TC3 = [[5, 5], [5, 4], [4, 4], [4, 5]]
        depth_TC3 = 4

        result_TC3 = numberOfAvailableDifferentPaths(board_TC3, snake_TC3, depth_TC3).result
        expected_result_TC3 = 81

        self.assertEqual(expected_result_TC3, result_TC3)


if __name__ == '__main__':
    unittest.main()
