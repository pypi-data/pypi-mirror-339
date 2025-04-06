import json
import base64
import time
import os
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as aes_padding
from cryptography.hazmat.backends import default_backend
import binascii

from .helpers import xor_bytes, reverse_xor_presenz, binary_string_to_bytes
from .errors import RSAKeyError, AESDecryptionError, PayloadError, TimeWindowError, BinaryStringError
from .enums import KeySize, IVSize

class RSAKeyManager:
    def __init__(self, private_key_path="private_key.pem", public_key_path="public_key.pem", private_key_password=b"your-secure-password"):
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        self.private_key_password = private_key_password
        self.private_key = None
        self.public_key = None
        self.load_keys()

    def generate_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
        public_key = private_key.public_key()
        pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=(serialization.BestAvailableEncryption(self.private_key_password) if self.private_key_password else serialization.NoEncryption()))
        with open(self.private_key_path, "wb") as f:
            f.write(pem_private)
        print(f"Generated 4096-bit private key: {self.private_key_path}")
        pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        with open(self.public_key_path, "wb") as f:
            f.write(pem_public)
        print(f"Generated public key: {self.public_key_path}")
        self.private_key = private_key
        self.public_key = public_key
        return private_key, public_key

    def load_keys(self):
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            return self.generate_keys()
        try:
            with open(self.private_key_path, "rb") as f:
                self.private_key = serialization.load_pem_private_key(f.read(), password=self.private_key_password, backend=default_backend())
            with open(self.public_key_path, "rb") as f:
                self.public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
            print(f"Loaded keys: {self.private_key_path}, {self.public_key_path}")
            return self.private_key, self.public_key
        except Exception as e:
            print(f"Error loading keys: {e}")
            raise RSAKeyError(f"Error loading keys: {e}")

    def get_public_key_pem(self):
        if not os.path.exists(self.public_key_path):
            self.load_keys()
        with open(self.public_key_path, "rb") as f:
            return f.read().decode('utf-8')

class AESCipher:
    def __init__(self, client_public_key, aes_key_size=KeySize.AES_256, aes_iv_size=IVSize.AES_BLOCK_SIZE):
        self.client_public_key = client_public_key
        self.aes_key_size = aes_key_size.value
        self.aes_iv_size = aes_iv_size.value

    def derive_aes_key(self, uid: str, t30: int) -> bytes:
        combined = (uid + str(t30) + self.client_public_key).encode('utf-8')
        return hashlib.sha256(combined).digest()  # Use full 32 bytes (256 bits)

    def derive_aes_iv(self, uid: str, t30: int) -> bytes:
        combined = (self.client_public_key + str(t30) + uid).encode('utf-8')
        return hashlib.sha256(combined).digest()[:self.aes_iv_size]  # Use first 16 bytes for IV

    def aes_decrypt(self, ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        try:
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = aes_padding.PKCS7(algorithms.AES.block_size).unpadder()
            return unpadder.update(padded_plaintext) + unpadder.finalize()
        except Exception as e:
            print(f"AES Decryption Error: {e}")
            raise AESDecryptionError("AES decryption failed.")

    def aes_encrypt(self, plaintext: bytes, key: bytes, iv: bytes) -> bytes:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = aes_padding.PKCS7(algorithms.AES.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        return encryptor.update(padded_plaintext) + encryptor.finalize()

class MultiEncrypter:
    def __init__(self, rsa_key_manager: RSAKeyManager, aes_cipher: AESCipher, xor_key_1="satya", xor_key_2="presenz"):
        self.rsa_key_manager = rsa_key_manager
        self.aes_cipher = aes_cipher
        self.xor_key_1 = xor_key_1.encode('utf-8')
        self.xor_key_2 = xor_key_2.encode('utf-8')

    def decrypt_refined_hybrid(self, payload_json: str, uid: str) -> dict:
        """Decrypts the hybrid encrypted payload."""
        try:
            payload = json.loads(payload_json)
            encrypted_aes_key_iv_b64 = payload['k']  # Encrypted AES Key+IV
            encrypted_data_b64 = payload['d']  # Encrypted Data (after XORs)
        except (json.JSONDecodeError, KeyError) as e:
            raise PayloadError(f"Invalid payload structure: {e}. Expected JSON with 'k' and 'd'.")

        # 2. Decrypt AES Key & IV using RSA Private Key
        encrypted_aes_key_iv = base64.b64decode(encrypted_aes_key_iv_b64)
        print("Attempting RSA decryption of AES key/IV...")
        recovered_aes_key_iv = self.rsa_key_manager.private_key.decrypt(encrypted_aes_key_iv, rsa_padding.OAEP(mgf=rsa_padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA512(), label=None))
        print("RSA decryption of AES key/IV successful.")

        if len(recovered_aes_key_iv) != self.aes_cipher.aes_key_size + self.aes_cipher.aes_iv_size:
            raise ValueError("Decrypted AES info has incorrect length.")
        recovered_aes_key = recovered_aes_key_iv[:self.aes_cipher.aes_key_size]
        recovered_aes_iv = recovered_aes_key_iv[self.aes_cipher.aes_key_size:]
        print(f"Recovered AES Key (Hex): {binascii.hexlify(recovered_aes_key).decode()}")
        print(f"Recovered AES IV (Hex): {binascii.hexlify(recovered_aes_iv).decode()}")

        # 3. Calculate potential T30s and derive expected AES keys/IVs
        current_ts = int(time.time())
        current_t30 = current_ts - (current_ts % 30)
        previous_t30 = current_t30 - 30
        possible_t30s = [current_t30, previous_t30]  # Check current and previous window

        print(f"Server Time: {current_ts}. Checking T30 windows: {previous_t30}, {current_t30}")

        key_match_found = False
        for t30_candidate in possible_t30s:
            print(f"  Deriving test key/IV for T30: {t30_candidate}")
            test_key = self.aes_cipher.derive_aes_key(uid, t30_candidate)
            test_iv = self.aes_cipher.derive_aes_iv(uid, t30_candidate)
            print(f"    Test Key: {binascii.hexlify(test_key).decode()}")
            print(f"    Test IV:  {binascii.hexlify(test_iv).decode()}")

            # 4. Compare recovered key/IV with derived ones
            if recovered_aes_key == test_key and recovered_aes_iv == test_iv:
                print(f"  SUCCESS: Recovered AES key/IV matches derived key for T30 {t30_candidate}.")
                key_match_found = True
                break  # Found the correct T30 window
            else:
                print(f"  Mismatch for T30 {t30_candidate}.")

        if not key_match_found:
            raise TimeWindowError("AES Key/IV verification failed. Key mismatch or invalid time window.")

        # 5. Decrypt Actual Data using the verified (recovered) AES Key & IV
        encrypted_data = base64.b64decode(encrypted_data_b64)
        print("Attempting AES decryption of data using verified key/IV...")
        decrypted_step4_bytes = self.aes_cipher.aes_decrypt(encrypted_data, recovered_aes_key, recovered_aes_iv)
        print("AES decryption of data successful.")

        # --- Reverse XOR Steps ---
        print(f"Step 1 Decrypted (AES resulted in bytes for Step 4): {binascii.hexlify(decrypted_step4_bytes[:32]).decode()}...")

        # 5. Reverse XOR with "presenz"
        step3_string = reverse_xor_presenz(decrypted_step4_bytes, self.xor_key_2)
        print(f"Step 2 Reversed (Binary String): {step3_string[:64]}...")
        try:
            step2_bytes = binary_string_to_bytes(step3_string)
        except ValueError as e:
            print(f"ERROR: Bad binary string: {e}")
            raise BinaryStringError(f"Bad binary string: {e}")
        print(f"Step 3 Reversed (XOR satya bytes): {binascii.hexlify(step2_bytes).decode()}")
        original_bytes = xor_bytes(step2_bytes, self.xor_key_1)
        print(f"Step 4 Reversed (Original Bytes): {binascii.hexlify(original_bytes).decode()}")

        # 8. Convert bytes to text -> JSON
        try:
            original_json_string = original_bytes.decode('utf-8')
            print(f"Step 5 Decoded JSON String: {original_json_string}")
            return json.loads(original_json_string)
        except Exception as e:
            raise ValueError(f"Final decoding/JSON parsing failed: {e}")

    def encrypt_refined_hybrid(self, data: dict, uid: str) -> str:
        """Encrypts data using the refined hybrid encryption scheme."""
        # 1. Serialize data to JSON
        data_json_string = json.dumps(data)
        original_bytes = data_json_string.encode('utf-8')

        # 2. XOR with "satya"
        step2_bytes = xor_bytes(original_bytes, self.xor_key_1)

        # 3. Convert bytes to binary string
        step3_string = ''.join(format(byte, '08b') for byte in step2_bytes)

        # 4. XOR with "presenz"
        decrypted_step4_bytes = reverse_xor_presenz(step3_string.encode('utf-8'), self.xor_key_2) #TODO: Fix it

        # 5. Generate T30 and derive AES key/IV
        current_ts = int(time.time())
        current_t30 = current_ts - (current_ts % 30)
        aes_key = self.aes_cipher.derive_aes_key(uid, current_t30)
        aes_iv = self.aes_cipher.derive_aes_iv(uid, current_t30)

        # 6. AES encrypt the data
        encrypted_data = self.aes_cipher.aes_encrypt(decrypted_step4_bytes.encode('utf-8'), aes_key, aes_iv)

        # 7. RSA encrypt the AES key/IV
        aes_key_iv = aes_key + aes_iv
        encrypted_aes_key_iv = self.rsa_key_manager.public_key.encrypt(
            aes_key_iv,
            rsa_padding.OAEP(
                mgf=rsa_padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )

        # 8. Base64 encode the encrypted data and encrypted AES key/IV
        encrypted_data_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        encrypted_aes_key_iv_b64 = base64.b64encode(encrypted_aes_key_iv).decode('utf-8')

        # 9. Construct the payload
        payload = {
            'k': encrypted_aes_key_iv_b64,
            'd': encrypted_data_b64
        }

        # 10. Return the JSON payload
        return json.dumps(payload)


