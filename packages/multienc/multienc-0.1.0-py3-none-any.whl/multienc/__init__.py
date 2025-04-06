# src/multienc/__init__.py

from .crypto import (
    RSAKeyManager,
    AESCipher,
    MultiEncrypter,
)

from .errors import (
    MultiEncError,
    RSAKeyError,
    AESDecryptionError,
    PayloadError,
    TimeWindowError,
    BinaryStringError,
)

from .enums import KeySize, IVSize

__all__ = [
    "RSAKeyManager",
    "AESCipher",
    "MultiEncrypter",
    "MultiEncError",
    "RSAKeyError",
    "AESDecryptionError",
    "PayloadError",
    "TimeWindowError",
    "BinaryStringError",
    "KeySize",
    "IVSize",
]

try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("multienc")
    except PackageNotFoundError:
        __version__ = "0.1"
except ImportError:
    # For Python < 3.8
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution("multienc").version
    except Exception:
        __version__ = "0.1"

__author__ = "Satyendra Bongi (s4tyendra)"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2023 Satyendra Bongi"
__description__ = "A refined hybrid encryption/decryption library for secure data transmission."
