import utils
import random
import numpy as np


random.seed(2)
sbox = np.array(random.sample(range(16), 16))
permutation = np.array([0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15])


def encrypt(p: int, round_keys: list[int]) -> int:
    num_rounds = len(round_keys)

    # w represents unkeyed input to sbox
    w = p
    for r in range(num_rounds - 2):
        u = w ^ round_keys[r]
        u_bits = utils.itob(u).zfill(16)
        assert len(u_bits) == 16

        u_blocks = utils.split_bin(u_bits)
        assert all(len(b) == 4 for b in u_blocks)

        v_blocks = [utils.itob(sbox[utils.btoi(b)]).zfill(4) for b in u_blocks]
        assert all(len(v) == 4 for v in v_blocks)

        v_bits = "".join(v_blocks)
        assert len(v_bits) == 16

        w_bits = "".join([v_bits[i] for i in np.argsort(permutation)])
        assert len(w_bits) == 16

        for i in range(16):
            assert v_bits[i] == w_bits[permutation[i]]

        w = utils.btoi(w_bits)

    u = w ^ round_keys[-2]
    u_bits = utils.itob(u).zfill(16)
    assert len(u_bits) == 16

    u_blocks = utils.split_bin(u_bits)
    assert all(len(b) == 4 for b in u_blocks)

    v_blocks = [utils.itob(sbox[utils.btoi(b)]).zfill(4) for b in u_blocks]
    assert all(len(v) == 4 for v in v_blocks)

    v_bits = "".join(v_blocks)
    assert len(v_bits) == 16

    v = utils.btoi(v_bits)

    c = v ^ round_keys[-1]
    return c
