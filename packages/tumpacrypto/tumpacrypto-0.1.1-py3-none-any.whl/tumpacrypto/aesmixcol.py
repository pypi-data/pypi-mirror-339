
class AESMixColumns:
    """AES Mix Columns transformation class"""
    def __init__(self):
        self.fixed_matrix = [
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03],
            [0x03, 0x01, 0x01, 0x02]
        ]

    def gf_multiply(self, a, b):
        """Galois Field (256) multiplication for AES Mix Columns"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit = a & 0x80
            a <<= 1
            if hi_bit:
                a ^= 0x1b  # AES irreducible polynomial
            b >>= 1
        return p & 0xFF

    def mix_columns(self,state_array):
        """Perform AES Mix Columns transformation"""
        result = [[0 for _ in range(4)] for _ in range(4)]
        
        for i in range(4):
            for j in range(4):
                sum = 0
                for k in range(4):
                    sum ^= self.gf_multiply(self.fixed_matrix[i][k], state_array[k][j])
                result[i][j] = sum
        return result
    
if __name__ == '__main__':
    

    state_array = [
        [0x44, 0xD6, 0x6B, 0x97],
        [0x4D, 0x7E, 0x0C, 0x1F],
        [0x7D, 0x60, 0xA1, 0x9E],
        [0x8A, 0x5C, 0x3C, 0x3D]
    ]

    # Perform transformation
    aes=AESMixColumns()
    resultant_matrix = aes.mix_columns(state_array)

    # Display results
    print("Original State:")
    for row in state_array:
        print(' '.join(f"{x:02X}" for x in row))

    print("\nResultant Matrix:")
    for row in resultant_matrix:
        print(' '.join(f"{x:02X}" for x in row))