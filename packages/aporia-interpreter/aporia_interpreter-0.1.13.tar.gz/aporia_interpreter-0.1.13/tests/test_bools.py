import unittest
from tests.util import interpret

class TestBooleans(unittest.TestCase):
    def test_equal(self):
        source = """
        int a
        true: a = 1.3
        true: print("", a == 1)
        """
        self.assertEqual("true", interpret(source))

    def test_greater_equal(self):
        source = """
        true: print("", 3 >= 3.01)
        """
        self.assertEqual("false", interpret(source))

    def test_smaller_equal(self):
        source = """
        true: print("", 3 <= 3.01)
        """
        self.assertEqual("true", interpret(source))

    def test_smaller(self):
        source = """
        true: print("", 3.01 < 3.01)
        """
        self.assertEqual("false", interpret(source))

    def test_greater(self):
        source = """
        true: print("", !(3.01 > 3.01 || 1 > 3) && 3 > 1)
        """
        self.assertEqual("true", interpret(source))

    def test_negation(self):
        source = """
            bool a, b
            true: a = !(1 == 1)
            true: b = !(!(a))
            true: print("",b)
        """
        self.assertEqual("false", interpret(source))

    def test_and(self):
        source = """
            bool a, b, c
            true: a = true
            true: b = false
            true: c = (a && !b) && b
            true: print("",c)
        """
        self.assertEqual("false", interpret(source))

    def test_or(self):
        source = """
            bool a, b, c
            true: a = true
            true: b = false
            true: c = (!a || b) || b
            true: print("",c)
        """
        self.assertEqual("false", interpret(source))

    def test_complex(self):
        source = """
            bool a, b, c
            true: a = true
            true: b = false
            true: b = a && (b || (c || !a)) && a
            true: print("",b)
        """
        self.assertEqual("false", interpret(source))

if __name__ == '__main__':
    unittest.main()
