#!/usr/bin/env python
import random
from copy import deepcopy

CUBE_SIZE = 6
NUM_PIECES = 48


def main():
    cube = create_cube(CUBE_SIZE)
    solved_cube = next(find_solutions(cube, 1))
    print_cube(solved_cube)


def find_solutions(cube, current_piece):
    for x in range(CUBE_SIZE):
        for y in range(CUBE_SIZE):
            for z in range(CUBE_SIZE):
                if cube[x][y][z] is not None:
                    continue
                for position in get_piece_positions(x, y, z):
                    if all(cube[a][b][c] is None for (a, b, c) in position):
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


def get_piece_positions(x, y, z):
    # Output all the ways of putting a piece in at virtual co-ordinates x, y, z
    # The piece might be oriented with its long edge pointing into any of the 6
    # directions representing the faces of a cube. Then it might be rotated any
    # of 4 ways for its "stick" to point
    positions = []
    for axis in ('x', 'y', 'z'):
        for direction in (1, -1):
            for stick_axis in list({'x', 'y', 'z'} - {axis}):
                for stick_direction in (1, -1):
                    # Square 1 : always target point
                    square_1 = (x, y, z)
                    # Square 2: one step along axis
                    square_2 = (
                        x + (direction if axis == 'x' else 0),
                        y + (direction if axis == 'y' else 0),
                        z + (direction if axis == 'z' else 0),
                    )
                    # Square 3: two steps along axis
                    square_3 = (
                        x + (2 * direction if axis == 'x' else 0),
                        y + (2 * direction if axis == 'y' else 0),
                        z + (2 * direction if axis == 'z' else 0),
                    )
                    # Square 4: 'stick', offset from square 2
                    square_4 = (
                        square_2[0] + (stick_direction if stick_axis == 'x' else 0),
                        square_2[1] + (stick_direction if stick_axis == 'y' else 0),
                        square_2[2] + (stick_direction if stick_axis == 'z' else 0),
                    )
                    position = [square_1, square_2, square_3, square_4]
                    if all(0 <= x < CUBE_SIZE and 0 <= y < CUBE_SIZE and 0 <= z < CUBE_SIZE for x, y, z in position):
                        positions.append([square_1, square_2, square_3, square_4])
    random.shuffle(positions)
    yield from positions


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
