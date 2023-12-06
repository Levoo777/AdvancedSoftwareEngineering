try:
    from classes.Block import Block
except:
    from Block import Block

class Board():
    matrix: int

    #@Leon Ams, Sercan Berkpinar, Lukas Buser
    def __init__(self):
        self.matrix = [[None for _ in range(20)] for _ in range(20)]
        
    # @ Lukas Buser, Leon Ams, Levin Bolbas
    def is_move_valid(self, row: int, column: int, block: Block):

            corner = False
            for i in range(len(block.block_matrix)):
                for j in range(len(block.block_matrix[i])):

                    if not block.block_matrix[i][j]: 
                        continue  

                    if row+i < 20 and row+i >= 0 and column+j <20 and column+j>= 0:                # new
                        pass
                    else:
                        return False

                    
                    if self.matrix[row + i][column + j] != None:
                            if block.block_matrix[i][j]:
                                return False

                    if row+i > 0:
                        if self.matrix[row-1+i][column+j] == block.color:
                            return False
                        if column+j > 0:
                            if self.matrix[row-1+i][column-1+j] == block.color:
                                corner = True
                        if column+j < 19:
                            if self.matrix[row-1+i][column+1+j] == block.color:
                                corner = True
                             
                             
                    if row+i < 19:
                        if self.matrix[row+1+i][column+j] == block.color:
                            return False
                        if column+j > 0:
                            if self.matrix[row+1+i][column-1+j] == block.color:
                                corner = True
                        if column+j < 19:
                            if self.matrix[row+1+i][column+1+j] == block.color:
                                corner = True
                        
                    if column+j > 0:
                        if self.matrix[row+i][column-1+j] == block.color:
                            return False
                        
                    if column+j < 19:
                        if self.matrix[row+i][column+1+j] == block.color:
                            return False       
            
            return corner

            # for i in range(len(block)):
            #     for j in range(len(block[i])):
            #                 self.matrix[row + i][column + j] = block[i][j]
            
    
    #@Leon Ams
    def board_insert(self, block: Block, row: int, col: int):
        for idx_row, x_row in enumerate(block.block_matrix):
            for idx_col, val in enumerate(x_row):
                if not self.matrix[row + idx_row][col + idx_col]:
                    print(f"INSERT {row + idx_row}, {col + idx_col}, {block.block_matrix}")
                    self.matrix[row + idx_row][col + idx_col] = val  

    #@Leon Ams, Sercan Berkpinar
    def show_board(self):
        for x_row in self.matrix:
            row = f""
            for y in x_row:
                cell_value = str(y) if y is not None else ""
                if len(cell_value) < 5:
                    cell_value = cell_value.ljust(5)
                row += f"  {cell_value} |"
            print(row)
            print("_________" * 20 + "\n")






field = Board()
