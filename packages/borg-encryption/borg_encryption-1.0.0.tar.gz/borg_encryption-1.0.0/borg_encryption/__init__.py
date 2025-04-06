"""
Borg Encryption System
=====================

A multi-layered, adaptive encryption system inspired by the Borg from Star Trek.
This system uses multiple encryption algorithms in sequence, including post-quantum
resistant algorithms, to create an extremely secure encryption mechanism.

Features:
- Multi-layered encryption (cascading ciphers)
- Post-quantum resistant algorithms
- Adaptive security measures
- Key rotation
- Side-channel attack protections
- Secure memory management
- REST API for easy integration
"""

__version__ = "1.0.0"
__author__ = "Borg Collective"
__license__ = "MIT"

from .borg_encryption import BorgEncryption, SecureBytes
from .key_manager import KeyManager
from .adaptive_defense import AdaptiveDefense

__all__ = [
    "BorgEncryption",
    "SecureBytes",
    "KeyManager",
    "AdaptiveDefense",
]
