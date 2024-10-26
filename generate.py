import cipher
import utils
import json
import random
import numpy as np


name = input("Enter your name: ").strip()
random.seed(int(input("Enter random seed: ").strip()))


sbox = np.array([14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7])
permutation = np.array([0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15])


round_keys = [random.getrandbits(16) for _ in range(5)]
dp = utils.btoi("0000 1011 0000 0000")
ciphertext_pairs = []
for x1 in range(5000):
    x2 = x1 ^ dp

    c1 = cipher.encrypt(x1, sbox, permutation, round_keys)
    c2 = cipher.encrypt(x2, sbox, permutation, round_keys)
    ciphertext_pairs.append((c1, c2))

with open(f"{name}.json", "w") as f:
    json.dump(
        {
            "sbox": sbox.tolist(),
            "permutation": permutation.tolist(),
            "round_keys": round_keys,
            "ciphertext_pairs": ciphertext_pairs,
        },
        f,
        indent=4,
    )
