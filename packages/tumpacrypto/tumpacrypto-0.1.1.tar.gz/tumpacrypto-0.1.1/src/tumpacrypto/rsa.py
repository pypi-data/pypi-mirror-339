import math


class RSA:
    def __init__(self, p, q, e=65537):
        """
        Initialize RSA with prime numbers p and q and public exponent e
        """
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self._choose_public_exponent(e)
        self.d = self._modular_inverse(self.e, self.phi)

    def _choose_public_exponent(self, e):
        """
        Choose public exponent e (usually 65537)
        """
        if math.gcd(e, self.phi) == 1:
            return e

        # choose an exponent in the range of 3 to phi
        for e in range(3, self.phi, 2):
            if math.gcd(e, self.phi) == 1:
                return e
        raise ValueError("Cannot find suitable public exponent")

    def _modular_inverse(self, a, m):
        """
        Find modular inverse using extended Euclidean algorithm
        """
        g, x, y = self._extended_gcd(a, m)
        if g != 1:
            return None
        return x % m

    def _extended_gcd(self, a, b):
        """
        Extended Euclidean Algorithm implementation
        """
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self._extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def get_public_key(self):
        """
        Return public key (e, n)
        """
        return (self.e, self.n)

    def get_private_key(self):
        """
        Return private key (d, n)
        """
        return (self.d, self.n)

    def encrypt(self, message):
        """
        Encrypt message using public key
        """
        e, n = self.get_public_key()
        return pow(message, e, n)

    def decrypt(self, ciphertext):
        """
        Decrypt ciphertext using private key
        """
        d, n = self.get_private_key()
        return pow(ciphertext, d, n)

    def encrypt_text(self, text):

        return [self.encrypt(ord(char)) for char in text]

    def decrypt_text(self, ciphertext):

        return "".join([chr(self.decrypt(c)) for c in ciphertext])


if __name__ == "__main__":
    # Use small primes for demonstration (insecure for real use)
    p = 61
    q = 53
    e = 65537

    rsa = RSA(p, q, e)

    print("Public Key:", rsa.get_public_key())
    print("Private Key:", rsa.get_private_key())

    # Number encryption demo
    message = 65
    encrypted = rsa.encrypt(message)
    decrypted = rsa.decrypt(encrypted)

    print(
        f"\nNumber Encryption:\nOriginal: {message}\nEncrypted: {encrypted}\nDecrypted: {decrypted}"
    )

    # Text encryption demo
    text = "HELLO"
    encrypted_text = rsa.encrypt_text(text)
    decrypted_text = rsa.decrypt_text(encrypted_text)
    print(
        f"\nText Encryption:\nOriginal: {text}\nEncrypted: {encrypted_text}\nDecrypted: {decrypted_text}"
    )
