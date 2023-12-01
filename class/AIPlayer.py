from Player import Player
from Board import Board
from Block import Block
from secrets import SystemRandom
import random
from copy import deepcopy

class Move():

    coef: int                                                       # strength of the move (atm number of new corners)
    row: int
    col: int
    new_corners: list[tuple[int, int]]
    block: Block

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
    
    corners: list[tuple[int, int]]
    rnd_gen: SystemRandom

    def __init__(self, color, board: Board, blocks=None):
        super().__init__(color, board, blocks)
        self.corners = []
        self.rnd_gen = SystemRandom()

    # inserts random big block in the middle of the field
    def set_first_block(self):
        best_move = Move(0, 0, 0, [])
        random_block_idx = len(self.blocks) - self.rnd_gen.randint(0,3)
        random_big_block = self.blocks[random_block_idx]

        pos_row = 10
        pos_col = 10
        #i = 10

        for i in range(0,6,2):
            move = self.try_block(pos_row  + i, pos_col + i, random_big_block)
            if move > best_move:
                best_move = move

            move = self.try_block(pos_row - i, pos_col - i, random_big_block)
            if move > best_move:
                best_move = move

            move = self.try_block(pos_row + i, pos_col - i, random_big_block)
            if move > best_move:
                best_move = move

            move = self.try_block(pos_row - i, pos_col + i, random_big_block)
            if move > best_move:
                best_move = move

        self.player_insert(random_block_idx, best_move.row, best_move.col)
        self.corners += best_move.new_corners
        self.pop_corners()
        print(self.corners)
    
    def set_block(self):
        best_move = Move(0, 0, 0, [])
        block_idx, rand_block = self.get_random_block()

        for row, col in self.corners:
            pass

    def get_random_block(self, size = None):
        remaining_idx = self.get_remaining_block_idx()
        if not size:
            rand_idx = random.shuffle(remaining_idx)[0]
            return rand_idx, self.blocks[rand_idx]
        elif size == "small":
            small_idx = remaining_idx[:len(remaining_idx)//2 +1]
            rand_idx = random.shuffle(small_idx)[0]
            return rand_idx, self.blocks[rand_idx]
        elif size == "big":
            big_idx = remaining_idx[len(remaining_idx)//2:]
            rand_idx = random.shuffle(big_idx)[0]
            return rand_idx, self.blocks[rand_idx]
        else:
            raise ValueError(f"'{size}' is not a valid size")

    def find_block_position(self, row_to_fullfile, col_to_fullfile, block: Block):
        for _ in range(3):
            count_rows = len(block.block_matrix)
            count_cols = len(block.block_matrix[0])
            element = block.block_matrix[0][0]
            valid = self.board.is_move_valid(row_to_fullfile, col_to_fullfile, block)
            if element:
                if valid:
                    return row_to_fullfile, col_to_fullfile
            else:
                for j in range(1, 4):
                    if block.block_matrix[0][j]:
                        if self.board.is_move_valid(row_to_fullfile - j, col_to_fullfile, block):
                                return row_to_fullfile - j, col_to_fullfile
            
                    if block.block_matrix[j][0]:
                        if self.board.is_move_valid(row_to_fullfile, col_to_fullfile - j, block):
                                return row_to_fullfile, col_to_fullfile - j

            element = block.block_matrix[0][-1]
            if element:
                if valid:
                    return row_to_fullfile, col_to_fullfile
            else:
                for j in range(1, 4):
                    if block.block_matrix[0][j]:
                        if self.board.is_move_valid(row_to_fullfile + j, col_to_fullfile, block):
                                return row_to_fullfile + j, col_to_fullfile
            
                    if block.block_matrix[j][0]:
                        if self.board.is_move_valid(row_to_fullfile, col_to_fullfile - j, block):
                                return row_to_fullfile, col_to_fullfile - j
            
            

                



            block.rotate()
            



        pass


    def get_remaining_block_idx(self):
        return [idx for idx in self.blocks]


        

    # inserts a block in a copied board and checks how many new corners it generates
    def try_block(self, row: int, col: int, block: Block) -> Move:
        if not self.board.is_move_valid(row, col, block):
            demo_board = deepcopy(self.board)
            demo_board.board_insert(block, row, col)
            new_corners = []
            for row_i in range(row -1, len(block.block_matrix) + row + 1):
                for col_i in range(col -1, len(block.block_matrix[0]) + col + 1):
                    if self.is_corner(demo_board, row_i, col_i):
                        if (row_i, col_i) not in self.corners:
                            new_corners.append((row_i, col_i))
            return Move(len(new_corners)-1, row, col, new_corners, block)


        
    # pops old corners (which are now invalid)
    def pop_corners(self):
        for row, col in self.corners:
            if not self.is_corner(self.board, row, col):
                self.corners.pop((row, col))

    # check if the position is a corner (possibility to insert new block)
    def is_corner(self, board: Board, row, col) -> bool:
        corner = False

        if row > 20 or row < 0 or col > 20 or col < 0:
            return False

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