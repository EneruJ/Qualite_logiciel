import unittest
from calculator.operations import add, subtract, multiply, divide, power, mod, sqrt, factorial, fibonacci

class TestCalculatorOperations(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(3, 2), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(subtract(3, 1), 2)
        self.assertEqual(subtract(1, 1), 0)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(-1, -1), 1)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(-1, 1), -1)
        self.assertEqual(divide(-1, -1), 1)
        with self.assertRaises(ValueError):
            divide(1, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(4, 0.5), 2)
        self.assertEqual(power(2, -1), 0.5)

    def test_mod(self):
        self.assertEqual(mod(10, 3), 1)
        self.assertEqual(mod(10, 5), 0)
        self.assertEqual(mod(-10, 3), 2)
        with self.assertRaises(ValueError):
            mod(1, 0)

    def test_sqrt(self):
        self.assertEqual(sqrt(4), 2)
        self.assertEqual(sqrt(9), 3)
        self.assertEqual(sqrt(0), 0)
        with self.assertRaises(ValueError):
            sqrt(-1)

if __name__ == '__main__':
    unittest.main()
