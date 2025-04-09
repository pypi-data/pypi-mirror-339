import unittest
from tests.util import interpret

class TestArithmetic(unittest.TestCase):
    def test_order_of_operations(self):
        source = """
        true: print("", 1 - (3 + 2) * 2)
        """
        self.assertEqual('-9', interpret(source))

    def test_float(self):
        source = """
        true: print("", 0.1 + 0.8)
        """
        self.assertEqual('0.9', interpret(source))

    def test_multiplication(self):
        source = """
        float a
        int b
        true: a = 1.8
        true: b = 2
        true: print("", (a + 1) * b)
        """
        self.assertEqual('5.6', interpret(source))

    def test_modulo(self):
        source = """
        int a, b
        true: a = 18
        true: b = (a % 12) % 2
        true: print("", b)
        """
        self.assertEqual('0', interpret(source))

    def test_division(self):
        source = """
        int a
        true: a = 1
        true: print("", a / 2.0)
        """
        self.assertEqual('0.5', interpret(source))

    def test_division2(self):
        source = """
        float a
        true: a = 1
        true: print("", a / 2)
        """
        self.assertEqual('0.5', interpret(source))

    def test_division3(self):
        source = """
        int a
        true: a = 1
        true: print("", a / 2)
        """
        self.assertEqual('0', interpret(source))

    def test_floor_division(self):
        source = """
        int a, b
        true: a = 28
        true: b = a // 5
        true: print("", b)
        """
        self.assertEqual('5', interpret(source))

    def test_floor_division2(self):
        source = """
        int a
        true: a = 1
        true: print("", a / 2)
        """
        self.assertEqual('0', interpret(source))



if __name__ == '__main__':
    unittest.main()
