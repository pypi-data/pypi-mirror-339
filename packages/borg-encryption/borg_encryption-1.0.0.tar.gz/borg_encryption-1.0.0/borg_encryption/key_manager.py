#!/usr/bin/env python3
"""
Borg Key Manager
---------------
Handles key generation, storage, rotation, and management for the Borg Encryption System.
Implements advanced key management techniques to ensure maximum security.
"""

import os
import time
import json
import base64
import secrets
import hashlib
from typing import Dict, List, Tuple, Optional, Any, Union
from cryptography.hazmat.primitives.asymmetric import rsa, x25519, ed25519
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet

# Constants
KEY_ROTATION_INTERVAL = 30 * 24 * 60 * 60  # 30 days in seconds
RSA_KEY_SIZE = 4096
SYMMETRIC_KEY_SIZE = 32  # 256 bits
HASH_ALGORITHM = hashes.SHA3_512()
KEY_STORAGE_FILE = "borg_keys.encrypted"


class KeyManager:
    """
    Manages encryption keys for the Borg Encryption System.
    Handles key generation, rotation, and secure storage.
    """
    
    def __init__(self, master_password: str):
        """
        Initialize the key manager with a master password.
        
        Args:
            master_password: Master password for securing the key storage
        """
        self.master_password = master_password
        self.keys = self._load_keys() or self._initialize_keys()
        
    def _derive_master_key(self, salt: bytes) -> bytes:
        """
        Derive a master key from the master password using Scrypt.
        
        Args:
            salt: Salt for key derivation
            
        Returns:
            Derived master key
        """
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**20,  # Memory cost
            r=8,       # Block size
            p=1        # Parallelization
        )
        return kdf.derive(self.master_password.encode('utf-8'))
    
    def _initialize_keys(self) -> Dict[str, Any]:
        """
        Initialize a new set of encryption keys.
        
        Returns:
            Dictionary containing the generated keys
        """
        # Generate a salt for the master key
        master_salt = os.urandom(16)
        
        # Generate symmetric keys
        aes_key = os.urandom(SYMMETRIC_KEY_SIZE)
        chacha_key = os.urandom(SYMMETRIC_KEY_SIZE)
        xsalsa_key = os.urandom(SYMMETRIC_KEY_SIZE)
        
        # Generate RSA key pair
        rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=RSA_KEY_SIZE
        )
        rsa_public_key = rsa_private_key.public_key()
        
        # Generate X25519 key pair for key exchange
        x25519_private_key = x25519.X25519PrivateKey.generate()
        x25519_public_key = x25519_private_key.public_key()
        
        # Generate Ed25519 key pair for signatures
        ed25519_private_key = ed25519.Ed25519PrivateKey.generate()
        ed25519_public_key = ed25519_private_key.public_key()
        
        # Serialize keys
        rsa_private_bytes = rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        rsa_public_bytes = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        x25519_private_bytes = x25519_private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        x25519_public_bytes = x25519_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        ed25519_private_bytes = ed25519_private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        ed25519_public_bytes = ed25519_public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Create key dictionary
        keys = {
            "created_at": int(time.time()),
            "last_rotated": int(time.time()),
            "master_salt": base64.b64encode(master_salt).decode('utf-8'),
            "symmetric_keys": {
                "aes": base64.b64encode(aes_key).decode('utf-8'),
                "chacha": base64.b64encode(chacha_key).decode('utf-8'),
                "xsalsa": base64.b64encode(xsalsa_key).decode('utf-8')
            },
            "asymmetric_keys": {
                "rsa": {
                    "private": base64.b64encode(rsa_private_bytes).decode('utf-8'),
                    "public": base64.b64encode(rsa_public_bytes).decode('utf-8')
                },
                "x25519": {
                    "private": base64.b64encode(x25519_private_bytes).decode('utf-8'),
                    "public": base64.b64encode(x25519_public_bytes).decode('utf-8')
                },
                "ed25519": {
                    "private": base64.b64encode(ed25519_private_bytes).decode('utf-8'),
                    "public": base64.b64encode(ed25519_public_bytes).decode('utf-8')
                }
            },
            "key_history": []
        }
        
        # Save the keys
        self._save_keys(keys)
        
        return keys
    
    def _save_keys(self, keys: Dict[str, Any]) -> None:
        """
        Save the keys to an encrypted file.
        
        Args:
            keys: Dictionary containing the keys to save
        """
        # Convert keys to JSON
        keys_json = json.dumps(keys)
        
        # Derive the master key
        master_salt = base64.b64decode(keys["master_salt"].encode('utf-8'))
        master_key = self._derive_master_key(master_salt)
        
        # Create a Fernet key from the master key
        fernet_key = base64.urlsafe_b64encode(master_key)
        fernet = Fernet(fernet_key)
        
        # Encrypt the keys
        encrypted_keys = fernet.encrypt(keys_json.encode('utf-8'))
        
        # Save to file
        with open(KEY_STORAGE_FILE, 'wb') as f:
            f.write(encrypted_keys)
    
    def _load_keys(self) -> Optional[Dict[str, Any]]:
        """
        Load keys from the encrypted storage file.
        
        Returns:
            Dictionary containing the keys, or None if the file doesn't exist
        """
        if not os.path.exists(KEY_STORAGE_FILE):
            return None
        
        try:
            # Read the encrypted keys
            with open(KEY_STORAGE_FILE, 'rb') as f:
                encrypted_keys = f.read()
            
            # Try to decrypt with the current master password
            # We need to try different salts if the master password has changed
            # For simplicity, we'll just try the current salt
            
            # Parse the salt from the encrypted data
            # This is a simplified approach - in a real implementation,
            # you would store the salt separately or in a header
            
            # For now, we'll try to decrypt and catch exceptions
            for attempt in range(3):  # Try a few different methods
                try:
                    if attempt == 0:
                        # Try to decrypt directly
                        # This assumes the master password hasn't changed
                        temp_keys = json.loads(encrypted_keys)
                        master_salt = base64.b64decode(temp_keys["master_salt"].encode('utf-8'))
                    elif attempt == 1:
                        # Try with a default salt
                        master_salt = b'BorgCollective123'
                    else:
                        # Try with a derived salt
                        master_salt = hashlib.sha256(self.master_password.encode('utf-8')).digest()[:16]
                    
                    master_key = self._derive_master_key(master_salt)
                    fernet_key = base64.urlsafe_b64encode(master_key)
                    fernet = Fernet(fernet_key)
                    
                    decrypted_keys = fernet.decrypt(encrypted_keys)
                    return json.loads(decrypted_keys.decode('utf-8'))
                except Exception as e:
                    if attempt == 2:
                        print(f"Failed to decrypt keys: {e}")
                        return None
                    continue
            
            return None
        except Exception as e:
            print(f"Error loading keys: {e}")
            return None
    
    def rotate_keys(self, force: bool = False) -> bool:
        """
        Rotate encryption keys if the rotation interval has passed.
        
        Args:
            force: Force key rotation regardless of the interval
            
        Returns:
            True if keys were rotated, False otherwise
        """
        current_time = int(time.time())
        last_rotated = self.keys.get("last_rotated", 0)
        
        if not force and (current_time - last_rotated) < KEY_ROTATION_INTERVAL:
            return False
        
        # Archive the current keys
        self.keys["key_history"].append({
            "rotated_at": current_time,
            "symmetric_keys": self.keys["symmetric_keys"],
            "asymmetric_keys": {
                "rsa": {"public": self.keys["asymmetric_keys"]["rsa"]["public"]},
                "x25519": {"public": self.keys["asymmetric_keys"]["x25519"]["public"]},
                "ed25519": {"public": self.keys["asymmetric_keys"]["ed25519"]["public"]}
            }
        })
        
        # Limit the history to the last 10 rotations
        if len(self.keys["key_history"]) > 10:
            self.keys["key_history"] = self.keys["key_history"][-10:]
        
        # Generate new symmetric keys
        self.keys["symmetric_keys"] = {
            "aes": base64.b64encode(os.urandom(SYMMETRIC_KEY_SIZE)).decode('utf-8'),
            "chacha": base64.b64encode(os.urandom(SYMMETRIC_KEY_SIZE)).decode('utf-8'),
            "xsalsa": base64.b64encode(os.urandom(SYMMETRIC_KEY_SIZE)).decode('utf-8')
        }
        
        # Update the rotation timestamp
        self.keys["last_rotated"] = current_time
        
        # Save the updated keys
        self._save_keys(self.keys)
        
        return True
    
    def get_symmetric_key(self, key_type: str) -> bytes:
        """
        Get a symmetric key of the specified type.
        
        Args:
            key_type: Type of key to retrieve ('aes', 'chacha', or 'xsalsa')
            
        Returns:
            The requested key as bytes
        """
        if key_type not in self.keys["symmetric_keys"]:
            raise ValueError(f"Unknown key type: {key_type}")
        
        return base64.b64decode(self.keys["symmetric_keys"][key_type].encode('utf-8'))
    
    def get_rsa_private_key(self) -> rsa.RSAPrivateKey:
        """
        Get the RSA private key.
        
        Returns:
            RSA private key object
        """
        private_bytes = base64.b64decode(self.keys["asymmetric_keys"]["rsa"]["private"].encode('utf-8'))
        return serialization.load_pem_private_key(
            private_bytes,
            password=None
        )
    
    def get_rsa_public_key(self) -> rsa.RSAPublicKey:
        """
        Get the RSA public key.
        
        Returns:
            RSA public key object
        """
        public_bytes = base64.b64decode(self.keys["asymmetric_keys"]["rsa"]["public"].encode('utf-8'))
        return serialization.load_pem_public_key(public_bytes)
    
    def get_x25519_private_key(self) -> x25519.X25519PrivateKey:
        """
        Get the X25519 private key.
        
        Returns:
            X25519 private key object
        """
        private_bytes = base64.b64decode(self.keys["asymmetric_keys"]["x25519"]["private"].encode('utf-8'))
        return x25519.X25519PrivateKey.from_private_bytes(private_bytes)
    
    def get_x25519_public_key(self) -> x25519.X25519PublicKey:
        """
        Get the X25519 public key.
        
        Returns:
            X25519 public key object
        """
        public_bytes = base64.b64decode(self.keys["asymmetric_keys"]["x25519"]["public"].encode('utf-8'))
        return x25519.X25519PublicKey.from_public_bytes(public_bytes)
    
    def get_ed25519_private_key(self) -> ed25519.Ed25519PrivateKey:
        """
        Get the Ed25519 private key.
        
        Returns:
            Ed25519 private key object
        """
        private_bytes = base64.b64decode(self.keys["asymmetric_keys"]["ed25519"]["private"].encode('utf-8'))
        return ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
    
    def get_ed25519_public_key(self) -> ed25519.Ed25519PublicKey:
        """
        Get the Ed25519 public key.
        
        Returns:
            Ed25519 public key object
        """
        public_bytes = base64.b64decode(self.keys["asymmetric_keys"]["ed25519"]["public"].encode('utf-8'))
        return ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)
    
    def export_public_keys(self) -> Dict[str, str]:
        """
        Export all public keys for sharing.
        
        Returns:
            Dictionary containing the public keys
        """
        return {
            "rsa": self.keys["asymmetric_keys"]["rsa"]["public"],
            "x25519": self.keys["asymmetric_keys"]["x25519"]["public"],
            "ed25519": self.keys["asymmetric_keys"]["ed25519"]["public"]
        }


if __name__ == "__main__":
    # Create a key manager with a master password
    manager = KeyManager("resistance-is-futile")
    
    # Get a symmetric key
    aes_key = manager.get_symmetric_key("aes")
    print(f"AES Key: {base64.b64encode(aes_key).decode('utf-8')}")
    
    # Export public keys
    public_keys = manager.export_public_keys()
    print("\nPublic Keys:")
    for key_type, key_value in public_keys.items():
        print(f"{key_type}: {key_value[:64]}...")
    
    # Rotate keys
    rotated = manager.rotate_keys(force=True)
    print(f"\nKeys rotated: {rotated}")
    
    # Get the new AES key after rotation
    new_aes_key = manager.get_symmetric_key("aes")
    print(f"\nNew AES Key: {base64.b64encode(new_aes_key).decode('utf-8')}")
    
    # Verify the keys are different
    print(f"\nKeys are different: {aes_key != new_aes_key}")
