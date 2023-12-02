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
    
    def __eq__(self, other: 'Move') -> bool:
        if self.coef == other.coef and self.row == other.row and self.col == other.col and self.new_corners == other.new_corners:
            return True
        return False
    
    def __str__(self):
        res = f"coef: {self.coef}, row: {self.row}, col: {self.col}, newcorners: {self.new_corners}, block:{self.block}"
        return res


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
            print("Hallo")
            random_block_idx = len(self.blocks) - self.rnd_gen.randint(0,7)
            random_big_block = self.blocks[random_block_idx]

            if not self.board.matrix[0][0]:
                pos_row = 0
                pos_col = 0
                print("a")
                move = self.try_block_first(pos_row, pos_col, random_big_block)
                print("b")
                if random_big_block.block_matrix[0][0]:
                    valid_move = True

            elif not self.board.matrix[19][0]:
                pos_row = 19
                pos_col = 0
                move = self.try_block_first(pos_row -2, pos_col, random_big_block)
                if random_big_block.block_matrix[-1][0] and len(random_big_block.block_matrix) == 3 and len(random_big_block.block_matrix[0]) == 3:
                    valid_move = True
            
            elif not self.board.matrix[0][19]:
                pos_row = 0
                pos_col = 19
                move = self.try_block_first(pos_row, pos_col, random_big_block -2)
                if random_big_block.block_matrix[0][-1] and len(random_big_block.block_matrix) == 3 and len(random_big_block.block_matrix[0]) == 3:
                    valid_move = True

            else:
                pos_row = 19
                pos_col = 19
                move = self.try_block_first(pos_row,  -2, random_big_block -2)
                if random_big_block.block_matrix[-1][-1] and len(random_big_block.block_matrix) == 3 and len(random_big_block.block_matrix[0]) == 3:
                    valid_move = True

        self.player_insert(random_block_idx, move.row, move.col)
        self.corners += move.new_corners
        self.pop_corners()
        print(self.corners)
    
   

    

    def get_random_block(self, size = None):
        remaining_idx = self.get_remaining_block_idx()
        if not size:
            random.shuffle(remaining_idx)
            rand_idx = remaining_idx[0]
            return rand_idx, self.blocks[rand_idx]
        elif size == "small":
            small_idx = remaining_idx[:len(remaining_idx)//2 +1]
            random.shuffle(small_idx)
            rand_idx = small_idx[0]
            return rand_idx, self.blocks[rand_idx]
        elif size == "big":
            big_idx = remaining_idx[len(remaining_idx)//2:]
            random.shuffle(big_idx)
            rand_idx = big_idx[0]
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
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[0][j]:
                            if self.board.is_move_valid(row_to_fullfile - j, col_to_fullfile, block):
                                move = self.try_block(row_to_fullfile - j, col_to_fullfile, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                
                                    

                    for j in range(1, len(block.block_matrix)):
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
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[-1][j]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - j, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                
                                    
                
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[-j-1][0]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 10,5)**2 + (col_to_fullfile - 10,5)**2 +(row_to_fullfile + len(block.block_matrix) - 10,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 10,5)**2
                                

                            
                element = block.block_matrix[0][-1]

                if element:
                    valid = self.board.is_move_valid(row_to_fullfile , col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                    if valid:
                        move = self.try_block(row_to_fullfile , col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                        if move > best_move:
                            best_move = move
                        #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                       
                        
                else:
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[0][-j-1]:
                            if self.board.is_move_valid(row_to_fullfile, col_to_fullfile - len(block.block_matrix[0]) + 1 + j, block):
                                move = self.try_block(row_to_fullfile, col_to_fullfile - len(block.block_matrix[0]) + 1 + j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                   
                
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[j][-1]:
                            if self.board.is_move_valid(row_to_fullfile -j, col_to_fullfile - len(block.block_matrix[0]) + 1, block):
                                move = self.try_block(row_to_fullfile -j, col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                
                            
                
                element = block.block_matrix[-1][-1]

                if element:
                    valid = self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 , col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                    if valid:
                        move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 , col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                        if move > best_move:
                            best_move = move
        
                        #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                        
                     
                else:
                    for j in range(1, len(block.block_matrix[0])):
                        if block.block_matrix[-1][-j-1]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - len(block.block_matrix[0]) + 1 + j, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1, col_to_fullfile - len(block.block_matrix[0]) + 1 + j, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                  
                                    
                
                    for j in range(1, len(block.block_matrix)):
                        if block.block_matrix[-j-1][-1]:
                            if self.board.is_move_valid(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile - len(block.block_matrix[0]) + 1, block):
                                move = self.try_block(row_to_fullfile - len(block.block_matrix) + 1 + j, col_to_fullfile - len(block.block_matrix[0]) + 1, block)
                                if move > best_move:
                                    best_move = move
                                #strength_of_move = -(row_to_fullfile - 9,5)**2 + (col_to_fullfile - 9,5)**2 +(row_to_fullfile + len(block.block_matrix) - 9,5)**2 + (col_to_fullfile + len(block.block_matrix[0])- 9,5)**2
                                
                                
                block.rotate()
            block.reflect()
        

        return best_move



    def get_remaining_block_idx(self):
        return [idx for idx in self.blocks]
    
    def get_best_corner(self):
        self.pop_corners()
        print(f"corner: {self.corners}")
        best_corner = (100, 100)
        for row, col in self.corners:
            if best_corner == (100, 100):
                best_corner = (row, col)
                old_strength = (row-9.5)**2 + (col-9.5)**2
            else:
                strength = (row-9.5)**2 + (col-9.5)**2
                if strength < old_strength:
                    old_strength = strength
                    best_corner = (row, col)
        return best_corner



        

    # inserts a block in a copied board and checks how many new corners it generates
    def try_block_first(self, row: int, col: int, block: Block) -> Move:
        demo_board = deepcopy(self.board)
        demo_board.board_insert(block, row, col)
        new_corners = []
        for row_i in range(row -1, len(block.block_matrix) + row + 1):
            #print(row_i)
            for col_i in range(col -1, len(block.block_matrix[0]) + col + 1):
                #print(col_i)
                if self.is_corner(demo_board, row_i, col_i):
                    if (row_i, col_i) not in self.corners:
                        new_corners.append((row_i, col_i))
        print(len(new_corners))
        return Move(len(new_corners)-1, row, col, new_corners, block)
    
    def try_block(self, row: int, col: int, block: Block) -> Move:
        if self.board.is_move_valid(row, col, block):
            demo_board = deepcopy(self.board)
            demo_board.board_insert(block, row, col)
            new_corners = []
            for row_i in range(row -1, len(block.block_matrix) + row + 1):
                for col_i in range(col -1, len(block.block_matrix[0]) + col + 1):
                    if self.is_corner(demo_board, row_i, col_i):
                        if (row_i, col_i) not in self.corners:
                            new_corners.append((row_i, col_i))
            x = deepcopy(block)
            return Move(len(new_corners)-1, row, col, new_corners, x)
        else:
            return Move(0, 0, 0, [])
    


        
    # pops old corners (which are now invalid)
    def pop_corners(self):
        demoboard = deepcopy(self.board)
        for index, (row, col) in enumerate(self.corners):
            if not self.is_corner(demoboard, row, col):
                self.corners.pop(index)

    # check if the position is a corner (possibility to insert new block)
    def is_corner(self, board: Board, row, col) -> bool:
        corner = False

        if row > 19 or row < 0 or col > 19 or col < 0:
            return False
        
        if board.matrix[row][col]:
            return False
    

        if row != 0:
            if board.matrix[row-1][col] == self.color:
                return False
            if col != 0:
                if board.matrix[row-1][col-1] == self.color:
                    corner = True
            if col != 19:
                if board.matrix[row-1][col+1] == self.color:
                    corner = True

        if row != 19:
            if board.matrix[row+1][col] == self.color:
                return False
            if col != 0:
                if board.matrix[row+1][col-1] == self.color:
                    corner = True
            if col != 19:
                if board.matrix[row+1][col+1] == self.color:
                    corner = True


        if col != 0:
            if board.matrix[row][col-1] == self.color:
                return False
            if row != 19:
                if board.matrix[row+1][col-1] == self.color:
                    corner = True
            if row != 0:
                if board.matrix[row-1][col-1] == self.color:
                    corner = True

        if col != 19:
            if board.matrix[row][col+1] == self.color:
                return False
            if row != 19:
                if board.matrix[row+1][col+1] == self.color:
                    corner = True
            if row != 0:
                if board.matrix[row-1][col+1] == self.color:
                    corner = True

        return corner
        
    def set_block(self):
        best_move = Move(0, 0, 0, [])
        #new_board.show_board()
        best_row, best_col = self.get_best_corner()

        best_idx= 0
        counter = 0


        while counter < 8:

            idx, block = self.get_random_block("big")
            #idx, block = 18, self.blocks[18]
            new_best_move = self.find_block_position(best_row, best_col, block)
            if best_move == Move(0, 0, 0, []):
                best_move = new_best_move
                best_idx = idx
            else:
                if new_best_move > best_move:
                    best_move = new_best_move
                    best_idx = idx
            counter += 1

        print ("end1")
        print(str(best_move))
        print(counter)
        print(best_move == Move(0, 0, 0, []))
        while best_move == Move(0, 0, 0, []) and counter < 30:
            print("start2")
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

        self.player_insert(best_idx, best_move.row, best_move.col, best_move.block)
        self.corners += best_move.new_corners
        #self.pop_corners()
        print(self.corners)

        

    def get_random_corner(self):
        copied_corners = deepcopy(self.corners)
        random.shuffle(copied_corners)
        return copied_corners[0]

#new_board = Board()
#ai = AIPlayer("red", new_board)
#new_board.show_board()
#ai.set_first_block()
#print("\n")
#new_board.show_board()
#print("\n")
#ai.set_block()
#cleanew_board.show_board()





