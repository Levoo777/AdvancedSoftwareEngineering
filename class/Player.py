# @ Lukas Buser, Levin Bolbas
import Board

class Player(Board):

    color: str
    blocks: dict

    def __init__(self, color):
        self.color = color
        self.blocks = {1: [[True]], 2: [[True,True]], 3: [[True,True],[False,True]], 4: [[True,True,True]]}


    def player_insert(self, block, position):
        self.board_insert(block, position)
        self.blocks.pop(block)



