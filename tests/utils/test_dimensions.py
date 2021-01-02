"""test_dimensions.py

Unit tests for dimensions utility functions.
"""


import unittest

from utils.dimensions import ndims


class TestStruct(unittest.TestCase):
    def test_1dimensional(self):
        """Test ndims in 1 dimension."""
        self.assertEqual(ndims(1, "1"), (1,))
        self.assertEqual(ndims(11, "1"), (11,))
        self.assertEqual(ndims(11, "2"), (12,))
        self.assertEqual(ndims(11, "3"), (12,))
        self.assertEqual(ndims(11, "5"), (15,))
        self.assertEqual(ndims(11, "7"), (14,))
        self.assertEqual(ndims(11, "11"), (11,))
        self.assertEqual(ndims(11, "13"), (13,))

    def test_2dimensional(self):
        """Test ndims in 2 dimensions."""
        self.assertEqual(ndims(1, "1:1"), (1, 1,))
        self.assertEqual(ndims(2, "1:1"), (2, 2,))
        self.assertEqual(ndims(4, "1:1"), (2, 2,))
        self.assertEqual(ndims(4, "1:2"), (2, 4,))
        self.assertEqual(ndims(8, "1:1"), (3, 3,))
        self.assertEqual(ndims(8, "1:2"), (2, 4,))
        self.assertEqual(ndims(11, "1:11"), (1, 11,))
        self.assertEqual(ndims(11, "1:13"), (1, 13,))

    def test_3dimensional(self):
        """Test ndims in 3 dimensions."""
        self.assertEqual(ndims(1, "1:1:1"), (1, 1, 1,))
        self.assertEqual(ndims(2, "1:1:1"), (2, 2, 2,))
        self.assertEqual(ndims(2, "1:1:2"), (1, 1, 2,))
        self.assertEqual(ndims(4, "1:1:1"), (2, 2, 2,))
        self.assertEqual(ndims(8, "1:1:1"), (2, 2, 2,))
        self.assertEqual(ndims(8, "1:2:4"), (1, 2, 4,))
        self.assertEqual(ndims(11, "1:1:11"), (1, 1, 11,))
        self.assertEqual(ndims(11, "1:1:13"), (1, 1, 13,))
