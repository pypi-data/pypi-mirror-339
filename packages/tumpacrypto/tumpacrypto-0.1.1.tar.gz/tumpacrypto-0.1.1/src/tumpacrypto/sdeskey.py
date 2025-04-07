class SDESKeyGenerator:
    def __init__(self, key):
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.key = [int(bit) for bit in key]
        self.k1, self.k2 = self.generate_subkeys()

    def permutate(self, bits, permutation):
        """Apply permutation to bit array"""
        return [bits[i - 1] for i in permutation]

    def split_key(self, key):
        """Split 10-bit key into two 5-bit halves"""
        return key[:5], key[5:]

    def left_shift(self, half, n):
        """Perform circular left shift on half-key"""
        return half[n:] + half[:n]

    def generate_subkeys(self):
        """Generate subkeys K1 and K2"""
        # Initial permutation
        p10_key = self.permutate(self.key, self.P10)

        # Split and shift
        left, right = self.split_key(p10_key)
        ls1_left = self.left_shift(left, 1)
        ls1_right = self.left_shift(right, 1)

        # Create K1
        combined_k1 = ls1_left + ls1_right
        k1 = self.permutate(combined_k1, self.P8)

        # Second shift for K2
        ls2_left = self.left_shift(ls1_left, 2)
        ls2_right = self.left_shift(ls1_right, 2)

        # Create K2
        combined_k2 = ls2_left + ls2_right
        k2 = self.permutate(combined_k2, self.P8)

        return k1, k2

    def get_keys(self):
        """Return subkeys as binary strings"""
        k1_str = "".join(map(str, self.k1))
        k2_str = "".join(map(str, self.k2))
        return k1_str, k2_str


if __name__ == "__main__":

    key = "0010010111"
    generator = SDESKeyGenerator(key)
    k1, k2 = generator.get_keys()

    print(f"Original Key: {key}")
    print(f"Subkey K1:    {k1}")
    print(f"Subkey K2:    {k2}")
