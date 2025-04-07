import random
import math


class DHParticipant:
    def __init__(self, name, p=None, g=None, private_key=None):
        self.name = name
        self.p = p  # prime modulus
        self.g = g  # generator
        self.private_key = private_key
        self.public_key = None
        self.shared_secret = None

    def generate_private_key(self):
        """Generate random private key if not provided"""
        if self.private_key is None:
            self.private_key = random.randint(2, self.p - 2)
        return self.private_key

    def compute_public_key(self):
        """Compute public key (g^a mod p)"""
        if self.private_key is None:
            self.generate_private_key()
        self.public_key = pow(self.g, self.private_key, self.p)
        return self.public_key

    def compute_shared_secret(self, received_key):
        """Compute shared secret from received public key"""
        self.shared_secret = pow(received_key, self.private_key, self.p)
        return self.shared_secret


def group_key_exchange(participants):
    """Perform multi-party DH key exchange"""
    # Forward direction
    current_value = participants[0].compute_public_key()
    for participant in participants[1:]:
        current_value = pow(current_value, participant.private_key, participant.p)

    forward_value = current_value
    # Reverse direction
    current_value = participants[len(participants) - 1].compute_public_key()
    for participant in reversed(participants[:-1]):
        current_value = pow(current_value, participant.private_key, participant.p)

    # Set shared secret for all participants
    for participant in participants:
        participant.shared_secret = current_value
    return forward_value


if __name__ == "__main__":

    # Example usage with predefined private keys
    p = 23  # Prime modulus
    g = 5  # Generator

    # 2-Party example with specified keys
    alice = DHParticipant("Alice", p, g, private_key=6)
    bob = DHParticipant("Bob", p, g, private_key=15)

    alice.compute_public_key()
    bob.compute_public_key()

    # Exchange public keys
    alice_secret = alice.compute_shared_secret(bob.public_key)
    bob_secret = bob.compute_shared_secret(alice.public_key)

    print(f"2-Party DH with predefined keys:")
    print(f"Alice's secret: {alice_secret}")
    print(f"Bob's secret: {bob_secret}")
    print(f"Secrets match: {alice_secret == bob_secret}")

    # 3-Party example with mixed keys (some predefined, some generated)
    p = 997  # Larger prime for 3-party
    g = 5

    # Charlie will have auto-generated key
    alice = DHParticipant("Alice", p, g, private_key=123)
    bob = DHParticipant("Bob", p, g, private_key=456)
    charlie = DHParticipant("Charlie", p, g, private_key=344)

    # Generate remaining keys
    # charlie.generate_private_key()

    # Compute public keys
    for participant in [alice, bob, charlie]:
        participant.compute_public_key()

    # Perform group exchange
    group_secret = group_key_exchange([alice, bob, charlie])

    print(f"\n3-Party DH with mixed keys:")
    print(f"Alice's secret: {alice.shared_secret}")
    print(f"Bob's secret: {bob.shared_secret}")
    print(f"Charlie's secret: {charlie.shared_secret}")
    print(
        f"All secrets match: {alice.shared_secret == bob.shared_secret == charlie.shared_secret==group_secret}"
    )
