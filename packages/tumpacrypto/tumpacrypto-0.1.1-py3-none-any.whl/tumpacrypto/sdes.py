class SDES:
    def __init__(self, key):
        # Permutation tables
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]
        
        # S-Boxes
        self.S0 = [
            [1,0,3,2],
            [3,2,1,0],
            [0,2,1,3],
            [3,1,3,2]
        ]
        self.S1 = [
            [0,1,2,3],
            [2,0,1,3],
            [3,0,1,0],
            [2,1,0,3]
        ]
        
        # Generate subkeys
        self.key = [int(bit) for bit in key]
        self.k1, self.k2 = self._generate_subkeys()
    
    def _generate_subkeys(self):
        """Generate subkeys K1 and K2"""
        # P10 permutation
        p10 = self._permutate(self.key, self.P10)
        
        # Split and shift
        left, right = p10[:5], p10[5:]
        ls1_left = self._left_shift(left, 1)
        ls1_right = self._left_shift(right, 1)
        
        # Create K1
        k1 = self._permutate(ls1_left + ls1_right, self.P8)
        
        # Second shift for K2
        ls2_left = self._left_shift(ls1_left, 2)
        ls2_right = self._left_shift(ls1_right, 2)
        
        # Create K2
        k2 = self._permutate(ls2_left + ls2_right, self.P8)
        
        return k1, k2
    
    def _permutate(self, bits, table):
        """Apply permutation to bit array"""
        return [bits[i-1] for i in table]
    
    def _left_shift(self, bits, n):
        """Circular left shift"""
        return bits[n:] + bits[:n]
    
    def _split(self, bits):
        """Split into two halves"""
        mid = len(bits)//2
        return bits[:mid], bits[mid:]
    
    def _expand(self, bits):
        """Apply EP expansion"""
        return self._permutate(bits, self.EP)
    
    def _substitute(self, bits, s_box):
        """S-Box substitution"""
        row = 2*bits[0] + bits[3]
        col = 2*bits[1] + bits[2]
        return [s_box[row][col] >> 1 & 1, s_box[row][col] & 1]
    
    def _xor(self, a, b):
        """XOR two bit arrays"""
        return [x ^ y for x,y in zip(a,b)]
    
    def _round_function(self, bits, key):
        """Feistel round function"""
        # Expand and XOR
        expanded = self._expand(bits)
        xored = self._xor(expanded, key)
        
        # S-Box substitutions
        left, right = self._split(xored)
        s0 = self._substitute(left, self.S0)
        s1 = self._substitute(right, self.S1)
        
        # P4 permutation
        return self._permutate(s0 + s1, self.P4)
    
    def encrypt(self, plaintext):
        """Encrypt 8-bit plaintext"""
        # Convert to bit array
        bits = [int(bit) for bit in plaintext]
        
        # Initial permutation
        ip = self._permutate(bits, self.IP)
        left, right = self._split(ip)
        
        # Round 1
        f_result = self._round_function(right, self.k1)
        new_right = self._xor(left, f_result)
        
        # Swap and Round 2
        f_result = self._round_function(new_right, self.k2)
        new_left = self._xor(right, f_result)
        
        # Combine and inverse IP
        combined = new_left + new_right
        ciphertext = self._permutate(combined, self.IP_inv)
        
        return ''.join(map(str, ciphertext))

# Example usage
if __name__ == "__main__":
    key = "0010010111"
    plaintext = "10100001"
    
    sdes = SDES(key)
    encrypted = sdes.encrypt(plaintext)
    
    print(f"Key: {key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted}")
