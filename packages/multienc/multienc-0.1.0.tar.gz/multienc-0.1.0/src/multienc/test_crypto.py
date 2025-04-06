import unittest
import json
import os
from .crypto import RSAKeyManager, AESCipher, MultiEncrypter
from .errors import PayloadError

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.rsa_key_manager = RSAKeyManager(private_key_path="test_private_key.pem", public_key_path="test_public_key.pem", private_key_password=b"test_password")
        self.aes_cipher = AESCipher(client_public_key="test_client_key")
        self.multi_encrypter = MultiEncrypter(self.rsa_key_manager, self.aes_cipher)

    def tearDown(self):
        try:
            os.remove("test_private_key.pem")
            os.remove("test_public_key.pem")
        except FileNotFoundError:
            pass

    def test_rsa_key_generation(self):
        self.rsa_key_manager.generate_keys()
        self.assertTrue(os.path.exists("test_private_key.pem"))
        self.assertTrue(os.path.exists("test_public_key.pem"))

    def test_invalid_payload_structure(self):
        with self.assertRaises(PayloadError):
            self.multi_encrypter.decrypt_refined_hybrid('{"invalid": "payload"}', "test_uid")

    def test_encryption_decryption(self):
        # Create a sample payload
        data = {"message": "Hello, world!", "iam": "immortal"}
        uid = "test_uid"

        # Encrypt the data
        encrypted_payload = self.multi_encrypter.encrypt_refined_hybrid(data, uid)

        # Decrypt the data
        decrypted_json = self.multi_encrypter.decrypt_refined_hybrid(encrypted_payload, uid)

        # Assert that the decrypted data matches the original data
        self.assertEqual(data, decrypted_json)

if __name__ == '__main__':
    unittest.main()