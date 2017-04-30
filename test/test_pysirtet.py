# -*- coding: utf-8 -*-

# Import python libs
import random
# Import pysirtet libs
from pysirtet import Polyomino, Tetrominoes, Grid
from pysirtet import get_opts

class TestPolyomino:
    '''
    Test the Polyomino class
    '''
    def test__check_constraints(self):
        '''
        Test the constraint checking function
        '''
        opts = get_opts(test=True)
        w = opts['size']['width'] = random.randint(5, 101)
        h = opts['size']['height'] = random.randint(5, 101)
        grid = Grid(opts)

        # Test that all interior points of an empty grid are valid
        for x in range(w):
            for y in range(h):
                assert True == Polyomino._check_constraints(Polyomino, (x, y), grid)

        # Test that interior points corresponding to occupied squares are invalid
        for i in range(random.randint(min(w, h), w*h)):
            grid[random.randint(0, w - 1), random.randint(0, h - 1)] = random.choice(tuple(Tetrominoes))
        for x in range(w):
            for y in range(h):
                assert (False if grid[x, y] != None else True) == Polyomino._check_constraints(Polyomino, (x, y), grid)

        # Test that exterior points are invalid
        x_out = [i for i in range(-h, -1)] + [i for i in range(w, w + h)]
        y_out = [j for j in range(-w, -1)] + [j for j in range(h, h + w)]
        for x in x_out:
            for y in y_out:
                assert False == Polyomino._check_constraints(Polyomino, (x, y), grid)
        for x in range(w):
            for y in y_out:
                assert False == Polyomino._check_constraints(Polyomino, (x, y), grid)
        for x in x_out:
            for y in range(h):
                assert False == Polyomino._check_constraints(Polyomino, (x, y), grid)
