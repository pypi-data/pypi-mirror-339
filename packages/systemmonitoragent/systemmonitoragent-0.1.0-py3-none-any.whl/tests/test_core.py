import unittest
from SystemMonitorAgent.core import hello

class TestCore(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello, World!")
        self.assertEqual(hello("User"), "Hello, User!")

if __name__ == "__main__":
    unittest.main()