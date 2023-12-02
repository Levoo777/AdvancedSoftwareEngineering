import random




BLOCKS_MATRIX = {1: [[True]], 2: [[True,True]], 3: [[True,True],[None,True]], 4: [[True,True,True]], 5: [[True,True,True, True]], 6: [[None, None, True],[True,True,True]], 7: [[True, True, None], [None, True, True]], 8: [[True, True], [True, True]], 9: [[None, True, None], [True, True, True]], 10: [[None, True, True], [True, True, None], [None, True, None]], 11: [[True, True, True, True, True]], 12: [[True, True, True, True], [None, None, None, True]], 13: [[True, True, True, None], [None, None, True, True]], 14: [[True, True, True], [None, True, True]], 15: [[True, True, True], [None, True, None], [None, True, None]], 16: [[True, True, True], [True, None, True]], 17: [[True, True, True], [None, None, True], [None, None, True]], 18: [[None, None, True], [None, True, True], [True, True, None]], 19: [[None, True, None], [True, True, True], [None, True, None]], 20: [[True, True, True, True], [None, None, True, None]], 21: [[True, True, None], [None, True, None], [None, True, True]]}

BLOCKS_MATRIX = {1: [[True]], 2: [[True,True]], 3: [[True,True],[None,True]], 4: [[True,True,True]], 5: [[True,True,True, True]], 6: [[None, None, True],[True,True,True]], 7: [[True, True, None], [None, True, True]], 8: [[True, True], [True, True]], 9: [[None, True, None], [True, True, True]], 10: [[None, True, True], [True, True, None], [None, True, None]], 11: [[True, True, True, True, True]], 12: [[True, True, True, True], [None, None, None, True]], 13: [[True, True, True, None], [None, None, True, True]], 14: [[True, True, True], [None, True, True]], 15: [[True, True, True], [None, True, None], [None, True, None]], 16: [[True, True, True], [True, None, True]], 17: [[True, True, True], [None, None, True], [None, None, True]], 18: [[None, None, True], [None, True, True], [True, True, None]], 19: [[None, True, None], [True, True, True], [None, True, None]], 20: [[True, True, True, True], [None, None, True, None]], 21: [[True, True, None], [None, True, None], [None, True, True]]}

print([index for index in BLOCKS_MATRIX])

print([index for index in BLOCKS_MATRIX])


def get_random_block(x, size = None):
    remaining_idx = [index for index in x]
    if not size:
        random.shuffle(remaining_idx)
        rand_idx = remaining_idx[0]
        return rand_idx, x[rand_idx]
    elif size == "small":
        small_idx = remaining_idx[:len(remaining_idx)//2 +1]
        random.shuffle(small_idx)
        rand_idx = small_idx[0]
        return rand_idx, x[rand_idx]
    elif size == "big":
        big_idx = remaining_idx[len(remaining_idx)//2:]
        random.shuffle(big_idx)
        rand_idx = big_idx[0]
        return rand_idx, x[rand_idx]
    else:
        raise ValueError(f"'{size}' is not a valid size")

for i in range(100):
    if i%2 == 0:
        index, block = get_random_block(BLOCKS_MATRIX, "small")
        BLOCKS_MATRIX.pop(index)
    else:
        index, block = get_random_block(BLOCKS_MATRIX, "big")
        BLOCKS_MATRIX.pop(index)
    print(index)
