import cipher
import numpy as np


print("=====")
print("S-Box")
print("=====")
print(cipher.sbox)


# Building difference distribution table
diff_table = np.zeros((16, 16), dtype=int)
for x1 in range(16):
    for dx in range(16):
        x2 = x1 ^ dx
        y1 = cipher.sbox[x1]
        y2 = cipher.sbox[x2]
        dy = y1 ^ y2
        diff_table[dx, dy] += 1
print("=============================")
print("Difference Distribution Table")
print("=============================")
print(diff_table)

# Finding max entries in the diff_table
topn = 10
flat_diff_table = diff_table.flatten()
_max_idxs = np.argpartition(flat_diff_table, -topn - 1)[-topn - 1 : -1]
_max_idxs = _max_idxs[np.argsort(-flat_diff_table[_max_idxs])]
max_idxs = np.unravel_index(_max_idxs, diff_table.shape)

diff_pairs = np.column_stack(max_idxs)
diff_counts = diff_table[max_idxs]
print("=======================")
print(f"Top {topn} difference pairs")
print("=======================")
for idx, count in zip(diff_pairs, diff_counts):
    print(
        f"∆X = {idx[0]:2d} ({idx[0]:X}) ⟶ ∆Y = {idx[1]:2d} ({idx[1]:X}), p = {count}/16 ({count/16})"
    )
