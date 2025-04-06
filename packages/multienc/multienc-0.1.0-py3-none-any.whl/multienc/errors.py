# src/multienc/errors.py

class MultiEncError(Exception):
    """Base class for all multienc exceptions."""
    pass

class RSAKeyError(MultiEncError):
    """Raised when there is an issue with RSA key loading or generation."""
    pass

class AESDecryptionError(MultiEncError):
    """Raised when AES decryption fails."""
    pass

class PayloadError(MultiEncError):
    """Raised when the payload is invalid or improperly structured."""
    pass

class TimeWindowError(MultiEncError):
    """Raised when the time window for key derivation is invalid."""
    pass

class BinaryStringError(MultiEncError):
    """Raised when the binary string is invalid."""
    pass