

board = [[None for _ in range(8)] for _ in range(8)]
block = [[True, True, True], [False, True, False]]

def insert(block, position):
    for i in range(len(block)):
        for j in range(len(block[0])):
            board[position[0]+i][position[1]+j] = block[i][j]

insert(block, [0,2])

print(board)
, 18: [[True, True, None], [None, True, True]]}


BLOCKS_MATRIX = {1: [[True]], 2: [[True,True]], 3: [[True,True],[None,True]], 4: [[True,True,True]], 5: [[True,True,True, True]], 6: [[None, None, True],[True,True,True]], 7: [[True, True, None], [None, True, True]], 8: [[True, True], [True, True]], 9: [[None, True, None], [True, True, True]], 10: [[None, True, True], [True, True, None], [None, True, None]], 11: [[True, True, True, True, True]], 12: [[True, True, True, True], [None, None, None, True]], 13: [[True, True, True, None], [None, None, True, True]], 14: [[True, True, True], [None, True, True]], 15: [[True, True, True], [None, True, None], [None, True, None]], 16: [[True, True, True], [True, None, True]], 17: [[True, True, True], [None, None, True], [None, None, True]], 18: [[None, None, True], [None, True, True], [True, True, None]], 19: [[None, True, None], [True, True, True], [None, True, None]], 20: [[True, True, True, True], [None, None, True, None]], 21: [[True, True, None], [None, True, None], [None, True, True]]}



