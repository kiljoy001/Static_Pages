import os
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self, key: bytes = None):
        if not key:
            # Try env var first
            env_key = os.environ.get("ENCRYPTION_KEY")
            if env_key:
                self.key = env_key.encode()
            else:
                # Try loading from file
                key_file = "secret.key"
                if os.path.exists(key_file):
                    with open(key_file, "rb") as f:
                        self.key = f.read()
                else:
                    # Generate and save
                    self.key = Fernet.generate_key()
                    with open(key_file, "wb") as f:
                        f.write(self.key)
                    print(f"WARNING: Generated new encryption key and saved to {key_file}.")
        else:
            self.key = key

        self.cipher_suite = Fernet(self.key)

    def encrypt(self, plain_text: str) -> str:
        if not plain_text:
            return ""
        encrypted_text = self.cipher_suite.encrypt(plain_text.encode())
        return encrypted_text.decode()

    def decrypt(self, encrypted_text: str) -> str:
        if not encrypted_text:
            return ""
        try:
            decrypted_text = self.cipher_suite.decrypt(encrypted_text.encode())
            return decrypted_text.decode()
        except Exception as e:
            # If decryption fails (e.g. wrong key or not encrypted), return original text or empty
            # For robustness in dev when mixing plain/encrypted, we might return original if it fails
            # But strictly, we should probably log error.
            print(f"Decryption failed: {e}")
            return encrypted_text
