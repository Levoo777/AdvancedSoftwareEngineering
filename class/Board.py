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
            
            return False
                    





field = Board()
