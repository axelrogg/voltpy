import unittest
from src.voltpy.utils import find_root


class TestUtils(unittest.TestCase):
    def test_find_root(self):
        # Test with a simple quadratic function: x^2 - 4 = 0, root is 2
        func = lambda x: x**2 - 4
        fprime = lambda x: 2 * x
        root = find_root(func, fprime, x0=1)
        self.assertAlmostEqual(root, 2)

        # Test with another quadratic function: x^2 - 3x + 2 = 0, roots are 1 and 2
        func = lambda x: x**2 - 3 * x + 2
        fprime = lambda x: 2 * x - 3
        root = find_root(func, fprime, x0=0)
        self.assertAlmostEqual(root, 1)


if __name__ == "__main__":
    unittest.main()
