import numpy as np

from matrices.easy import MyMatrix
from matrices.hard import MyHashableMatrix


def generate_artifacts(matrix_constructor, artifacts_path):
    np.random.seed(0)
    first_matrix = matrix_constructor(np.random.randint(0, 10, (10, 10)))
    second_matrix = matrix_constructor(np.random.randint(0, 10, (10, 10)))
    with open(f'{artifacts_path}/matrix+.txt', 'w') as file:
        file.write((first_matrix + second_matrix).__str__())
    with open(f'{artifacts_path}/matrix*.txt', 'w') as file:
        file.write((first_matrix * second_matrix).__str__())
    with open(f'{artifacts_path}/matrix@.txt', 'w') as file:
        file.write((first_matrix @ second_matrix).__str__())


def generate_artifacts_hard(artifacts_path):
    a = MyHashableMatrix([[1, 2], [3, 4]])
    b = MyHashableMatrix([[1, 1], [1, 1]])
    c = MyHashableMatrix([[1, 1], [4, 4]])
    d = MyHashableMatrix([[1, 1], [1, 1]])

    ab = a @ b
    c._matmul_hashes = {}
    cd = c @ d

    with open(f'{artifacts_path}/A.txt', 'w') as file:
        file.write(str(a))
    with open(f'{artifacts_path}/B.txt', 'w') as file:
        file.write(str(b))
    with open(f'{artifacts_path}/C.txt', 'w') as file:
        file.write(str(c))
    with open(f'{artifacts_path}/D.txt', 'w') as file:
        file.write(str(d))
    with open('artifacts/hard/AB.txt', 'w') as file:
        file.write(str(ab))
    with open(f'{artifacts_path}/CD.txt', 'w') as file:
        file.write(str(cd))
    with open('artifacts/hard/hash.txt', 'w') as file:
        file.write("AB hash:\n" + str(ab.__hash__()) + '\nCD hash:\n' + str(cd.__hash__()))


if __name__ == '__main__':
    generate_artifacts(MyMatrix, "artifacts/easy")
    generate_artifacts(MyMatrix, "artifacts/medium")
    generate_artifacts_hard("artifacts/hard")
