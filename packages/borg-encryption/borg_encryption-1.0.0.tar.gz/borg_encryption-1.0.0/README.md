# Borg Encryption System

A multi-layered, adaptive encryption system inspired by the Borg from Star Trek. This system uses multiple encryption algorithms in sequence, including post-quantum resistant algorithms, to create an extremely secure encryption mechanism.

## Features

- **Multi-layered encryption** (cascading ciphers)
- **Post-quantum resistant algorithms**
- **Adaptive security measures**
- **Key rotation**
- **Side-channel attack protections**
- **Secure memory management**
- **REST API** for easy integration

## Installation

```bash
pip install borg-encryption
```

## Quick Start

### Command Line Usage

```bash
# Encrypt a text message
borg-encrypt encrypt --text "Resistance is futile" --key "your-password" --local

# Decrypt a text message
borg-encrypt decrypt --file encrypted.txt --key "your-password" --local

# Encrypt a file
borg-encrypt encrypt-file --file secret.pdf --key "your-password" --output secret.encrypted --local

# Decrypt a file
borg-encrypt decrypt-file --file secret.encrypted --key "your-password" --output secret.pdf --local

# Start the API server
borg-encrypt server --port 8000
```

### Python API Usage

```python
from borg_encryption import BorgEncryption

# Create an encryption instance
borg = BorgEncryption("your-password")

# Encrypt data
message = "Resistance is futile. Your biological and technological distinctiveness will be added to our own."
encrypted = borg.encrypt(message)

# Decrypt data
decrypted = borg.decrypt_to_string(encrypted)
print(decrypted)  # Should print the original message
```

### REST API Usage

```python
from borg_encryption.client import BorgAPIClient

# Create a client
client = BorgAPIClient("http://localhost:8000", "your-api-key")

# Encrypt a message
encrypted = client.encrypt_text("Resistance is futile", "your-password")

# Decrypt a message
decrypted = client.decrypt_text(encrypted, "your-password")
```

## Security Features

- **Multi-layered encryption**: Uses AES-GCM, ChaCha20-Poly1305, and XSalsa20-Poly1305 in sequence
- **Secure key derivation**: Uses PBKDF2 and Scrypt with high iteration counts
- **Adaptive defense**: Monitors for attacks and adapts security parameters
- **Secure memory management**: Clears sensitive data from memory when no longer needed
- **Side-channel attack protections**: Implements timing attack countermeasures

## License

MIT License
