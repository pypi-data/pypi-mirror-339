# coding = utf-8
"""
:Date: 2025-3-29 Latest
:Description: A package for calculate Math problem contain easy calculation and easy linear algebra problem,
              in the future author will add functions to solve easy geometry problems.
"""
import numpy as np

class EC:
    @staticmethod
    def sum(x, y):
        """
        :param x: the first value, number or list and other are all OK
        :param y: the second value, number or list and other are all OK
        :return: the summary of the two values
        """
        return sum(x) + sum(y)

    @staticmethod
    def subtract(x, y):
        """
        :param x: the first value, number or list and other are all OK
        :param y: the second value, number or list and other are all OK
        :return: to subtract the two values
        """
        return sum(x) - sum(y)

    @staticmethod
    def multiply(x, y):
        """
        :param x: the first value, number or list and other are all OK
        :param y: the second value, number or list and other are all OK
        :return: multiply the two values
        """
        return sum(x) * sum(y)

    @staticmethod
    def divide(x, y, int_divide: int = None, decimal_places=None):
        """
        :param x: numerator, number or list and other are all
        :param y: denominator, number or list and other are all but cannot be zero !
        :param int_divide: bool value, to judge user whether need exact division
        :param decimal_places: the number of digits after decimal point
        :return: for division
        """
        if y == 0:
            return "Error! Division by zero is not allowed."
        elif int_divide == 0:
            result = x / y
            return round(result, decimal_places)
        elif int_divide == 1:
            int_result = x // y
            return int_result

    @staticmethod
    def square(x, y):
        """
        :param x: the truth of a matter
        :param y: index
        :return: for quadratic root
        """
        return x ** y

    @staticmethod
    def square_root(number, numerator, denominator, decimal_places: int = None):
        """
        :param number: the truth of a matter
        :param numerator: numerator of root
        :param denominator: denominator of root
        :param decimal_places: the number of digits after decimal point
        :return: for rooting
        """
        if number < 0 and number % 2 == 0:
            return "Error! Cannot calculate square root of a negative number."
        result = number ** (numerator / denominator)
        return round(result, decimal_places)


class EL:
    @staticmethod
    def inverse(arr: list):
        """
        :param arr: list, inverse number
        :return: count inverse number
        """
        inversions = sum(1 for i in range(len(arr)) for j in range(i + 1, len(arr)) if arr[i] > arr[j])
        return inversions

    @staticmethod
    def determinant(arr: list) -> int:
        """
        :param arr: list, det determinant
        :return: result of determinant
        """
        dimension = len(arr)
        if dimension == 1:
            return arr[0][0]
        elif dimension == 2:
            return arr[0][0] * arr[1][1] - arr[0][1] * arr[1][0]
        else:
            det = 0
            for i in range(dimension):
                sub_matrix = [row[:i] + row[i + 1:] for row in arr[1:]]
                det += ((-1) ** i) * arr[0][i] * EL.determinant(sub_matrix)
            return det

    @staticmethod
    def cofactor(arr: list) -> list:
        """
        :param arr: list, det determinant
        :return: for algebraic cofactor
        """
        cofactor_matrix = []
        for i in range(len(arr)):
            cofactor_row = []
            for j in range(len(arr)):
                minor_matrix = [row[:j] + row[j + 1:] for row in (arr[:i] + arr[i + 1:])]
                cofactor_row.append(((-1) ** (i + j)) * EL.determinant(minor_matrix))
            cofactor_matrix.append(cofactor_row)
        return cofactor_matrix

    @staticmethod
    def matrix_show(matrix, num_rows: int = None, num_columns: int = None, by_row=True, by_column=False):
        if isinstance(matrix, np.ndarray):
            matrix = matrix.tolist()
        def get_dimension(matrix):
            if isinstance(matrix, list):
                if len(matrix) == 0:
                    return 1
                return 1 + get_dimension(matrix[0])
            return 0

        dim = get_dimension(matrix)
        def flatten_to_2d(matrix, dim):
            if dim == 1:
                return [matrix]
            elif dim == 2:
                return matrix
            else:
                flattened = []
                for sub_matrix in matrix:
                    flattened.extend(flatten_to_2d(sub_matrix, dim - 1))
                return flattened

        if dim == 1:
            if num_rows is None and num_columns is None:
                num_columns = len(matrix)
                num_rows = 1
            elif num_rows is None:
                num_rows = len(matrix) // num_columns + (len(matrix) % num_columns > 0)
            elif num_columns is None:
                num_columns = len(matrix) // num_rows + (len(matrix) % num_rows > 0)

            if by_row and num_rows:
                for i in range(num_rows):
                    row = '  '.join(str(x) for x in matrix[i * num_columns: (i + 1) * num_columns])
                    print(row)
            elif by_column and num_columns:
                for i in range(num_columns):
                    column = '  '.join(str(matrix[j * num_columns + i]) for j in range(num_rows))
                    print(column)
            else:
                print("Invalid format option. Please specify either by_row or by_column.")

        elif dim >= 2:
            flat_matrix = flatten_to_2d(matrix, dim)
            if num_rows is None:
                num_rows = len(flat_matrix)
            if num_columns is None:
                num_columns = len(flat_matrix[0])

            if by_row and num_rows:
                for i in range(num_rows):
                    row = '  '.join(str(x) for x in flat_matrix[i])
                    print(row)
            elif by_column and num_columns:
                for i in range(num_columns):
                    column = '  '.join(str(flat_matrix[j][i]) for j in range(num_rows))
                    print(column)
            else:
                print("Invalid format option. Please specify either by_row or by_column.")

        else:
            print("Invalid dimension detected.")


class EG:
    @staticmethod
    def circle_square(r, pi=3.141592653589793):
        """
        :param r: radius
        :param pi: const pi
        :return: circle square
        """
        return pi * (r ** 2)

    @staticmethod
    def spherical_volume(r, pi=3.141592653589793):
        """
        :param r: spherical radius
        :param pi: const pi
        :return: spherical volume
        """
        return 4 * (pi * r ** 3) / 3

    @staticmethod
    def cube_volume(length):
        """
        :param length: cube length
        :return: cube volume
        """
        return length ** 3

    @staticmethod
    def cuboid_volume(length, width, height):
        """
        :param length: cuboid length
        :param width: cuboid width
        :param height: cuboid height
        :return: cuboid volume
        """
        return length * width * height
