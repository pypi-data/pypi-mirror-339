# tests/test_operations.py

import unittest
from mathutils import add, multiply, power

class TestMathUtils(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 7)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)

if __name__ == "__main__":
    unittest.main()