#!/usr/bin/env python3
"""
Borg Encryption System API Client
--------------------------------
A client for the Borg Encryption System API.
"""

import os
import base64
import requests
from typing import Dict, List, Optional, Any


class BorgAPIClient:
    """Client for the Borg Encryption System API."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.api_key = api_key or os.environ.get("API_KEY", "resistance-is-futile")
        self.session.headers.update({"X-API-Key": self.api_key})
    
    def encrypt_text(self, text: str, password: str) -> Optional[str]:
        """
        Encrypt text using the Borg Encryption System.
        
        Args:
            text: Text to encrypt
            password: Encryption password
            
        Returns:
            Encrypted text or None if encryption failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/encrypt",
                json={"data": text, "password": password}
            )
            response.raise_for_status()
            
            data = response.json()
            return data["encrypted_data"]
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt_text(self, encrypted_text: str, password: str) -> Optional[str]:
        """
        Decrypt text using the Borg Encryption System.
        
        Args:
            encrypted_text: Encrypted text to decrypt
            password: Decryption password
            
        Returns:
            Decrypted text or None if decryption failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/decrypt",
                json={"encrypted_data": encrypted_text, "password": password}
            )
            response.raise_for_status()
            
            data = response.json()
            return data["decrypted_data"]
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def encrypt_file(self, file_path: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Encrypt a file using the Borg Encryption System.
        
        Args:
            file_path: Path to the file to encrypt
            password: Encryption password
            
        Returns:
            Dictionary with encrypted data and filename, or None if encryption failed
        """
        try:
            # Read the file
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Encode the file content as base64
            file_content_base64 = base64.b64encode(file_content).decode('utf-8')
            
            # Get the filename
            filename = os.path.basename(file_path)
            
            response = self.session.post(
                f"{self.base_url}/encrypt/file",
                json={
                    "file_content": file_content_base64,
                    "password": password,
                    "filename": filename
                }
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"File encryption error: {e}")
            return None
    
    def decrypt_file(self, encrypted_data: str, password: str, output_path: str) -> bool:
        """
        Decrypt a file using the Borg Encryption System.
        
        Args:
            encrypted_data: Encrypted file data
            password: Decryption password
            output_path: Path to save the decrypted file
            
        Returns:
            True if decryption was successful, False otherwise
        """
        try:
            response = self.session.post(
                f"{self.base_url}/decrypt/file",
                json={"encrypted_file_content": encrypted_data, "password": password}
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Decode the base64 decrypted data
            decrypted_data = base64.b64decode(data["decrypted_data"])
            
            # Write the decrypted data to the output file
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            return True
        except Exception as e:
            print(f"File decryption error: {e}")
            return False
    
    def generate_keys(self, master_password: str) -> bool:
        """
        Generate new encryption keys.
        
        Args:
            master_password: Master password for key generation
            
        Returns:
            True if key generation was successful, False otherwise
        """
        try:
            response = self.session.post(
                f"{self.base_url}/keys/generate",
                json={"master_password": master_password}
            )
            response.raise_for_status()
            
            return response.json()["status"] == "success"
        except Exception as e:
            print(f"Key generation error: {e}")
            return False
    
    def rotate_keys(self, master_password: str, force: bool = False) -> Dict[str, Any]:
        """
        Rotate encryption keys.
        
        Args:
            master_password: Master password for key rotation
            force: Force key rotation regardless of the rotation interval
            
        Returns:
            Response data or None if key rotation failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/keys/rotate",
                json={"master_password": master_password, "force": force}
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Key rotation error: {e}")
            return None
    
    def export_public_keys(self, master_password: str) -> Optional[Dict[str, str]]:
        """
        Export public keys.
        
        Args:
            master_password: Master password for key export
            
        Returns:
            Dictionary with public keys or None if export failed
        """
        try:
            response = self.session.post(
                f"{self.base_url}/keys/export",
                json={"master_password": master_password}
            )
            response.raise_for_status()
            
            data = response.json()
            return data["public_keys"]
        except Exception as e:
            print(f"Public key export error: {e}")
            return None
    
    def get_threat_report(self) -> Optional[Dict[str, Any]]:
        """
        Get the current threat report.
        
        Returns:
            Threat report data or None if request failed
        """
        try:
            response = self.session.get(f"{self.base_url}/security/threat-report")
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error getting threat report: {e}")
            return None
    
    def get_security_parameters(self) -> Optional[Dict[str, Any]]:
        """
        Get the current security parameters.
        
        Returns:
            Security parameters or None if request failed
        """
        try:
            response = self.session.get(f"{self.base_url}/security/parameters")
            response.raise_for_status()
            
            return response.json()["security_parameters"]
        except Exception as e:
            print(f"Error getting security parameters: {e}")
            return None


if __name__ == "__main__":
    import sys
    
    # Create client
    client = BorgAPIClient()
    
    # Encrypt a message
    message = "Resistance is futile. Your biological and technological distinctiveness will be added to our own."
    password = "borg-collective"
    
    print(f"\nOriginal message: {message}")
    
    encrypted = client.encrypt_text(message, password)
    if encrypted:
        print(f"\nEncrypted message (truncated):\n{encrypted[:100]}...")
        
        # Decrypt the message
        decrypted = client.decrypt_text(encrypted, password)
        if decrypted:
            print(f"\nDecrypted message:\n{decrypted}")
            
            # Verify the decryption worked correctly
            assert message == decrypted
            print("\nEncryption and decryption successful!")
    
    # Get threat report
    report = client.get_threat_report()
    if report:
        print("\nThreat Report:")
        print(f"Threat Level: {report['threat_level']}")
        print(f"Active Lockouts: {report['active_lockouts']}")
        print(f"Known IPs: {report['known_ips_count']}")
