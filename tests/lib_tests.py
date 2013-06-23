import unittest
from ..lib import (
    rules,
)

class RulesTester(unittest.TestCase):
    def test_win(self):
        win_boards = (
            "111   2  ",
            "111 2    ",
            "111    2 ",
            "   111 2 ",
            "1     222",
            
            "1  1  1  ",
            " 1  1  1 ",
            "  1  1  1",
            
            
            "1   1   1",
            "  1 1 1  ",
        )
        
        fail_boards = (
            "         ",
            "1 12 21 1",
            "121    2 ",
            "   121 2 ",
            "1     212",
        )
        
        for board in win_boards:
            self.assertNotEqual(rules.test_win(board), False, msg="Board = %s" % board)
        
        for board in fail_boards:
            self.assertEqual(rules.test_win(board), False)
