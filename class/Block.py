from copy import deepcopy

BLOCKS_MATRIX = {1: [[True]], 2: [[True,True]], 3: [[True,True],[None,True]], 4: [[True,True,True]], 5: [[True,True,True, True]], 6: [[None, None, True],[True,True,True]], 7: [[True, True, None], [None, True, True]]}

class Block():
    color: str
    block_matrix: list[list[None, str]]

    #@Leon Ams, Sercan Berkpinar, Lukas Buser
    def __init__(self, matrix: list[list[bool]], color):
        self.color = color
        self.block_matrix = matrix
        self.color_matrix()

    #@Leon Ams, Sercan Berkpinar, Lukas Buser
    def rotate(self):
        len_rows, len_cols = len(self.block_matrix), len(self.block_matrix[0])
        rotated_matrix = [[False] * len_rows for _ in range(len_cols)]
        for i in range(len_rows):
            for j in range(len_cols):
                rotated_matrix[j][len_rows - 1 - i] = self.block_matrix[i][j]
        self.block_matrix = rotated_matrix

    #@Leon Ams, Sercan Berkpinar, Lukas Buser
    def reflect(self):
        self.block_matrix = [row[::-1] for row in self.block_matrix]
    
    #@Leon Ams
    def color_matrix(self):
        for idx_row, x_row in enumerate(self.block_matrix):
            for idx_col, val in enumerate(x_row):
                if val:
                    self.block_matrix[idx_row][idx_col] = self.color
    
    #@Leon Ams, Sercan Berkpinar
    def show_block(self):
        for row in self.block_matrix:
            row_str = ""
            for y in row:
                cell_value = str(y) if y else ""
                if len(cell_value) < 5:
                    cell_value = cell_value.ljust(5)
                row_str += f"  {cell_value} |"
            print("_" * len(row_str) + "\n")
            print(row_str)
        print("_" * len(row_str) + "\n")

    #@Leon Ams  - generates full dict of blocks
    @staticmethod
    def generate_block_set(color: str, blocks_set = BLOCKS_MATRIX):
        blocks = {}
        for idx, matrix in blocks_set.items():
            blocks[idx] = deepcopy(Block(matrix, color))
        return blocks