import unittest
from tests.util import interpret

class TestMisc(unittest.TestCase):
    def test_empty_program(self):
        source = ""
        self.assertEqual("", interpret(source))

    def test_default_values(self):
        source = """
        int a
        float b
        bool c
        true: print("", a)
        true: print("", b)
        true: print("", c)
        """
        self.assertEqual("0\n0.0\nfalse", interpret(source))


if __name__ == '__main__':
    unittest.main()
