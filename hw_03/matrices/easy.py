import numpy as np


def check_matrix_size(matrix):
    if not all(len(row) == len(matrix[0]) for row in matrix):
        raise ValueError('Incorrect matrix shape')


def check_matrices_matmul(first, second):
    if len(first[0]) != len(second):
        raise ValueError("Incorrect matrices shapes for matmul")


def check_matrices(first, second):
    if len(first) != len(second) or \
            len(first[0]) != len(second[0]):
        raise ValueError("Incorrect matrices shapes for operation")


class MyMatrix:
    check_matrix_size = staticmethod(check_matrix_size)
    check_matrices_matmul = staticmethod(check_matrices_matmul)
    check_matrices = staticmethod(check_matrices)

    def __init__(self, input_data):
        self.check_matrix_size(input_data)
        self.data = input_data

    def __add__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices(self.data, other.data)
        result = [list(map(sum, zip(*rows))) for rows in zip(self.data, other.data)]
        return MyMatrix(result)

    def __matmul__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices_matmul(self.data, other.data)
        result = [[sum(matrix_elem * other_elem for matrix_elem, other_elem in zip(matrix_row, other_col))
                   for other_col in zip(*other.data)]
                  for matrix_row in self.data]
        return MyMatrix(result)

    def __mul__(self, other):
        self.check_matrix_size(other.data)
        self.check_matrices(self.data, other.data)
        result = [[a * b for a, b in zip(*rows)] for rows in zip(self.data, other.data)]
        return MyMatrix(result)

    def __str__(self):
        result = "["
        for row in self.data:
            result += str(row) + '\n'
        return result[:-1] + "]"