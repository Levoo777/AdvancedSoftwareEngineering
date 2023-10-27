#@Leon Ams, Sercan Berkpinar, Lukas Buser
block_dict = {1: [[True]], 2: [[True,True]], 3: [[True,True],[False,True]], 4: [[True,True,True]]}

class block:
    color: str
    block_matrix: int

    def __init__(self, block_index, color):
        self.block_matrix = block_dict[block_index]
        self.color = color

    def rotate(self):
        len_rows, len_cols = len(self.block_matrix), len(self.block_matrix[0])
        rotated_matrix = [[False] * len_rows for _ in range(len_cols)]
        for i in range(len_rows):
            for j in range(len_cols):
                rotated_matrix[j][len_rows - 1 - i] = self.block_matrix[i][j]
        self.block_matrix = rotated_matrix

    def reflect(self):
        self.block_matrix = [row[::-1] for row in self.block_matrix]