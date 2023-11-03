#@Leon Ams, Sercan Berkpinar, Lukas Buser
# import block


class Field():
    matrix: int

    def __init__(self):
        self.matrix = [[None for _ in range(20)] for _ in range(20)]


field = Field()

print(field)