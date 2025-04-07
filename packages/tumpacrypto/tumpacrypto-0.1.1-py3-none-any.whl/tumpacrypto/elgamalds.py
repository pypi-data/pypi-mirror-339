import random
import math


class ElGamalDS:
    def __init__(self, p, g, private_key=None):
        """
        Initialize ElGamal signer with prime modulus (p), generator (g),
        and optional private key
        """
        self.p = p
        self.g = g
        self.private_key = (
            private_key if private_key is not None else self._generate_private_key()
        )
        self.y = pow(g, self.private_key, p)  # Public key component

    def _generate_private_key(self):
        """Generate random private key (1 < x < p-1)"""
        return random.randint(2, self.p - 2)

    def _generate_ephemeral_key(self):
        """Generate random k coprime with p-1"""
        while True:
            k = random.randint(2, self.p - 2)
            if math.gcd(k, self.p - 1) == 1:
                return k

    def _modular_inverse(self, a, m):
        """Find modular inverse using extended Euclidean algorithm"""
        g, x, y = self._extended_gcd(a, m)
        if g != 1:
            return None
        return x % m

    def _extended_gcd(self, a, b):
        """Extended Euclidean Algorithm"""
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self._extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def get_public_key(self):
        """Return public key tuple (p, g, y)"""
        return (self.p, self.g, self.y)

    def sign(self, message):
        """Sign a message (integer)"""
        k = self._generate_ephemeral_key()
        r = pow(self.g, k, self.p)
        k_inv = self._modular_inverse(k, self.p - 1)
        s = ((message - self.private_key * r) * k_inv) % (self.p - 1)
        return (r, s)

    @staticmethod
    def verify(signature, message, public_key):
        """Verify signature against message"""
        p, g, y = public_key
        r, s = signature

        # Check basic constraints
        if not (0 < r < p and 0 < s < p - 1):
            return False

        # Compute both sides of verification equation
        left = pow(g, message, p)  # v1
        right_part1 = pow(y, r, p)
        right_part2 = pow(r, s, p)
        right = (right_part1 * right_part2) % p

        return left == right  # v1==v2

    def sign_text(self, text):
        """Sign text string (character by character)"""
        return [self.sign(ord(char)) for char in text]

    @staticmethod
    def verify_text(signatures, original_text, public_key):
        """Verify text signature"""
        if len(signatures) != len(original_text):
            return False

        for sig, char in zip(signatures, original_text):
            if not ElGamalDS.verify(sig, ord(char), public_key):
                return False
        return True


# Example usage
if __name__ == "__main__":
    # Public parameters (small values for demonstration)
    p = 23  # Prime modulus
    g = 5  # Generator

    # Initialize signer with known private key
    alice = ElGamalDS(p, g, private_key=6)

    # Get public key
    public_key = alice.get_public_key()
    print("Public Key (p, g, y):", public_key)

    # Number signature demo
    message = 10
    signature = alice.sign(message)
    is_valid = ElGamalDS.verify(signature, message, public_key)
    print(
        f"\nNumber Signature:\nMessage: {message}\nSignature: {signature}\nValid: {is_valid}"
    )

    # Text signature demo
    text = "HELLO"
    signatures = alice.sign_text(text)
    text_valid = ElGamalDS.verify_text(signatures, text, public_key)
    print(
        f"\nText Signature:\nOriginal: {text}\nSignatures: {signatures}\nValid: {text_valid}"
    )

    # Tampering test
    tampered_text = "HELPO"
    tampered_valid = ElGamalDS.verify_text(signatures, tampered_text, public_key)
    print(f"\nTampered Text Validation:\nExpected: False\nActual: {tampered_valid}")
