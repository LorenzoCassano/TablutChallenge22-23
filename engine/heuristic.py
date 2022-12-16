import numpy as np

BLOCKED_MOVES = ((0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (4, 0), (5, 0), (4, 1), (8, 3), (8, 4), (8, 5), (7, 4),
                 (4, 7), (3, 8), (4, 8), (5, 8), (4, 4))

BL_MOVES = (
    (0, 0, 0, 1, 3, 4, 5, 4, 8, 8, 8, 7, 4, 3, 4, 5, 4),
    (3, 4, 5, 4, 0, 0, 0, 1, 3, 4, 5, 4, 7 ,8, 8, 8, 4)
)
board_array = np.zeros((9, 9), dtype=np.int8)
blocked_mask = np.zeros((9, 9), dtype=np.int8)
print(board_array[BL_MOVES])
blocked_mask[BL_MOVES] = 1
print(blocked_mask)