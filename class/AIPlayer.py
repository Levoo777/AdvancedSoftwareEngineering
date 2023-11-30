from Player import Player
from Board import Board
from Block import Block
from secrets import SystemRandom
from copy import deepcopy

class Move():
    def __init__(self, coef, row, col, new_corners, block = None):
        self.coef = coef
        self.row = row
        self.col = col
        self.new_corners = new_corners
        self.block = block
    
    def __gt__(self, other: 'Move') -> bool:
        if self.coef > other.coef:
            return True
        return False

class AIPlayer(Player):
    
    corners: list
    rnd_gen: SystemRandom

    def set_first_block(self):
        self.rnd_gen = SystemRandom()
        self.corners = []
        best_move = Move(0, 0, 0, [])
        random_block_idx = len(self.blocks) - self.rnd_gen.randint(0,3)
        random_big_block = self.blocks[random_block_idx]

        pos_row = 9
        pos_col = 8

        for i in range(0,6,2):

            if not self.board.is_move_valid(pos_row  + i, pos_col + i, random_big_block):
                c, new_corners = self.try_block(pos_row  + i, pos_col + i, random_big_block)
                move = Move(c, pos_row + i, pos_col + i, new_corners)
                if move > best_move:
                    best_move = move

            if not self.board.is_move_valid(pos_row - i, pos_col - i, random_big_block):
                c, new_corners = self.try_block(pos_row - i, pos_col - i, random_big_block)
                move = Move(c, pos_row - i, pos_col - i, new_corners)
                if move > best_move:
                    best_move = move

            if not self.board.is_move_valid(pos_row + i, pos_col - i, random_big_block):
                c, new_corners = self.try_block(pos_row + i, pos_col - i, random_big_block)
                move = Move(c, pos_row + i, pos_col - i, new_corners)
                if move > best_move:
                    best_move = move

            if not self.board.is_move_valid(pos_row - i, pos_col + i, random_big_block):
                c, new_corners = self.try_block(pos_row - i, pos_col + i, random_big_block)
                move = Move(c, pos_row - i, pos_col + i, new_corners)
                if move > best_move:
                    best_move = move

        self.player_insert(random_block_idx, best_move.row, best_move.col)
        self.corners += best_move.new_corners
        print(self.corners)
        self.pop_corners()
        print(self.corners)

            

    # inserts a block in a copied board and checks how many new corners it generates
    def try_block(self, row: int, col: int, block: Block):
        demo_board = deepcopy(self.board)
        demo_board.board_insert(block, row, col)
        new_corners = []
        for row_i in range(row -1, len(block.block_matrix) + row + 1):
            for col_i in range(col -1, len(block.block_matrix[0]) + col + 1):
                if self.is_corner(demo_board, row_i, col_i):
                    if (row_i, col_i) not in self.corners:
                        new_corners.append((row_i, col_i))
        return len(new_corners)-1, new_corners
        
    # pops old corners (which are now invalid)
    def pop_corners(self):
        for row, col in self.corners:
            if not self.is_corner(self.board, row, col):
                self.corners.pop((row, col))

    # check if the position is a corner(possibility to insert new block)
    def is_corner(self, board: Board, row, col) -> bool:
        corner = False
        if board.matrix[row][col]:
            return False
        for i in [-1, 1]:
            if board.matrix[row + i][col] == self.color:
                return False
            if board.matrix[row][col+i] == self.color:
                return False
            if board.matrix[row+i][col+i] == self.color:
                corner = True
            if board.matrix[row-i][col+i] == self.color:
                corner = True
        return corner
        


new_board = Board()
ai = AIPlayer("red", new_board)
new_board.show_board()
ai.set_first_block()
new_board.show_board()