## 📄 `minisecret.py`

import os
import json
import base64
import ctypes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class MiniSecret:
    def __init__(self, secrets_file: str = "secrets.enc.json", env_key_var: str = "MINISECRET_KEY"):
        self.secrets_file = secrets_file
        self.env_key_var = env_key_var
        self._key = self._derive_key()

    def _derive_key(self) -> bytes:
        key_material = os.environ.get(self.env_key_var)
        if not key_material:
            raise ValueError(f"Environment variable '{self.env_key_var}' is not set.")
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key_material.encode())
        return digest.finalize()

    def _encrypt(self, data: dict) -> bytes:
        aesgcm = AESGCM(self._key)
        nonce = os.urandom(12)
        plaintext = json.dumps(data).encode()
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return base64.b64encode(nonce + ciphertext)

    def _decrypt(self, data: bytes) -> dict:
        raw = base64.b64decode(data)
        nonce = raw[:12]
        ciphertext = raw[12:]
        aesgcm = AESGCM(self._key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext)

    def _load_secrets(self) -> dict:
        if not os.path.exists(self.secrets_file):
            return {}
        with open(self.secrets_file, "rb") as f:
            return self._decrypt(f.read())

    def _save_secrets(self, secrets: dict):
        with open(self.secrets_file, "wb") as f:
            f.write(self._encrypt(secrets))

    def get(self, key: str) -> str:
        return self._load_secrets().get(key)

    def secure_get(self, key: str) -> str:
        """Get a secret and securely clear it from memory after use."""
        secrets = self._load_secrets()
        value = secrets.get(key)

        if value is None:
            return None

        b = bytearray(value, encoding='utf-8')
        try:
            return_value = b.decode()
        finally:
            for i in range(len(b)):
                b[i] = 0
            del b
            del value

        return return_value

    def put(self, key: str, value: str):
        secrets = self._load_secrets()
        secrets[key] = value
        self._save_secrets(secrets)

    def list_keys(self):
        return list(self._load_secrets().keys())

# CLI interface
if __name__ == "__main__":
    import sys

    ms = MiniSecret()

    def print_usage():
        print("Usage:")
        print("  python minisecret.py put <key> <value>")
        print("  python minisecret.py get <key> [--secure]")
        print("  python minisecret.py list")

    if len(sys.argv) == 4 and sys.argv[1] == "put":
        ms.put(sys.argv[2], sys.argv[3])
        print(f"✅ Stored secret: '{sys.argv[2]}'")

    elif len(sys.argv) >= 3 and sys.argv[1] == "get":
        key = sys.argv[2]
        use_secure = "--secure" in sys.argv
        value = ms.secure_get(key) if use_secure else ms.get(key)
        if value is None:
            print(f"❌ Secret '{key}' not found.")
        else:
            print(value)

    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        keys = ms.list_keys()
        print("🔐 Stored keys:", keys)

    else:
        print_usage()