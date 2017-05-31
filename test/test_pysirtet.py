# -*- coding: utf-8 -*-

# Import python libs
import random
import pytest
from contextlib import contextmanager

# Import pysirtet libs
from pysirtet import Polyomino, TetrominoName, Grid, Transformation
from pysirtet import tetrominoes, Config


# https://stackoverflow.com/a/42327075
@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


class TestPolyomino:
    '''
    Test the Polyomino class
    '''
    @pytest.fixture(autouse=True)
    def setup_grid(self):
        '''
        Setup program options and grid state
        '''
        self.opts = Config(test=True).get_opts()
        self.grid = Grid(self.opts)

    def test__check_grid(self):
        '''
        Test the constraint checking function
        '''
        # Test that all interior squares of an empty grid are valid
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                assert True == Polyomino._check_grid(Polyomino, (x, y), self.grid)

        # Test that interior squares that are occupied are invalid
        for i in range(random.randint(min(self.grid.width, self.grid.height), self.grid.width*self.grid.height)):
            self.grid[random.randint(0, self.grid.width - 1), random.randint(0, self.grid.height - 1)]['type'] = random.choice(tuple(TetrominoName))
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                assert (False if self.grid[x, y]['type'] != None else True) == Polyomino._check_grid(Polyomino, (x, y), self.grid)

        # Test that exterior squares are invalid (pick an arbitrary covering, $(wh)^2$, of the grid)
        x_out = [i for i in range(-self.grid.height//2, -1)] + [i for i in range(self.grid.width, self.grid.width + self.grid.height//2)]
        y_out = [j for j in range(-self.grid.width//2, -1)] + [j for j in range(self.grid.height, self.grid.height + self.grid.width//2)]
        for x in x_out:
            for y in y_out:
                assert False == Polyomino._check_grid(Polyomino, (x, y), self.grid)
        for x in range(self.grid.width):
            for y in y_out:
                assert False == Polyomino._check_grid(Polyomino, (x, y), self.grid)
        for x in x_out:
            for y in range(self.grid.height):
                assert False == Polyomino._check_grid(Polyomino, (x, y), self.grid)

    def test__min(self):
        '''
        Test the minimum coordinate function
        '''
        # Setup random 'polyomino'
        ordinal = random.randint(2, 11)
        coords = [[random.randint(0, self.grid.height) for i in range(2)] for j in range(ordinal)]
        p = Polyomino(None, None, coords)

        for i in range(2):
            assert p._min(i) == min([c[i] for c in coords])

    def test__max(self):
        '''
        Test the maximum coordinate function
        '''
        # Setup random 'polyomino'
        ordinal = random.randint(2, 11)
        coords = [[random.randint(0, self.grid.height) for i in range(2)] for j in range(ordinal)]
        p = Polyomino(None, None, coords)

        for i in range(2):
            assert p._max(i) == max([c[i] for c in coords])

    def test_rotate(self):
        '''
        Test polyomino rotations on the grid
        '''
        # For each tetromino
        for tetromino in tetrominoes:
            # Test each direction
            for direction in (Transformation.cw, Transformation.ccw):
                # Move piece to center of grid
                tetromino.translate([self.grid.width//2, self.grid.height//2], self.grid)
                rotation_states = {}
                # And cover the rotation space twice
                for quarter in range(9):
                    # Test that rotation is successful
                    assert True == tetromino.rotate(Transformation.cw, self.grid)
                    rotation_states[quarter] = tetromino.coords
                    if quarter - 4 in rotation_states:
                        # Test that rotations are isometric mod 4
                        assert rotation_states[quarter] == rotation_states[quarter - 4]

    def test_translate(self):
        '''
        Test polyomino translations on the grid
        '''
        # For each tetromino
        for tetromino in tetrominoes:
            # Test each single row/column translation
            for translation in ([-1, 0], [1, 0], [0, -1]):
                # Move piece to center of grid
                tetromino.translate([self.grid.width//2 - tetromino.o[0], self.grid.height//2 - tetromino.o[1]], self.grid)
                # Test that translation is successful
                assert True == tetromino.translate(translation, self.grid)

            # Test each extremal translation
            for translation in (Transformation.min, Transformation.max, Transformation.bottom):
                # Move piece to center of grid
                tetromino.translate([self.grid.width//2 - tetromino.o[0], self.grid.height//2 - tetromino.o[1]], self.grid)
                # Test that translation is successful
                assert True == tetromino.translate(translation, self.grid)
                # Test that translation is idempotent
                coords = tetromino.coords
                tetromino.translate(translation, self.grid)
                assert coords == tetromino.coords
                # Test that translation is extremal
                if translation == Transformation.min:
                    assert 0 == tetromino._min(0)
                if translation == Transformation.max:
                    assert self.grid.width == tetromino._max(0) + 1
                if translation == Transformation.bottom:
                    assert 0 == tetromino._min(1)


class TestGrid:
    '''
    Test the Grid class
    '''
    @pytest.fixture(autouse=True)
    def setup_grid(self):
        '''
        Setup program options and create a test grid instance
        '''
        self.opts = Config(test=True).get_opts()
        self.grid = Grid(self.opts)

    def test_get(self):
        '''
        Test getting squares in the grid
        '''
        # Test that interior squares are valid
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                with not_raises(IndexError) as e_info:
                    assert self.grid[[i, j]]['type'] == None

        # Test that exterior squares are invalid (pick an arbitrary covering, $(wh)^2$, of the grid)
        x_out = [i for i in range(-self.grid.height//2, -1)] + [i for i in range(self.grid.width, self.grid.width + self.grid.height//2)]
        y_out = [j for j in range(-self.grid.width//2, -1)] + [j for j in range(self.grid.height, self.grid.height + self.grid.width//2)]
        for x in x_out:
            for y in y_out:
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]]
        for x in range(self.grid.width):
            for y in y_out:
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]]
        for x in x_out:
            for y in range(self.grid.height):
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]]

    def test_set(self):
        '''
        Test setting squares in the grid
        '''
        # Test that interior squares are valid
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                with not_raises(IndexError) as e_info:
                    tetromino_name = random.choice(tuple(TetrominoName))
                    self.grid[[i, j]]['type'] = tetromino_name
                    assert self.grid[[i, j]]['type'] == tetromino_name

        # Test that exterior squares are invalid (pick an arbitrary covering, $(wh)^2$, of the grid)
        x_out = [i for i in range(-self.grid.height//2, -1)] + [i for i in range(self.grid.width, self.grid.width + self.grid.height//2)]
        y_out = [j for j in range(-self.grid.width//2, -1)] + [j for j in range(self.grid.height, self.grid.height + self.grid.width//2)]
        for x in x_out:
            for y in y_out:
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]] = random.choice(tuple(TetrominoName))
        for x in range(self.grid.width):
            for y in y_out:
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]] = random.choice(tuple(TetrominoName))
        for x in x_out:
            for y in range(self.grid.height):
                with pytest.raises(IndexError) as e_info:
                    self.grid[[x, y]] = random.choice(tuple(TetrominoName))
