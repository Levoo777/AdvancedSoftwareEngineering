

board = [[None for _ in range(8)] for _ in range(8)]
block = [[True, True, True], [False, True, False]]

def insert(block, position):
    for i in range(len(block)):
        for j in range(len(block[0])):
            board[position[0]+i][position[1]+j] = block[i][j]

insert(block, [0,2])

print(board)