# src/multienc/helpers.py
import binascii

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

def reverse_xor_presenz(step4_bytes: bytes, key: bytes) -> str:
    """
    XORs the bytes received after AES decryption with the key ('presenz') to recover the bytes of the original binary string.
    Then decodes those bytes as UTF-8 to get the binary string itself.
    """
    xored_bytes_list = [step4_bytes[i] ^ key[i % len(key)] for i in range(len(step4_bytes))]
    binary_string_bytes = bytes(xored_bytes_list)
    try:
        # The result *should* be the original binary string, decodable as UTF-8
        return binary_string_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # If this happens, something is wrong upstream
        print(f"DEBUG: Bytes after presenz XOR (hex): {binascii.hexlify(binary_string_bytes).decode()}")
        raise ValueError("Reverse XOR with 'presenz' did not result in bytes decodable to a UTF-8 binary string.")


def binary_string_to_bytes(bin_str: str) -> bytes:
    if len(bin_str) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")
    try:
        return bytes([int(bin_str[i:i+8], 2) for i in range(0, len(bin_str), 8)])
    except ValueError as e:
        raise ValueError(f"Invalid character in binary string: {e}")