import unittest
from Block import Block, BLOCKS_MATRIX
from Board import Board

class TestIsMoveValid(unittest.TestCase):
#setup board
    def test_valid_move(self):
        board = Board()
        block = Block(BLOCKS_MATRIX[1], "blue")  # Ein Beispielblock
        board.board_insert(block,1,1)
        # Test für einen gültigen Zug
        self.assertFalse(board.is_move_valid(1, 1, block))

if __name__ == '__main__':
    unittest.main()
