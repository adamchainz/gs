#!/usr/bin/env python
import sys
from copy import deepcopy

CUBE_SIZE = 6
NUM_PIECES = 54


def main():
    positions = list(all_positions(CUBE_SIZE))
    cube = create_cube(CUBE_SIZE)
    sys.setrecursionlimit(len(positions) * 2)
    solved_cube = next(find_solutions(cube, positions, NUM_PIECES))
    print_cube(solved_cube)


def find_solutions(cube, positions, positions_to_pick):
    if positions_to_pick > len(positions):
        return

    current_position = positions[0]
    remaining_positions = positions[1:]
    if all(cube[a][b][c] is None for a, b, c in current_position):
        new_cube = deepcopy(cube)
        for a, b, c in current_position:
            new_cube[a][b][c] = positions_to_pick
        new_positions_to_pick = positions_to_pick - 1
        if new_positions_to_pick == 0:
            yield new_cube
        else:
            yield from find_solutions(new_cube, remaining_positions, new_positions_to_pick)
    yield from find_solutions(cube, remaining_positions, positions_to_pick)


def all_positions(cube_size):
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                for position in positions_at_point(cube_size, x, y, z):
                    yield position


def positions_at_point(cube_size, x, y, z):
    # Output all the ways of putting a piece in at virtual co-ordinates x, y, z
    # The piece might be oriented with its long edge pointing into any of the 6
    # directions representing the faces of a cube. Then it might be rotated any
    # of 4 ways for its "stick" to point.
    # We trim the directions for the edges though down to three though, since
    # e.g. negative X is represented by positive X with a different starting
    # position inside the bounds of the cube.
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
            for a, b, c in position
        ):
            yield tuple(sorted(position))


def test_all_positions_unique():
    positions = list(all_positions(6))
    assert len(positions) == len(set(positions))


def test_all_positions_bounds():
    positions = set(all_positions(6))
    first_position = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 0, 2),
        (0, 1, 1),
    )
    assert first_position in positions
    last_position = (
        (5, 4, 4),
        (5, 5, 3),
        (5, 5, 4),
        (5, 5, 5),
    )
    assert last_position in positions


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
                    print('  .', end='')
                else:
                    print(str(square).rjust(3), end='')
            print('')
        print('')
        print('')


if __name__ == '__main__':
    main()
