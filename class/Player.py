class Player():

    color: str
    blocks: dict

    # @ Lukas Buser, Levin Bolbas
    def __init__(self, color):
        self.color = color
        self.blocks = {1: [[True]], 2: [[True,True]], 3: [[True,True],[False,True]], 4: [[True,True,True]]}


    # @ Lukas Buser, Levin Bolbas
    def player_insert(self, block, position):
        self.board_insert(block, position)
        self.blocks.pop(block)

    


