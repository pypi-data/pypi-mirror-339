import random
import math


class ElGamal:
    def __init__(self, p, g, private_key=None):
        """
        Initialize ElGamal with prime modulus (p), generator (g),
        and optional private key
        """
        self.p = p
        self.g = g
        self.private_key = (
            private_key if private_key is not None else self._generate_private_key()
        )
        self.h = pow(self.g, self.private_key, self.p)  # Public key component

    def _generate_private_key(self):
        """Generate random private key (1 < x < p-1)"""
        return random.randint(2, self.p - 2)

    def get_public_key(self):
        """Return public key tuple (p, g, h)"""
        return (self.p, self.g, self.h)

    @staticmethod
    def encrypt(message, public_key):
        """
        Encrypt a message using recipient's public key
        Returns ciphertext tuple (c1, c2)
        """
        p, g, h = public_key
        if message >= p:
            raise ValueError("Message must be smaller than prime modulus")

        # Generate ephemeral key
        k = random.randint(2, p - 2)
        c1 = pow(g, k, p)
        s = pow(h, k, p)  # can do directly in c2 as (pt*h^k)%p
        c2 = (message * s) % p
        return (c1, c2)

    def decrypt(self, ciphertext):
        """Decrypt ciphertext tuple (c1, c2)"""
        c1, c2 = ciphertext
        s = pow(c1, self.private_key, self.p)
        s_inv = pow(s, -1, self.p)  # Modular inverse using Fermat's little theorem
        return (c2 * s_inv) % self.p

    def encrypt_text(self, text, public_key):
        """Encrypt text string (character by character)"""
        return [self.encrypt(ord(char), public_key) for char in text]

    def decrypt_text(self, ciphertexts):
        """Decrypt list of ciphertext tuples to text"""
        return "".join([chr(self.decrypt(c)) for c in ciphertexts])


# Example usage
if __name__ == "__main__":
    # Public parameters (normally large primes, small values for demonstration)
    p = 7457  # Prime modulus
    g = 6  # Generator (primitive root modulo p)

    # Initialize participants
    alice = ElGamal(p, g, private_key=4)  # Private key 4
    bob = ElGamal(p, g)  # Random private key

    # Get public keys
    alice_pub = alice.get_public_key()
    bob_pub = bob.get_public_key()

    # Basic number encryption
    message = 10
    ciphertext = ElGamal.encrypt(message, alice_pub)
    decrypted = alice.decrypt(ciphertext)
    print(
        f"Number Encryption:\nOriginal: {message}\nEncrypted: {ciphertext}\nDecrypted: {decrypted}"
    )

    # Text encryption
    text = "HELLO"
    encrypted_text = bob.encrypt_text(text, alice_pub)
    decrypted_text = alice.decrypt_text(encrypted_text)
    print(
        f"\nText Encryption:\nOriginal: {text}\nEncrypted: {encrypted_text}\nDecrypted: {decrypted_text}"
    )

    # Demonstration of public key components
    print("\nKeys:")
    print(f"Alice's public key: {alice_pub}")
    print(f"Bob's public key: {bob_pub}")
