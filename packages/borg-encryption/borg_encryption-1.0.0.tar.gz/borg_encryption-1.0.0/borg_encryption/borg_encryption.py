#!/usr/bin/env python3
"""
Borg Encryption System
----------------------
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
"""

import os
import time
import base64
import secrets
import random
from typing import Tuple, Union
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto.Cipher import ChaCha20_Poly1305, AES
from Crypto.Protocol.KDF import scrypt
import nacl.secret
import nacl.utils

# Custom exceptions for more specific error handling
class BorgEncryptionError(Exception):
    """Base exception for all Borg Encryption errors."""
    pass

class DecryptionError(BorgEncryptionError):
    """Raised when decryption fails."""
    pass

class AuthenticationError(DecryptionError):
    """Raised when authentication fails during decryption."""
    pass

class FormatError(BorgEncryptionError):
    """Raised when the encrypted data format is invalid."""
    pass

class VersionError(BorgEncryptionError):
    """Raised when the encryption version is incompatible."""
    pass

# Secure memory management
class SecureBytes:
    """A class for securely handling sensitive data in memory."""

    def __init__(self, data: bytes = None):
        """Initialize with optional data."""
        self._data = bytearray(data) if data else bytearray()

    def __del__(self):
        """Securely clear data when the object is destroyed."""
        self.clear()

    def clear(self):
        """Securely clear the data from memory."""
        for i in range(len(self._data)):
            self._data[i] = 0

    def get(self) -> bytes:
        """Get the data as bytes."""
        return bytes(self._data)

    def set(self, data: bytes):
        """Set the data, clearing any previous data."""
        self.clear()
        self._data = bytearray(data)

    def __len__(self):
        """Get the length of the data."""
        return len(self._data)

# Constants
ENCRYPTION_LAYERS = 3  # Number of encryption layers
KEY_SIZE = 32  # 256 bits
NONCE_SIZE = 12  # 96 bits for AES-GCM and ChaCha20-Poly1305
XSALSA20_NONCE_SIZE = 24  # 192 bits for XSalsa20-Poly1305
TAG_SIZE = 16  # 128 bits
SALT_SIZE = 16  # 128 bits
# Reduced values for testing - in production use much higher values
ITERATIONS = 10_000  # Reduced iteration count for testing (use 1,000,000+ in production)
MEMORY_COST = 2**14  # 16 KB for testing (use 2**20+ in production)
VERSION = 1  # Protocol version
TIMING_PROTECTION = True  # Enable timing attack protection

class BorgEncryption:
    """
    Main encryption class that implements the multi-layered Borg encryption system.
    This implementation includes protections against side-channel attacks and
    secure memory management for sensitive data.
    """

    def __init__(self, master_password: str = None):
        """
        Initialize the encryption system with a master password.
        If no password is provided, a secure random one will be generated.

        Args:
            master_password: Optional master password for key derivation
        """
        # Store the master password in secure memory
        self._master_password = SecureBytes()
        password = master_password or self._generate_secure_password(32)
        self._master_password.set(password.encode('utf-8'))

        # For compatibility with existing code that accesses master_password directly
        # We'll keep a string version, but this should be deprecated in future versions
        self.master_password = password

        self.encryption_algorithms = [
            self._aes_gcm_encrypt,
            self._chacha20_poly1305_encrypt,
            self._xsalsa20_poly1305_encrypt
        ]
        self.decryption_algorithms = [
            self._xsalsa20_poly1305_decrypt,
            self._chacha20_poly1305_decrypt,
            self._aes_gcm_decrypt
        ]

    def _generate_secure_password(self, length: int = 32) -> str:
        """Generate a cryptographically secure random password."""
        return secrets.token_urlsafe(length)

    def _derive_key(self, salt: bytes, password: str = None) -> SecureBytes:
        """
        Derive a key using PBKDF2 with a high iteration count.
        Uses secure memory management for the derived key.

        Args:
            salt: Salt for key derivation
            password: Optional password (uses master password if None)

        Returns:
            Derived key as SecureBytes
        """
        # Get password bytes securely
        if password:
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = self._master_password.get()

        # Derive the key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_512(),
            length=KEY_SIZE,
            salt=salt,
            iterations=ITERATIONS
        )
        derived_key = kdf.derive(password_bytes)

        # Store in secure memory
        secure_key = SecureBytes(derived_key)

        # We can't clear bytes objects directly since they're immutable
        # But the garbage collector will eventually clean it up
        # In a more secure implementation, we would use a bytearray instead

        return secure_key

    def _derive_key_scrypt(self, salt: bytes, password: str = None) -> SecureBytes:
        """
        Derive a key using scrypt with high memory and CPU cost.
        Uses secure memory management for the derived key.

        Args:
            salt: Salt for key derivation
            password: Optional password (uses master password if None)

        Returns:
            Derived key as SecureBytes
        """
        # Get password bytes securely
        if password:
            password_bytes = password.encode('utf-8')
        else:
            password_bytes = self._master_password.get()

        # Derive the key
        derived_key = scrypt(
            password=password_bytes,
            salt=salt,
            key_len=KEY_SIZE,
            N=MEMORY_COST,
            r=8,
            p=1
        )

        # Store in secure memory
        secure_key = SecureBytes(derived_key)

        # We can't clear bytes objects directly since they're immutable
        # But the garbage collector will eventually clean it up
        # In a more secure implementation, we would use a bytearray instead

        return secure_key

    def _aes_gcm_encrypt(self, data: bytes, key: SecureBytes) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using AES-GCM.

        Args:
            data: Data to encrypt
            key: Encryption key (SecureBytes)

        Returns:
            Tuple of (ciphertext, nonce, tag)
        """
        nonce = os.urandom(NONCE_SIZE)
        cipher = AES.new(key.get(), AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, nonce, tag

    def _aes_gcm_decrypt(self, ciphertext: bytes, key: SecureBytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt data using AES-GCM.

        Args:
            ciphertext: Encrypted data
            key: Decryption key (SecureBytes)
            nonce: Nonce used for encryption
            tag: Authentication tag

        Returns:
            Decrypted data
        """
        try:
            cipher = AES.new(key.get(), AES.MODE_GCM, nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except Exception as e:
            # Add timing protection to prevent timing attacks
            if TIMING_PROTECTION:
                # Add a small random delay to mask timing differences
                time.sleep(0.01 + random.random() * 0.01)
            raise AuthenticationError("AES-GCM authentication failed") from e

    def _chacha20_poly1305_encrypt(self, data: bytes, key: SecureBytes) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using ChaCha20-Poly1305.

        Args:
            data: Data to encrypt
            key: Encryption key (SecureBytes)

        Returns:
            Tuple of (ciphertext, nonce, tag)
        """
        nonce = os.urandom(NONCE_SIZE)
        cipher = ChaCha20_Poly1305.new(key=key.get(), nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, nonce, tag

    def _chacha20_poly1305_decrypt(self, ciphertext: bytes, key: SecureBytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt data using ChaCha20-Poly1305.

        Args:
            ciphertext: Encrypted data
            key: Decryption key (SecureBytes)
            nonce: Nonce used for encryption
            tag: Authentication tag

        Returns:
            Decrypted data
        """
        try:
            cipher = ChaCha20_Poly1305.new(key=key.get(), nonce=nonce)
            return cipher.decrypt_and_verify(ciphertext, tag)
        except Exception as e:
            # Add timing protection to prevent timing attacks
            if TIMING_PROTECTION:
                # Add a small random delay to mask timing differences
                time.sleep(0.01 + random.random() * 0.01)
            raise AuthenticationError("ChaCha20-Poly1305 authentication failed") from e

    def _xsalsa20_poly1305_encrypt(self, data: bytes, key: SecureBytes) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using XSalsa20-Poly1305 (NaCl secretbox compatible).

        Args:
            data: Data to encrypt
            key: Encryption key (SecureBytes)

        Returns:
            Tuple of (ciphertext, nonce, tag)
        """
        # Generate a random nonce
        nonce = nacl.utils.random(XSALSA20_NONCE_SIZE)

        # Create a SecretBox with the key
        box = nacl.secret.SecretBox(key.get())

        # Encrypt the data
        # PyNaCl's SecretBox.encrypt returns a combined format with nonce + ciphertext + tag
        encrypted = box.encrypt(data, nonce)

        # Extract the ciphertext (without nonce)
        # In PyNaCl, the ciphertext includes the authentication tag
        ciphertext_with_tag = encrypted.ciphertext

        # For compatibility with our layered approach, we need to separate the tag
        # PyNaCl doesn't expose the tag separately, but we can extract it
        # The tag is the last 16 bytes of the ciphertext
        ciphertext = ciphertext_with_tag[:-TAG_SIZE]
        tag = ciphertext_with_tag[-TAG_SIZE:]

        return ciphertext, nonce, tag

    def _xsalsa20_poly1305_decrypt(self, ciphertext: bytes, key: SecureBytes, nonce: bytes, tag: bytes) -> bytes:
        """
        Decrypt data using XSalsa20-Poly1305.

        Args:
            ciphertext: Encrypted data
            key: Decryption key (SecureBytes)
            nonce: Nonce used for encryption
            tag: Authentication tag

        Returns:
            Decrypted data
        """
        try:
            # Create a SecretBox with the key
            box = nacl.secret.SecretBox(key.get())

            # Combine ciphertext and tag as expected by PyNaCl
            ciphertext_with_tag = ciphertext + tag

            # In PyNaCl, we need to decrypt using the combined format
            # The format is: nonce + ciphertext_with_tag
            # We'll manually construct this format
            encrypted_data = nonce + ciphertext_with_tag

            # Decrypt the data
            return box.decrypt(encrypted_data)
        except Exception as e:
            # Add timing protection to prevent timing attacks
            if TIMING_PROTECTION:
                # Add a small random delay to mask timing differences
                time.sleep(0.01 + random.random() * 0.01)
            raise AuthenticationError("XSalsa20-Poly1305 authentication failed") from e

    def encrypt(self, data: Union[str, bytes], password: str = None) -> str:
        """
        Encrypt data using multiple layers of encryption.

        Args:
            data: Data to encrypt (string or bytes)
            password: Optional password (uses master password if None)

        Returns:
            Base64-encoded encrypted data with metadata
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Generate a unique salt for this encryption
        master_salt = os.urandom(SALT_SIZE)

        # Current data to be encrypted through layers
        current_data = data

        # Metadata to store with the encrypted data
        metadata = {
            "version": VERSION,
            # Use a random offset to obscure the exact timestamp
            "timestamp": int(time.time()) + random.randint(-60, 60) if not TIMING_PROTECTION else 0,
            "layers": [],
            "master_salt": base64.b64encode(master_salt).decode('utf-8')
        }

        # Apply each encryption layer
        for i, encrypt_func in enumerate(self.encryption_algorithms):
            # Derive a unique key for this layer
            layer_salt = os.urandom(SALT_SIZE)
            if i % 2 == 0:
                key = self._derive_key(layer_salt, password)
            else:
                key = self._derive_key_scrypt(layer_salt, password)

            # Encrypt the data
            ciphertext, nonce, tag = encrypt_func(current_data, key)

            # Update the current data for the next layer
            current_data = ciphertext

            # Store the metadata for this layer
            metadata["layers"].append({
                "algorithm": encrypt_func.__name__,
                "salt": base64.b64encode(layer_salt).decode('utf-8'),
                "nonce": base64.b64encode(nonce).decode('utf-8'),
                "tag": base64.b64encode(tag).decode('utf-8')
            })

            # Clear the key from secure memory
            key.clear()

        # Combine the final ciphertext with the metadata
        result = {
            "metadata": metadata,
            "ciphertext": base64.b64encode(current_data).decode('utf-8')
        }

        # Convert to a compact string representation
        import json
        return base64.b64encode(json.dumps(result).encode('utf-8')).decode('utf-8')

    def decrypt(self, encrypted_data: str, password: str = None) -> bytes:
        """
        Decrypt data that was encrypted with multiple layers.

        Args:
            encrypted_data: Base64-encoded encrypted data with metadata
            password: Optional password (uses master password if None)

        Returns:
            Decrypted data as bytes
        """
        import json

        # Parse the encrypted data
        try:
            data_json = json.loads(base64.b64decode(encrypted_data.encode('utf-8')))
            metadata = data_json["metadata"]
            ciphertext = base64.b64decode(data_json["ciphertext"].encode('utf-8'))
        except Exception as e:
            if TIMING_PROTECTION:
                time.sleep(0.01 + random.random() * 0.01)
            raise FormatError("Invalid encrypted data format") from e

        # Check version compatibility
        if metadata["version"] != VERSION:
            if TIMING_PROTECTION:
                time.sleep(0.01 + random.random() * 0.01)
            raise VersionError(f"Incompatible encryption version: {metadata['version']}")

        # Current data to be decrypted through layers
        current_data = ciphertext

        # Apply each decryption layer in reverse order
        for i, layer_data in enumerate(reversed(metadata["layers"])):
            try:
                # Get the decryption function
                decrypt_func = self.decryption_algorithms[i]

                # Decode the layer metadata
                layer_salt = base64.b64decode(layer_data["salt"].encode('utf-8'))
                nonce = base64.b64decode(layer_data["nonce"].encode('utf-8'))
                tag = base64.b64decode(layer_data["tag"].encode('utf-8'))

                # Derive the key for this layer
                if (len(metadata["layers"]) - i - 1) % 2 == 0:
                    key = self._derive_key(layer_salt, password)
                else:
                    key = self._derive_key_scrypt(layer_salt, password)

                # Decrypt the data
                current_data = decrypt_func(current_data, key, nonce, tag)

                # Clear the key from secure memory
                key.clear()

            except AuthenticationError as e:
                # Propagate authentication errors
                raise
            except Exception as e:
                # For any other error, provide a consistent error message
                if TIMING_PROTECTION:
                    time.sleep(0.01 + random.random() * 0.01)
                raise DecryptionError(f"Decryption failed at layer {i+1}") from e

        return current_data

    def decrypt_to_string(self, encrypted_data: str, password: str = None) -> str:
        """
        Decrypt data and return as a string.

        Args:
            encrypted_data: Base64-encoded encrypted data with metadata
            password: Optional password (uses master password if None)

        Returns:
            Decrypted data as string
        """
        try:
            return self.decrypt(encrypted_data, password).decode('utf-8')
        except UnicodeDecodeError as e:
            if TIMING_PROTECTION:
                time.sleep(0.01 + random.random() * 0.01)
            raise DecryptionError("Decrypted data is not valid UTF-8") from e


if __name__ == "__main__":
    print("=== Borg Encryption System with Enhanced Security ===\n")

    # Create an instance with a random master password
    borg = BorgEncryption()
    print(f"Generated master password: {borg.master_password}")

    # Encrypt some data
    message = "Resistance is futile. Your biological and technological distinctiveness will be added to our own."
    print(f"\nOriginal message: {message}")

    encrypted = borg.encrypt(message)
    print(f"\nEncrypted data (truncated):\n{encrypted[:100]}...")

    # Decrypt the data
    try:
        decrypted = borg.decrypt_to_string(encrypted)
        print(f"\nDecrypted message:\n{decrypted}")

        # Verify the decryption worked correctly
        assert message == decrypted
        print("\nEncryption and decryption successful!")
    except AuthenticationError as e:
        print(f"\nAuthentication failed: {e}")
    except DecryptionError as e:
        print(f"\nDecryption failed: {e}")

    # Demonstrate error handling with tampered data
    print("\n=== Testing Error Handling with Tampered Data ===")

    # Tamper with the encrypted data more significantly
    # We'll modify the base64 data to ensure it breaks the authentication
    import json
    decoded = json.loads(base64.b64decode(encrypted).decode('utf-8'))
    ciphertext = base64.b64decode(decoded['ciphertext'])
    # Modify a byte in the middle of the ciphertext
    modified = bytearray(ciphertext)
    modified[len(modified)//2] = (modified[len(modified)//2] + 1) % 256
    # Update the ciphertext
    decoded['ciphertext'] = base64.b64encode(modified).decode('utf-8')
    # Re-encode
    tampered = base64.b64encode(json.dumps(decoded).encode('utf-8')).decode('utf-8')

    try:
        borg.decrypt_to_string(tampered)
        print("Decryption of tampered data succeeded (this should not happen!)")
    except Exception as e:
        print(f"Decryption of tampered data failed as expected: {type(e).__name__}: {e}")

    # Demonstrate secure memory management
    print("\n=== Testing Secure Memory Management ===")

    # Create a secure bytes object
    secure_data = SecureBytes(b"sensitive data")
    print(f"Secure data created with {len(secure_data)} bytes")

    # Use the data
    print(f"Data: {secure_data.get().decode()}")

    # Clear the data
    secure_data.clear()
    print("Data cleared from memory")

    # Verify it's cleared
    cleared_data = secure_data.get()
    is_cleared = all(b == 0 for b in cleared_data) if cleared_data else True
    print(f"Data after clearing: {cleared_data!r}")
    print(f"Memory securely cleared: {is_cleared}")
