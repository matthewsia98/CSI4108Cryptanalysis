import utils
import json
import numpy as np


victim = input("Enter victim's name: ").strip()
with open(f"{victim}-ciphertexts.json", "r") as f:
    data = json.load(f)

sbox = np.array(data.get("sbox"))

# NOTE: must change if changing sbox or permutation
target_du = utils.btoi("0000 0000 0011 0011")
du_counts = np.zeros(256, dtype=int)
for c1, c2 in data.get("ciphertext_pairs"):
    dc = c1 ^ c2
    dc_bits = utils.itob(dc).zfill(16)
    # NOTE: might need to change depending on permutation
    if dc_bits[0:4] != "0000" or dc_bits[4:8] != "0000":
        continue

    for sk in range(256):
        sk1, sk2 = utils.split_bin(utils.itob(sk).zfill(8))
        # NOTE: might need to change depending on permutation
        k = utils.btoi(f"0000 0000 {sk1} {sk2}")

        v1 = c1 ^ k
        v2 = c2 ^ k

        v1_bits = utils.itob(v1).zfill(16)
        v2_bits = utils.itob(v2).zfill(16)

        v1_blocks = utils.split_bin(v1_bits)
        v2_blocks = utils.split_bin(v2_bits)

        # inverse sbox
        u1_blocks = [
            utils.itob(sbox.tolist().index(utils.btoi(b))).zfill(4) for b in v1_blocks
        ]
        u2_blocks = [
            utils.itob(sbox.tolist().index(utils.btoi(b))).zfill(4) for b in v2_blocks
        ]

        u1_bits = "".join(u1_blocks)
        u2_bits = "".join(u2_blocks)
        assert len(u1_bits) == 16
        assert len(u2_bits) == 16

        u1 = utils.btoi(u1_bits)
        u2 = utils.btoi(u2_bits)

        du = u1 ^ u2
        if du == target_du:
            du_counts[sk] += 1


print("================")
print("∆U Probabilities")
print("================")
for sk in np.argsort(-du_counts):
    sk1, sk2 = utils.split_bin(utils.itob(sk).zfill(8))
    # NOTE: might need to change depending on permutation
    sk_bits = f"xxxx xxxx {sk1} {sk2}"
    print(f"k = {sk_bits}, p = {du_counts[sk]}/5000 ({du_counts[sk] / 5000})")


topn = 10
print("=====================")
print(f"Top {topn} key candidates")
print("=====================")
max_idxs = np.argpartition(du_counts, -topn)[-topn:]
max_idxs = max_idxs[np.argsort(-du_counts[max_idxs])]
for idx in max_idxs:
    sk1, sk2 = utils.split_bin(utils.itob(idx).zfill(8))
    # NOTE: might need to change depending on permutation
    sk_bits = f"xxxx xxxx {sk1} {sk2}"
    print(
        f"k = {sk_bits}, p = {f"{du_counts[idx]}/5000".rjust(9)} ({du_counts[idx] / 5000})"
    )


with open(f"{victim}-keys.json", "r") as f:
    data = json.load(f)
print("==========")
print("Actual Key")
print("==========")
k = data.get("round_keys", [])[-1]
print(f"k = {utils.format_bin(utils.itob(k).zfill(16))}")


print()
