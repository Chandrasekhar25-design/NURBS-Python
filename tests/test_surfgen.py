"""
    Tests for the NURBS-Python package
    Released under The MIT License. See LICENSE file for details.
    Copyright (c) 2018 Onur Rauf Bingol

    Tests geomdl.GPGen module. Requires "pytest" to run.
"""
import os
import pytest
from geomdl import CPGen


@pytest.fixture
def grid():
    """ Generates a 3x4 control points grid """
    surfgrid = CPGen.Grid(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


@pytest.fixture
def grid2():
    """ Generates a 6x6 control points grid """
    surfgrid = CPGen.Grid(7, 13)
    surfgrid.generate(9, 9)
    return surfgrid


@pytest.fixture
def gridw():
    """ Generates a weighted control points grid """
    surfgrid = CPGen.GridWeighted(7, 13)
    surfgrid.generate(3, 4)
    return surfgrid


def test_grid_generate1():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.raises(ValueError):
        test_grid.generate(-1, 5)


def test_grid_generate2():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.raises(ValueError):
        test_grid.generate(5, -1)


def test_grid_generate3():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.warns(UserWarning):
        test_grid.generate(3.5, 4)


def test_grid_generate4():
    test_grid = CPGen.GridWeighted(7, 13)
    with pytest.warns(UserWarning):
        test_grid.generate(3, 4.2)


def test_grid_generate5(grid):
    # testing regeneration of the grid
    grid.generate(13, 17)

    assert grid._size_u == 13
    assert grid._size_v == 17
    assert len(grid.grid) == 14
    assert len(grid.grid[0]) == 18


def test_grid(grid):
    result = [[[0.0, 0.0, 0.0], [0.0, 3.25, 0.0], [0.0, 6.5, 0.0], [0.0, 9.75, 0.0], [0.0, 13.0, 0.0]],
              [[2.3333333333333335, 0.0, 0.0], [2.3333333333333335, 3.25, 0.0],
               [2.3333333333333335, 6.5, 0.0], [2.3333333333333335, 9.75, 0.0], [2.3333333333333335, 13.0, 0.0]],
              [[4.666666666666667, 0.0, 0.0], [4.666666666666667, 3.25, 0.0], [4.666666666666667, 6.5, 0.0],
               [4.666666666666667, 9.75, 0.0], [4.666666666666667, 13.0, 0.0]],
              [[7.0, 0.0, 0.0], [7.0, 3.25, 0.0], [7.0, 6.5, 0.0], [7.0, 9.75, 0.0], [7.0, 13.0, 0.0]]]

    assert grid.grid == result


def test_grid_reset1(grid):
    grid.reset()

    assert grid._grid_points == []
    assert grid._size_u == 0
    assert grid._size_v == 0
    assert grid._origin == [0.0, 0.0, 0.0]


def test_grid_reset2(gridw):
    gridw.weight = 0.33
    gridw.reset()

    assert gridw._grid_points == []
    assert gridw._size_u == 0
    assert gridw._size_v == 0
    assert gridw._origin == [0.0, 0.0, 0.0]
    assert gridw._cache['grid_points'] == []
    assert gridw._weight == 1.0


def test_grid_weight1(gridw):
    result = [[[0.0, 0.0, 0.0, 1.0], [0.0, 3.25, 0.0, 1.0], [0.0, 6.5, 0.0, 1.0],
               [0.0, 9.75, 0.0, 1.0], [0.0, 13.0, 0.0, 1.0]],
              [[2.3333333333333335, 0.0, 0.0, 1.0], [2.3333333333333335, 3.25, 0.0, 1.0],
               [2.3333333333333335, 6.5, 0.0, 1.0], [2.3333333333333335, 9.75, 0.0, 1.0],
               [2.3333333333333335, 13.0, 0.0, 1.0]],
              [[4.666666666666667, 0.0, 0.0, 1.0],
               [4.666666666666667, 3.25, 0.0, 1.0], [4.666666666666667, 6.5, 0.0, 1.0],
               [4.666666666666667, 9.75, 0.0, 1.0], [4.666666666666667, 13.0, 0.0, 1.0]],
              [[7.0, 0.0, 0.0, 1.0], [7.0, 3.25, 0.0, 1.0], [7.0, 6.5, 0.0, 1.0],
               [7.0, 9.75, 0.0, 1.0], [7.0, 13.0, 0.0, 1.0]]]

    # default weight is 1.0
    assert gridw.grid == result


def test_grid_weight2(gridw):
    with pytest.raises(TypeError):
        gridw.weight = "test string"


def test_grid_weight3(gridw):
    with pytest.raises(ValueError):
        gridw.weight = -0.1


def test_grid_weight4(gridw):
    # default weight should be 1.0
    assert gridw.weight == 1.0


def test_grid_weight5(gridw):
    # try to change weight
    gridw.weight = 0.35
    assert gridw.weight == 0.35


def test_grid_save1(grid):
    fname = "test_grid.txt"
    grid.save(fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_grid_save1_weighted(gridw):
    fname = "test_gridw.txt"
    gridw.save(fname)

    assert os.path.isfile(fname)
    assert os.path.getsize(fname) > 0

    # Clean up temporary file if exists
    if os.path.isfile(fname):
        os.remove(fname)


def test_grid_save2():
    test_grid = CPGen.Grid(5, 7)
    with pytest.raises(RuntimeError):
        # trying to save before generate()
        test_grid.save()


def test_grid_save3(grid):
    with pytest.raises(TypeError):
        # file name should be a string
        grid.save(5)


def test_grid_save4(grid):
    with pytest.warns(UserWarning):
        # impossible file name
        grid.save("")


def test_bumps1(grid2):
    grid2.bumps(num_bumps=2, all_positive=False, bump_height=5, base_extent=2)
    check_vals = grid2.grid

    check = False
    for rows in check_vals:
        for val in rows:
            # should consider negative values too
            if abs(val[2]) == 5.0:
                check = True

    assert check


def test_bumps1_all_positive_heights(grid2):
    grid2.bumps(num_bumps=2, all_positive=True, bump_height=5, base_extent=2)
    check_vals = grid2.grid

    check = False
    for rows in check_vals:
        for val in rows:
            if val[2] == 5.0:
                check = True

    assert check


def test_bumps2(grid2):
    with pytest.raises(RuntimeError):
        # impossible to add 10 bumps on this specific grid
        grid2.bumps(num_bumps=10, all_positive=False, bump_height=5, base_extent=2)


def test_bumps4():
    test_grid = CPGen.Grid(5, 7)
    with pytest.raises(RuntimeError):
        # bumps before calling generate()
        test_grid.bumps(num_bumps=3)


def test_bumps5(grid2):
    with pytest.warns(UserWarning):
        # non-integer num_bumps
        grid2.bumps(num_bumps=1.1, all_positive=False, bump_height=5, base_extent=2)


def test_bumps6(grid2):
    with pytest.raises(ValueError):
        # negative bump_height
        grid2.bumps(num_bumps=1, all_positive=False, bump_height=-5, base_extent=2)


def test_bumps7(grid2):
    with pytest.raises(ValueError):
        # non-bool all_positive argument
        grid2.bumps(num_bumps=1, all_positive=15, bump_height=5, base_extent=2)


def test_bumps8(grid2):
    with pytest.raises(ValueError):
        # large base_extent
        grid2.bumps(num_bumps=1, all_positive=False, bump_height=5, base_extent=7)


def test_bumps9(grid2):
    with pytest.raises(ValueError):
        # small base_extent
        grid2.bumps(num_bumps=1, all_positive=False, bump_height=5, base_extent=0)


def test_bumps10(grid2):
    with pytest.raises(ValueError):
        # large base_adjust
        grid2.bumps(num_bumps=1, all_positive=False, bump_height=5, base_extent=2, base_adjust=2)


def test_bumps11(grid2):
    with pytest.warns(UserWarning):
        # num_bumps <= 0
        grid2.bumps(num_bumps=0)
