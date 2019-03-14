#!/usr/bin/env python
import random
from copy import deepcopy

CUBE_SIZE = 6
NUM_PIECES = 54


def main():
    cube = create_cube(CUBE_SIZE)
    solved_cube = next(find_solutions(cube, 1))
    print_cube(solved_cube)


def find_solutions(cube, current_piece):
    if current_piece < NUM_PIECES - 2:
        print(current_piece)
    for x in range(CUBE_SIZE):
        for y in range(CUBE_SIZE):
            for z in range(CUBE_SIZE):
                for position in get_piece_positions(cube, x, y, z):
                    new_cube = deepcopy(cube)
                    for a, b, c in position:
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


def get_piece_positions(cube, x, y, z):
    # Output all the ways of putting a piece in at virtual co-ordinates x, y, z
    # The piece might be oriented with its long edge pointing into any of the 6
    # directions representing the faces of a cube. Then it might be rotated any
    # of 4 ways for its "stick" to point
    positions = [
        (
            (x, y, z),
            (x + 1, y, z),
            (x + 2, y, z),
            (x + 1, y + 1, z),
        ),
        (
            (x, y, z),
            (x + 1, y, z),
            (x + 2, y, z),
            (x + 1, y - 1, z),
        ),
        (
            (x, y, z),
            (x + 1, y, z),
            (x + 2, y, z),
            (x + 1, y, z + 1),
        ),
        (
            (x, y, z),
            (x + 1, y, z),
            (x + 2, y, z),
            (x + 1, y, z - 1),
        ),

        (
            (x, y, z),
            (x, y + 1, z),
            (x, y + 2, z),
            (x + 1, y + 1, z),
        ),
        (
            (x, y, z),
            (x, y + 1, z),
            (x, y + 2, z),
            (x - 1, y + 1, z),
        ),
        (
            (x, y, z),
            (x, y + 1, z),
            (x, y + 2, z),
            (x, y + 1, z + 1),
        ),
        (
            (x, y, z),
            (x, y + 1, z),
            (x, y + 2, z),
            (x, y + 1, z + 2),
        ),

        (
            (x, y, z),
            (x, y, z + 1),
            (x, y, z + 2),
            (x + 1, y, z + 1),
        ),
        (
            (x, y, z),
            (x, y, z + 1),
            (x, y, z + 2),
            (x - 1, y, z + 1),
        ),
        (
            (x, y, z),
            (x, y, z + 1),
            (x, y, z + 2),
            (x, y + 1, z + 1),
        ),
        (
            (x, y, z),
            (x, y, z + 1),
            (x, y, z + 2),
            (x, y - 1, z + 1),
        ),
    ]

    for position in positions:
        if all(
            0 <= a < CUBE_SIZE
            and 0 <= b < CUBE_SIZE
            and 0 <= c < CUBE_SIZE
            and cube[a][b][c] is None
            for a, b, c in position
        ):
            yield position


def print_cube(cube):
    for layer_no, layer in enumerate(cube, start=1):
        print(f'Layer {layer_no}')
        for line in layer:
            for square in line:
                if square is None:
                    print('  .', end='')
                else:
                    print(str(square).rjust(3), end='')
            print('')
        print('')
        print('')


if __name__ == '__main__':
    main()
