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
        #best_move = Move(0, 0, 0, [])
        random_block_idx = len(self.blocks) - self.rnd_gen.randint(0,7)
        random_big_block = self.blocks[random_block_idx]

        #pos_row = 10
        #pos_col = 10
        #i = 10
        valid_move = False

        while valid_move == False:
            if not self.board.matrix[0][0]:
                pos_row = 0
                pos_col = 0
                move = self.try_block(pos_row, pos_col, random_big_block)
                if self.board.matrix[0][0]:
                    valid_move = True

            elif not self.board.matrix[19][0]:
                pos_row = 19
                pos_col = 0
                move = self.try_block(pos_row -2, pos_col, random_big_block)
                if self.board.matrix[19][0]:
                    valid_move = True
            
            elif not self.board.matrix[0][19]:
                pos_row = 0
                pos_col = 19
                move = self.try_block(pos_row, pos_col, random_big_block -2)
                if self.board.matrix[0][19]:
                    valid_move = True

            else:
                pos_row = 19
                pos_col = 19
                move = self.try_block(pos_row,  -2, random_big_block -2)
                if self.board.matrix[19][19]:
                    valid_move = True

        self.player_insert(random_block_idx, move.row, move.col)
        self.corners += move.new_corners
        #self.pop_corners()
        print(self.corners)
    
   

    

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
        best_move = Move(0, 0, 0, [])
        count_rows = len(block.block_matrix)
        count_cols = len(block.block_matrix[0])
        for _ in range (2):
            for _ in range(4):
                
                element = block.block_matrix[0][0]
                
                if element:
                    if self.board.is_move_valid(row_to_fullfile, col_to_fullfile, block):
                        move = self.try_block(row_to_fullfile,  col_to_fullfile, block)
                        if move > best_move:
                            best_move = move
                        #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                        
                else:
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[0][j]:
                            if self.board.is_move_valid(row_to_fullfile - j, col_to_fullfile, block):
                                move = self.try_block(row_to_fullfile - j, col_to_fullfile, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                
                                    

                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[j][0]:
                            if self.board.is_move_valid(row_to_fullfile, col_to_fullfile - j, block):
                                move = self.try_block(row_to_fullfile, col_to_fullfile - j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                
                                    



                element = block.block_matrix[-1][0]

                if element:
                    valid = self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile, block)
                    if valid:
                        move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile, block)
                        if move > best_move:
                            best_move = move
                        #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                        
                else:
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[-1][j]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - j, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                
                                    
                
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[-j-1][0]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                

                            
                element = block.block_matrix[0][-1]

                if element:
                    valid = self.board.is_move_valid(row_to_fullfile , col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                    if valid:
                        move = self.try_block(row_to_fullfile , col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                        if move > best_move:
                            best_move = move
                        #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                       
                        
                else:
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[0][-j-1]:
                            if self.board.is_move_valid(row_to_fullfile, col_to_fullfile - len(block.block_matrix)[0] + 1 + j, block):
                                move = self.try_blockrow_to_fullfile, col_to_fullfile - len(block.block_matrix)[0] + 1 + j, block
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                   
                
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[j][-1]:
                            if self.board.is_move_valid(row_to_fullfile -j, col_to_fullfile - len(block.block_matrix)[0] + 1, block):
                                move = self.try_block(row_to_fullfile -j, col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                
                            
                
                element = block.block_matrix[-1][-1]

                if element:
                    valid = self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 , col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                    if valid:
                        move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 , col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                        if move > best_move:
                            best_move = movemove = self.try_block()
        
                        #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                        
                     
                else:
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[-1][-j-1]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - len(block.block_matrix)[0] + 1 + j, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - len(block.block_matrix)[0] + 1 + j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                  
                                    
                
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[-j-1][-1]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile - len(block.block_matrix)[0] + 1, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile - len(block.block_matrix)[0] + 1, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                

                block.rotate()
            block.reflect()
        
        if best_move == Move(0, 0, 0, []):
            return best_move

        pass


    def get_remaining_block_idx(self):
        return [idx for idx in self.blocks]
    
    def get_best_corner(self):
        best_corner = (100, 100)
        for row, col in self.corners:
            if best_corner == (100, 100):
                best_corner = (row, col)
                old_strength = (row-9,5)**2 + (col-9,5)**2
            else:
                strength = (row-9,5)**2 + (col-9,5)**2
                if strength < old_strength:
                    old_strength = strength
                    best_corner = (row, col)
        return best_corner



        

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
        
    def set_block(self):
        best_move = Move(0, 0, 0, [])
        new_board.show_board()
        best_row, best_col = self.get_best_corner()

        best_idx= 0
        counter = 0

        while counter < 8:

            idx, block = self.get_random_block("big")
            new_best_move = self.find_block_position(best_row, best_col, block)
            if best_move == Move(0, 0, 0, []):
                best_move = new_best_move
                best_idx = idx
            else:
                if new_best_move > best_move:
                    best_move = new_best_move
                    best_idx = idx
            counter += 1


        while best_move == Move(0, 0, 0, []) and counter < 16:
            best_row, best_col = self.get_random_corner()
            idx, block = self.get_random_block()
            new_best_move = self.find_block_position(best_row, best_col, block)
            if best_move == Move(0, 0, 0, []):
                best_move = new_best_move
                best_idx = idx 
            else:
                if new_best_move > best_move:
                    best_move = new_best_move 
                    best_idx = idx
            counter += 1

        self.player_insert(best_idx, best_move.row, best_move.col)
        self.corners += best_move.new_corners
        self.pop_corners()
        print(self.corners)

        

    def get_random_corner(self):
        copied_corners = deepcopy(self.corners)
        return random.shuffle(copied_corners)[0]

new_board = Board()
ai = AIPlayer("red", new_board)
new_board.show_board()
ai.set_first_block()






