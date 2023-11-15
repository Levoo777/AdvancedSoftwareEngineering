#@Leon Ams, Sercan Berkpinar, Lukas Buser
# import block


class Board():
    matrix: int

    def __init__(self):
        self.matrix = [[None for _ in range(20)] for _ in range(20)]
        


    # @ Levin Bolbas
    def insert_block(self, row: int, column: int, block):


            for i in range(len(block)):
                for j in range(len(block[i])):
                    
                    if self.matrix[row + i][column + j] != None:
                            return "Move not possible!"

            for i in range(len(block)):
                for j in range(len(block[i])):
                            self.matrix[row + i][column + j] = block[i][j]
            
            return "Movie is possible!"
                    





field = Board()
