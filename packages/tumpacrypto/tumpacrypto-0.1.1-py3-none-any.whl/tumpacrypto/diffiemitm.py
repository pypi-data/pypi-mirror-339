class DHParticipant:
    def __init__(self, name, p, g, private_key):
        self.name = name
        self.p = p
        self.g = g
        self.private_key = private_key
        self.public_key = pow(g, private_key, p)
        
    def get_shared_secret(self, received_public):
        return pow(received_public, self.private_key, self.p)

class MITMAttacker:
    def __init__(self, p, g, private_key1, private_key2):
        self.p = p
        self.g = g
        self.k1 = private_key1
        self.k2 = private_key2
        self.fake_public1 = pow(g, private_key1, p)
        self.fake_public2 = pow(g, private_key2, p)
        
    def intercept_keys(self, alice_pub, bob_pub):
        print("\nDarth intercepts the public keys:")
        print(f"Original Alice's public key: {alice_pub}")
        print(f"Original Bob's public key: {bob_pub}")
        
        print("\nDarth replaces public keys:")
        print(f"Sends fake public {self.fake_public2} to Alice")
        print(f"Sends fake public {self.fake_public1} to Bob")
        return self.fake_public2, self.fake_public1

if __name__ == "__main__":
    # Public parameters
    p = 23
    g = 5
    
    # Create legitimate participants
    alice = DHParticipant("Alice", p, g, 6)
    bob = DHParticipant("Bob", p, g, 15)
    
    # Create attacker
    darth = MITMAttacker(p, g, 10, 12)
    
    print(f"Alice's public key: {alice.public_key}")
    print(f"Bob's public key: {bob.public_key}")
    
    # MITM interception
    fake_for_alice, fake_for_bob = darth.intercept_keys(alice.public_key, bob.public_key)
    
    # Shared secrets calculation
    alice_secret = alice.get_shared_secret(fake_for_alice)
    bob_secret = bob.get_shared_secret(fake_for_bob)
    
    # Attacker's secrets
    darth_secret_alice = pow(alice.public_key, darth.k2, p)
    darth_secret_bob = pow(bob.public_key, darth.k1, p)
    
    print("\nShared Secrets:")
    print(f"Alice's secret: {alice_secret}")
    print(f"Bob's secret: {bob_secret}")
    print(f"Darth's secret with Alice: {darth_secret_alice}")
    print(f"Darth's secret with Bob: {darth_secret_bob}")


