# -*- coding: utf-8 -*-

# Import pysirtet libs
import pysirtet

class TestPolyomino(object):
    '''
    Test polyomino definitions and transformations
    '''
    def setUp(self):
        '''
        Define data common to all tests
        '''
        self.grid_width = 10
        self.grid_height = 22
        self.constraints = [['' for j in range(self.grid_height)] for i in range(self.grid_width)]
        self.polyomino = pysirtet.Polyomino(
                             name='o',
                             coords=[[0, 0], [1, 0], [0, 1], [1, 1]],
                             colors={'normal': '#CC66CC',
                                     'light' : '#FC79FC',
                                     'dark'  : '#803B80'}
                         )

    def test_check_constraints(self):
        '''
        Test that constraints are met
        '''
        # Get function
        check = self.polyomino._check_constraints
        # Validate correct truth of all permutation classes of constraint (non)violation
        self.assertTrue(check([0, 3], self.constraints))
        self.assertTrue(check([5, 7], self.constraints))
        self.assertTrue(check([self.grid_width - 1, self.grid_height - 1], self.constraints))

        self.assertFalse(check([-1, 2], self.constraints))
        self.assertFalse(check([3, -5], self.constraints))
        self.assertFalse(check([self.grid_width + 1, 7], self.constraints))
        self.assertFalse(check([3, self.grid_height + 1], self.constraints))

        for i, c in enumerate(self.constraints[0]):
            self.constraints[0][i] = 'o'
        print(len(self.constraints))
        self.assertFalse(check([0, 5], self.constraints))
