# multienc

A refined hybrid encryption/decryption library for secure data transmission.

## Installation

```bash
pip install multienc
```

## Usage

```python
from multienc.crypto import RSAKeyManager, AESCipher, MultiEncrypter

# Configuration
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"
PRIVATE_KEY_PASSWORD = b"secure-password"  # Replace with a secure password
CLIENT_PUBLIC_KEY_FOR_AES = "clientpubkey1234"  # Must match the client's key
UID = "user123"  # Unique user identifier

# Initialize the key manager (generates keys if they don't exist)
rsa_key_manager = RSAKeyManager(PRIVATE_KEY_PATH, PUBLIC_KEY_PATH, PRIVATE_KEY_PASSWORD)

# Initialize the AES cipher
aes_cipher = AESCipher(CLIENT_PUBLIC_KEY_FOR_AES)

# Initialize the multi-encrypter
multi_encrypter = MultiEncrypter(rsa_key_manager, aes_cipher)

# Encryption 
data = {"message": "This is a secret message!"}
encrypted_payload = multi_encrypter.encrypt_refined_hybrid(data, UID)
print("Encrypted payload:", encrypted_payload)

# Decryption 
# (Assume you've received the encrypted_payload from the client)
decrypted_data = multi_encrypter.decrypt_refined_hybrid(encrypted_payload, UID)
print("Decrypted data:", decrypted_data)
```

**Important:**

*   Replace `"secure-password"` with a strong, randomly generated password for your RSA private key.
*   Ensure the `CLIENT_PUBLIC_KEY_FOR_AES` matches the value used by the client for AES key derivation.
*   Handle RSA key generation and storage securely.  Do not hardcode the private key password in production.
*   The `UID` should be unique per user or session.