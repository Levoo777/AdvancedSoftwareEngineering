from Block import Block

class Board():
    matrix: int

    #@Leon Ams, Sercan Berkpinar, Lukas Buser
    def __init__(self):
        self.matrix = [[None for _ in range(20)] for _ in range(20)]
        
    # @ Levin Bolbas
    def is_move_valid(self, row: int, column: int, block):


            for i in range(len(block)):
                for j in range(len(block[i])):
                    
                    if self.matrix[row + i][column + j] != None:
                            return False

            # for i in range(len(block)):
            #     for j in range(len(block[i])):
            #                 self.matrix[row + i][column + j] = block[i][j]
            
            return True
    
    #@Leon Ams
    def board_insert(self, block: Block, row: int, col: int):
        for idx_row, x_row in enumerate(block.block_matrix):
            for idx_col, val in enumerate(x_row):
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
