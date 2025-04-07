import math


class RSA_Signer:
    def __init__(self, p, q, e=65537):
        """
        Initialize RSA signer with prime numbers p and q
        """
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = e
        self.d = self._modular_inverse(self.e, self.phi)  # private key

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
        """Return public key (e, n)"""
        return (self.e, self.n)

    def sign(self, message):
        """Sign message using private key"""
        if message >= self.n:
            raise ValueError("Message must be smaller than modulus n")
        return pow(message, self.d, self.n)

    @staticmethod
    def verify(signature, message, public_key):
        """Verify signature using public key"""
        e, n = public_key
        decrypted = pow(signature, e, n)
        return decrypted == message

    def sign_text(self, text):
        """Sign text string (character by character)"""
        return [self.sign(ord(char)) for char in text]

    @staticmethod
    def verify_text(signatures, original_text, public_key):
        """Verify text signature"""
        if len(signatures) != len(original_text):
            return False

        for sig, char in zip(signatures, original_text):
            if not RSA_Signer.verify(sig, ord(char), public_key):
                return False
        return True


# Example usage
if __name__ == "__main__":

    p = 61
    q = 53
    e = 24
    # Initialize signer
    alice = RSA_Signer(p, q, e)

    print("Public Key:", alice.get_public_key())

    # Number signing demo
    message = 65
    signature = alice.sign(message)
    is_valid = RSA_Signer.verify(signature, message, alice.get_public_key())
    print(
        f"\nNumber Signing:\nMessage: {message}\nSignature: {signature}\nValid: {is_valid}"
    )

    # Text signing demo
    text = "HELLO"
    signatures = alice.sign_text(text)
    text_valid = RSA_Signer.verify_text(signatures, text, alice.get_public_key())
    print(
        f"\nText Signing:\nOriginal: {text}\nSignatures: {signatures}\nValid: {text_valid}"
    )

    # Test tampering detection
    tampered_text = "HELPO"
    tampered_valid = RSA_Signer.verify_text(
        signatures, tampered_text, alice.get_public_key()
    )
    print(f"\nTampered Text Validation:\nExpected: False\nActual: {tampered_valid}")
