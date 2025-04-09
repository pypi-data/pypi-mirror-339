import unittest
from tests.util import interpret

class TestConditionalExecution(unittest.TestCase):
    def test_useless_statement(self):
        source = """
            bool a
            false: print("this should not be executed")
            true: print("", 0)
        """
        self.assertEqual("0", interpret(source))

    def test_if_else(self):
        source = """
            bool if_condition, else_condition
            int a, b
            true: a = 1
            true: b = 2
            true: if_condition = b < a || !true
            true: else_condition = !if_condition
            if_condition: print("", 0)
            else_condition: print("", 1)
        """
        self.assertEqual("1", interpret(source))


if __name__ == '__main__':
    unittest.main()
