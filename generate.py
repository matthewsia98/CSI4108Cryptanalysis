import cipher
import utils
import json
import random


name = input("Enter your name: ").strip().lower()
random.seed(name)


round_keys = [random.getrandbits(16) for _ in range(5)]
# NOTE: must change if changing sbox or permutation
dp = utils.btoi("0000 0000 1101 0000")


num_ciphertext_pairs = 5000
match name:
    case "matt":
        gen = range(0, num_ciphertext_pairs, 1)
    case "lilia":
        gen = range(2**16 - 1, 2**16 - num_ciphertext_pairs - 1, -1)
    case _:
        raise ValueError("unrecognized name")

ciphertext_pairs = []
for x1 in gen:
    x2 = x1 ^ dp

    c1 = cipher.encrypt(x1, round_keys)
    c2 = cipher.encrypt(x2, round_keys)
    ciphertext_pairs.append((c1, c2))

filename = f"{name}.json"
with open(filename, "w") as f:
    json.dump(
        {
            "sbox": cipher.sbox.tolist(),
            "permutation": cipher.permutation.tolist(),
            "ciphertext_pairs": ciphertext_pairs,
        },
        f,
        indent=4,
    )
print(f"Results written to {filename}")

filename = f"{name}-keys.json"
with open(filename, "w") as f:
    json.dump(
        {
            "round_keys": round_keys,
        },
        f,
    )
print(f"Round keys written to {filename}")


print()
