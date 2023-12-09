import unittest
from unittest.mock import Mock
from Block import Block, BLOCKS_MATRIX
from Board import Board
from Player import Player

# @Sercan Berkpinar
# Unit tests to check that the functions are okay
    
class TestIsMoveValid(unittest.TestCase):
    def test_valid_on_same_position(self):
        board = Board()
        block = Block(BLOCKS_MATRIX[1], "blue")  # 1 x 1 Block
        board.board_insert(block,1,1)
        self.assertFalse(board.is_move_valid(1, 1, block))

    def test_block_next_door(self):
        board = Board()
        block = Block(BLOCKS_MATRIX[1], "yellow")
        board.board_insert(block, 1, 1)
        self.assertFalse(board.is_move_valid(1, 0, block))

    def test_adjacent_same_color_corner_valid(self):
        board = Board()
        block1 = Block(BLOCKS_MATRIX[1], "blue")
        block2 = Block(BLOCKS_MATRIX[1], "blue")
        board.board_insert(block1, 0, 0)
        self.assertTrue(board.is_move_valid(1, 1, block2))  

    def test_block_rotation_valid_move(self):
        board = Board()
        block1 = Block(BLOCKS_MATRIX[1], "blue")
        block2 = Block(BLOCKS_MATRIX[3], "blue")  # L-Block
        block2.rotate()
        board.board_insert(block2, 0,1)
        self.assertTrue(board.is_move_valid(0, 0, block1))

    def test_block_reflection_invalid_move(self):
        board = Board()
        block = Block(BLOCKS_MATRIX[3], "blue")  # L-Block
        block.reflect()
        board.board_insert(block, 0, 0)
        block.reflect()  
        self.assertFalse(board.is_move_valid(0, 0, block))  # Should fail because the space is already occupied
    
    def test_move_outside_board(self):
        board = Board()
        block = Block(BLOCKS_MATRIX[1], "blue")
        self.assertFalse(board.is_move_valid(20, 20, block)) 

class PlayerBlocks(unittest.TestCase):
    def test_block_insertion_reduces_remaining_blocks(self):
        board = Board()
        player = Player("red", board)
        initial_block_count = len(player.blocks)
        player.player_insert(3, 1, 2)
        # Check that the number of remaining blocks has been updated correctly
        self.assertEqual(len(player.blocks), initial_block_count - 1)
        # Check that the correct block has been removed
        self.assertNotIn(3, player.blocks)

    def test_insertion_of_nonexistent_block(self):
        board = Board()
        player = Player("red", board)
        with self.assertRaises(KeyError):
            player.player_insert(999, 1, 2)  # a non-existent block index

    def test_insertion_outside_board(self):
        board = Board()
        player = Player("red", board)
        # insert a block outside the boundaries of the game board
        with self.assertRaises(IndexError):
            player.player_insert(3, 20, 20)

# @Sercan Berkpinar 
# Implement Custom Test Runner for Enhanced Test Results Reporting

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_test_counts = {}
        self.class_success_counts = {}

    def startTest(self, test):
        super().startTest(test)
        test_class = test.__class__.__name__
        if test_class not in self.class_test_counts:
            self.class_test_counts[test_class] = 0
        self.class_test_counts[test_class] += 1

    def addSuccess(self, test):
        super().addSuccess(test)
        test_class = test.__class__.__name__
        if test_class not in self.class_success_counts:
            self.class_success_counts[test_class] = 0
        self.class_success_counts[test_class] += 1

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = CustomTestResult(self.stream, self.descriptions, self.verbosity)
        test(result)
        self.stream.writeln("\nTest results:")
        for class_name, test_count in result.class_test_counts.items():
            success_count = result.class_success_counts.get(class_name, 0)
            self.stream.writeln(f"{class_name}: {success_count} from {test_count} correct")
        return result
    
if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())