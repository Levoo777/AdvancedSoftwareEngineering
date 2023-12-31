try:
    from classes.Board import Board
    from classes.Block import Block
except:
    from Board import Board
    from Block import Block

class Player():

    color: str
    blocks: dict[int, Block]
    board: Board

    # @ Lukas Buser, Levin Bolbas
    def __init__(self, color, board= None, blocks = None):
        self.color = color
        self.board = board
        if not blocks:
            self.blocks = Block.generate_block_set(color)
        
    # @ Lukas Buser, Levin Bolbas
    def player_insert(self, block_idx: int, row: int, col: int, block = None):
        if not block:
            self.board.board_insert(self.blocks[block_idx], row, col)
        else:
            self.board.board_insert(block, row, col)
        self.blocks.pop(block_idx)

    #@Leon Ams
    def show_remaining_blocks(self):
        for idx, block in self.blocks.items():
            block.show_block()
            
    #@Lukas Buser
    def get_block(self, index):
        return self.blocks[index]

    def calc_points(self):
        points = 89
        for block in self.blocks:
            for idx1, row in enumerate(self.blocks[block].block_matrix):
                for idx2, y in enumerate(row):
                    if self.blocks[block].block_matrix[idx1][idx2]:
                        points -= 1
        return points        
