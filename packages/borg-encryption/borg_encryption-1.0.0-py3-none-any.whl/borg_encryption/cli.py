#!/usr/bin/env python3
"""
Borg Encryption System CLI
-------------------------
Command-line interface for the Borg Encryption System.
"""

import os
import sys
import base64
import argparse
from typing import Dict, List, Optional, Any

from .client import BorgAPIClient
from .borg_encryption import BorgEncryption


def main():
    """Main function for the CLI."""
    parser = argparse.ArgumentParser(
        description="Borg Encryption System CLI",
        epilog="Resistance is futile."
    )
    
    # Add arguments
    parser.add_argument("--url", default="http://localhost:8000", help="API URL")
    parser.add_argument("--api-key", default=os.environ.get("API_KEY", "resistance-is-futile"), help="API key")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Encrypt text command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt text")
    encrypt_parser.add_argument("--text", required=True, help="Text to encrypt")
    encrypt_parser.add_argument("--key", required=True, help="Encryption password")
    encrypt_parser.add_argument("--output", help="Output file (optional)")
    encrypt_parser.add_argument("--local", action="store_true", help="Use local encryption instead of API")
    
    # Decrypt text command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt text")
    decrypt_parser.add_argument("--text", help="Text to decrypt")
    decrypt_parser.add_argument("--file", help="File containing text to decrypt")
    decrypt_parser.add_argument("--key", required=True, help="Decryption password")
    decrypt_parser.add_argument("--output", help="Output file (optional)")
    decrypt_parser.add_argument("--local", action="store_true", help="Use local decryption instead of API")
    
    # Encrypt file command
    encrypt_file_parser = subparsers.add_parser("encrypt-file", help="Encrypt a file")
    encrypt_file_parser.add_argument("--file", required=True, help="File to encrypt")
    encrypt_file_parser.add_argument("--key", required=True, help="Encryption password")
    encrypt_file_parser.add_argument("--output", help="Output file (optional)")
    encrypt_file_parser.add_argument("--local", action="store_true", help="Use local encryption instead of API")
    
    # Decrypt file command
    decrypt_file_parser = subparsers.add_parser("decrypt-file", help="Decrypt a file")
    decrypt_file_parser.add_argument("--file", required=True, help="File to decrypt")
    decrypt_file_parser.add_argument("--key", required=True, help="Decryption password")
    decrypt_file_parser.add_argument("--output", required=True, help="Output file")
    decrypt_file_parser.add_argument("--local", action="store_true", help="Use local decryption instead of API")
    
    # Generate keys command
    generate_keys_parser = subparsers.add_parser("generate-keys", help="Generate new encryption keys")
    generate_keys_parser.add_argument("--master-password", required=True, help="Master password")
    
    # Rotate keys command
    rotate_keys_parser = subparsers.add_parser("rotate-keys", help="Rotate encryption keys")
    rotate_keys_parser.add_argument("--master-password", required=True, help="Master password")
    rotate_keys_parser.add_argument("--force", action="store_true", help="Force key rotation")
    
    # Export public keys command
    export_keys_parser = subparsers.add_parser("export-keys", help="Export public keys")
    export_keys_parser.add_argument("--master-password", required=True, help="Master password")
    export_keys_parser.add_argument("--output", help="Output file (optional)")
    
    # Get threat report command
    threat_report_parser = subparsers.add_parser("threat-report", help="Get threat report")
    
    # Get security parameters command
    security_params_parser = subparsers.add_parser("security-params", help="Get security parameters")
    
    # Start API server command
    server_parser = subparsers.add_parser("server", help="Start the API server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    server_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle server command separately
    if args.command == "server":
        from .api import run_server
        run_server(host=args.host, port=args.port, reload=args.reload)
        return
    
    # Create client for API commands
    client = BorgAPIClient(args.url, args.api_key)
    
    # Execute command
    if args.command == "encrypt":
        if args.local:
            # Use local encryption
            borg = BorgEncryption(args.key)
            encrypted = borg.encrypt(args.text, args.key)
        else:
            # Use API
            encrypted = client.encrypt_text(args.text, args.key)
            
        if encrypted:
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(encrypted)
                print(f"Encrypted text saved to {args.output}")
            else:
                print(f"Encrypted text (truncated):\n{encrypted[:100]}...")
        else:
            print("Encryption failed")
    
    elif args.command == "decrypt":
        if args.text:
            encrypted_text = args.text
        elif args.file:
            with open(args.file, 'r') as f:
                encrypted_text = f.read()
        else:
            print("Error: You must specify either --text or --file")
            sys.exit(1)
        
        if args.local:
            # Use local decryption
            borg = BorgEncryption(args.key)
            try:
                decrypted = borg.decrypt_to_string(encrypted_text, args.key)
            except Exception as e:
                print(f"Decryption error: {e}")
                decrypted = None
        else:
            # Use API
            decrypted = client.decrypt_text(encrypted_text, args.key)
            
        if decrypted:
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(decrypted)
                print(f"Decrypted text saved to {args.output}")
            else:
                print(f"Decrypted text:\n{decrypted}")
        else:
            print("Decryption failed")
    
    elif args.command == "encrypt-file":
        if args.local:
            # Use local encryption
            try:
                with open(args.file, 'rb') as f:
                    file_content = f.read()
                
                borg = BorgEncryption(args.key)
                encrypted_data = borg.encrypt(file_content, args.key)
                
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(encrypted_data)
                    print(f"Encrypted file saved to {args.output}")
                else:
                    print(f"Encrypted file data (truncated):\n{encrypted_data[:100]}...")
            except Exception as e:
                print(f"File encryption error: {e}")
        else:
            # Use API
            result = client.encrypt_file(args.file, args.key)
            if result:
                encrypted_data = result["encrypted_data"]
                if args.output:
                    with open(args.output, 'w') as f:
                        f.write(encrypted_data)
                    print(f"Encrypted file saved to {args.output}")
                else:
                    print(f"Encrypted file data (truncated):\n{encrypted_data[:100]}...")
            else:
                print("File encryption failed")
    
    elif args.command == "decrypt-file":
        with open(args.file, 'r') as f:
            encrypted_data = f.read()
        
        if args.local:
            # Use local decryption
            try:
                borg = BorgEncryption(args.key)
                decrypted_data = borg.decrypt(encrypted_data, args.key)
                
                with open(args.output, 'wb') as f:
                    f.write(decrypted_data)
                
                print(f"File decrypted successfully to {args.output}")
            except Exception as e:
                print(f"File decryption error: {e}")
        else:
            # Use API
            success = client.decrypt_file(encrypted_data, args.key, args.output)
            if success:
                print(f"File decrypted successfully to {args.output}")
            else:
                print("File decryption failed")
    
    elif args.command == "generate-keys":
        success = client.generate_keys(args.master_password)
        if success:
            print("Encryption keys generated successfully")
        else:
            print("Key generation failed")
    
    elif args.command == "rotate-keys":
        result = client.rotate_keys(args.master_password, args.force)
        if result:
            if result["status"] == "success":
                print("Encryption keys rotated successfully")
            else:
                print(result["message"])
        else:
            print("Key rotation failed")
    
    elif args.command == "export-keys":
        public_keys = client.export_public_keys(args.master_password)
        if public_keys:
            if args.output:
                import json
                with open(args.output, 'w') as f:
                    json.dump(public_keys, f, indent=2)
                print(f"Public keys exported to {args.output}")
            else:
                print("Public Keys:")
                for key_type, key_value in public_keys.items():
                    print(f"{key_type}: {key_value[:64]}...")
        else:
            print("Public key export failed")
    
    elif args.command == "threat-report":
        report = client.get_threat_report()
        if report:
            print("\nBorg Collective Security Threat Report")
            print("=====================================")
            print(f"Threat Level: {report['threat_level']}")
            print(f"Active Lockouts: {report['active_lockouts']}")
            print(f"Known IPs: {report['known_ips_count']}")
            print("\nAttack Patterns:")
            for pattern, count in report['attack_patterns'].items():
                print(f"  {pattern}: {count}")
            print("\nSecurity Parameters:")
            for param, value in report['security_parameters'].items():
                print(f"  {param}: {value}")
        else:
            print("Failed to get threat report")
    
    elif args.command == "security-params":
        params = client.get_security_parameters()
        if params:
            print("\nBorg Collective Security Parameters")
            print("==================================")
            for param, value in params.items():
                print(f"{param}: {value}")
        else:
            print("Failed to get security parameters")


if __name__ == "__main__":
    main()
