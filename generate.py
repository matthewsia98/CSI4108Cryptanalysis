import cipher
import utils
import json
import random


name = input("Enter your name: ").strip()
random.seed(name)


round_keys = [random.getrandbits(16) for _ in range(5)]
# NOTE: must change if changing sbox or permutation
dp = utils.btoi("0000 0000 1101 0000")
ciphertext_pairs = []
for x1 in range(5000):
    x2 = x1 ^ dp

    c1 = cipher.encrypt(x1, round_keys)
    c2 = cipher.encrypt(x2, round_keys)
    ciphertext_pairs.append((c1, c2))

with open(f"{name}.json", "w") as f:
    json.dump(
        {
            "sbox": cipher.sbox.tolist(),
            "permutation": cipher.permutation.tolist(),
            "round_keys": round_keys,
            "ciphertext_pairs": ciphertext_pairs,
        },
        f,
        indent=4,
    )
