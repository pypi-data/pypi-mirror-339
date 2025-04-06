# src/multienc/enums.py
from enum import Enum

class KeySize(Enum):
    AES_256 = 32  # AES-256 key size in bytes

class IVSize(Enum):
    AES_BLOCK_SIZE = 16 # AES block size for IV in bytes