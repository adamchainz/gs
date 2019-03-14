#!/usr/bin/env python
import sys
from copy import deepcopy

CUBE_SIZE = 6
NUM_PIECES = 54


def main():
    # print(sum(1 for p in all_positions(6) if (2, 2, 2) in p))
    # Print all positions in 4 sided cube passing through (1, 1, 1)
    # for position in all_positions(4):
    #     if (1, 1, 1) in position:
    #         cube = cube_with_position_taken(create_cube(4), position, 1)
    #         print_cube(cube)

    positions = all_positions(CUBE_SIZE)
    cube = create_cube(CUBE_SIZE)
    sys.setrecursionlimit(len(positions) * 2)
    solved_cube = next(find_solutions_newer(cube, positions, NUM_PIECES))
    # solved_cube = next(find_solutions_new(cube, CUBE_SIZE, positions, 50))
    print_cube(solved_cube)


def find_solutions_newer(cube, positions, positions_to_pick):
    head_position = positions[0]

    shared_positions = []
    non_shared_positions = []
    for position in positions:
        if any(c in head_position for c in position):
            shared_positions.append(position)
        else:
            non_shared_positions.append(position)

    for position in shared_positions:
        new_cube = cube_with_position_taken(cube, position, label=positions_to_pick)
        if positions_to_pick == 1:
            yield new_cube
        else:
            available = [p for p in non_shared_positions if all(new_cube[a][b][c] is None for a, b, c in p)]
            if available:
                yield from find_solutions_newer(
                    new_cube,
                    available,
                    positions_to_pick - 1,
                )


def find_solutions_new(cube, cube_size, positions, positions_to_pick):
    if positions_to_pick == 0:
        yield cube
        return

    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                if cube[x][y][z] is not None:
                    continue

                point = (x, y, z)
                positions_touching_point = []
                positions_not_touching_point = []
                for position in positions:
                    if point in position:
                        positions_touching_point.append(position)
                    else:
                        positions_not_touching_point.append(position)

                for position in positions_touching_point:
                    new_cube = cube_with_position_taken(cube, position, label=positions_to_pick)
                    allowed_positions = [
                        p for p in positions_not_touching_point
                        if all(new_cube[a][b][c] is None for a, b, c in p)
                    ]
                    yield from find_solutions_new(
                        new_cube,
                        cube_size,
                        allowed_positions,
                        positions_to_pick - 1,
                    )


def find_solutions(cube, positions, positions_to_pick):
    # Try skipping the head position
    if len(positions) > positions_to_pick:
        yield from find_solutions(cube, positions[1:], positions_to_pick)

    # Try taking the head position
    head_position = positions[0]
    new_cube = cube_with_position_taken(cube, head_position, label=positions_to_pick)
    if positions_to_pick == 1:
        yield new_cube
    else:
        new_positions = [
            p for p in positions[1:]
            if all(new_cube[a][b][c] is None for a, b, c in p)
        ]
        if len(new_positions) >= positions_to_pick:
            yield from find_solutions(new_cube, new_positions, positions_to_pick - 1)


def all_positions(cube_size):
    positions = set()
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                positions.update(positions_at_point(cube_size, x, y, z))
    return sorted(positions)


def positions_at_point(cube_size, x, y, z):
    # Output all the ways of putting a piece in at virtual co-ordinates x, y, z
    # The piece might be oriented with its long edge pointing into any of the 6
    # directions representing the faces of a cube. Then it might be rotated any
    # of 4 ways for its "stick" to point.
    # We trim the directions for the edges though down to three though, since
    # e.g. negative X is represented by positive X with a different starting
    # position inside the bounds of the cube.
    for axis in ('x', 'y', 'z'):
        for direction in (1, -1):
            for stick_axis in {'x', 'y', 'z'} - {axis}:
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
                    position = tuple(sorted([square_1, square_2, square_3, square_4]))
                    if all(
                        0 <= a < cube_size
                        and 0 <= b < cube_size
                        and 0 <= c < cube_size
                        for a, b, c in position
                    ):
                        yield tuple(sorted(position))


def test_all_positions_unfeasible_cube():
    assert all_positions(2) == []


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


def cube_with_position_taken(cube, position, label):
    new_cube = deepcopy(cube)
    for a, b, c in position:
        new_cube[a][b][c] = label
    return new_cube


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
