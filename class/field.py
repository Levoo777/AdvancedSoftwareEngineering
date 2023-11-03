#@Leon Ams, Sercan Berkpinar, Lukas Buser
class Field:
    matrix: int

    def __init__(self):
        self.matrix = [[None for _ in range(20)] for _ in range(20)]

    def insert(self, block, position):
        self.matrix[position[0]][position[1]] = 'yellow'
