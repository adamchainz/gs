#!/usr/bin/env python
from copy import deepcopy

CUBE_SIZE = 6
NUM_PIECES = 36


def main():
    cube = create_cube(CUBE_SIZE)
    solved_cube = next(find_solutions(cube, 1))
    print_cube(solved_cube)


def find_solutions(cube, current_piece):
    for x in range(CUBE_SIZE):
        for y in range(CUBE_SIZE):
            for z in range(CUBE_SIZE):
                positions = [
                    (x, y, z),
                    (x, y, z + 1),
                    (x, y, z + 2),
                    (x, y + 1, z + 1),
                ]

                try:
                    can_fit = all(cube[a][b][c] is None for (a, b, c) in positions)
                except IndexError:
                    can_fit = False

                if can_fit:
                    new_cube = deepcopy(cube)
                    for a, b, c in positions:
                        new_cube[a][b][c] = current_piece
                    if current_piece == NUM_PIECES:
                        yield new_cube
                    else:
                        yield from find_solutions(new_cube, current_piece + 1)


def create_cube(size):
    return [
        [
            [None for x in range(size)]
            for y in range(size)
        ]
        for z in range(size)
    ]


def test_create_cube_1():
    assert create_cube(1) == [[[None]]]


def test_create_cube_2():
    assert create_cube(2) == [
        [
            [None, None],
            [None, None],
        ],
        [
            [None, None],
            [None, None],
        ],
    ]


def print_cube(cube):
    for layer_no, layer in enumerate(cube, start=1):
        print(f'Layer {layer_no}')
        for line in layer:
            for square in line:
                if square is None:
                    print(' . ', end='')
                else:
                    print(str(square).rjust(3), end='')
            print('')
        print('')
        print('')


if __name__ == '__main__':
    main()
