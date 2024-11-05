
import json

with open('matt-ciphertexts.json', 'r') as file:
    data = json.load(file)

ciphertext_pairs = data["ciphertext_pairs"]

results = {}

target_difference = int("0000000000110011", 2)

subkey_probabilities = [0] * 256

#define s-box and its inverse
sbox = [1, 15, 14, 5, 2, 10, 4, 9, 3, 8, 0, 6, 13, 7, 11, 12]
inverse_sbox = {value: index for index, value in enumerate(sbox)}

#helper function to split value into 4 bit blocks
def split_into_4bit_blocks(value):
    return [(value >> (4 * i)) & 0xF for i in reversed(range(4))]

def apply_inverse_sbox_and_reassemble(blocks):
    transformed_blocks = [inverse_sbox[block] for block in blocks]
    result = (transformed_blocks[0] << 12) | (transformed_blocks[1] << 8) | (transformed_blocks[2] << 4) | transformed_blocks[3]
    return result

for subkey_8bit in range(256):
    full_key = int(f"00000000{subkey_8bit:08b}", 2)
    
    xor_results = []

    for c1, c2 in ciphertext_pairs:
        v1 = c1 ^ full_key
        v2 = c2 ^ full_key

        v1_blocks = split_into_4bit_blocks(v1)
        v2_blocks = split_into_4bit_blocks(v2)

        u1 = apply_inverse_sbox_and_reassemble(v1_blocks)
        u2 = apply_inverse_sbox_and_reassemble(v2_blocks)

        du = u1 ^ u2

        if du == target_difference:
          subkey_probabilities[subkey_8bit] += 1

    subkey_probabilities[subkey_8bit] /= 5000


sorted_subkeys = sorted(enumerate(subkey_probabilities), key=lambda x: x[1], reverse=True)

with open("lilia-attack-matthew.txt", "w") as file:
    for subkey, probability in sorted_subkeys:
        file.write(f"Subkey {subkey:02X} : {probability:.4f}\n")
