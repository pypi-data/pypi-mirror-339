#!/usr/bin/env python3
"""
Borg Encryption System API
-------------------------
A REST API for the Borg Encryption System with minimal dependencies.
"""

import os
import time
import base64
import secrets
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from contextlib import asynccontextmanager

from .borg_encryption import BorgEncryption
from .key_manager import KeyManager
from .adaptive_defense import AdaptiveDefense

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='borg_api.log'
)
logger = logging.getLogger('borg_api')

# Define lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the adaptive defense system
    app.state.defense = AdaptiveDefense()
    logger.info("API starting, defense system initialized")
    yield
    # Shutdown: clean up resources
    app.state.defense.shutdown()
    logger.info("API shutting down, defense system stopped")

# Initialize the FastAPI app
app = FastAPI(
    title="Borg Encryption System API",
    description="API for the Borg Encryption System - Resistance is futile.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key authentication
API_KEY = os.environ.get("API_KEY", "resistance-is-futile")
api_key_header = APIKeyHeader(name="X-API-Key")

# ----- Pydantic Models -----

class EncryptRequest(BaseModel):
    data: str
    password: str

class EncryptFileRequest(BaseModel):
    file_content: str  # Base64 encoded file content
    password: str
    filename: Optional[str] = None

class DecryptRequest(BaseModel):
    encrypted_data: str
    password: str

class DecryptFileRequest(BaseModel):
    encrypted_file_content: str  # Base64 encoded encrypted file content
    password: str

class KeyGenerationRequest(BaseModel):
    master_password: str

class KeyRotationRequest(BaseModel):
    master_password: str
    force: bool = False

class PublicKeysExportRequest(BaseModel):
    master_password: str

class SecurityReport(BaseModel):
    threat_level: str
    active_lockouts: int
    attack_patterns: Dict[str, int]
    security_parameters: Dict[str, Any]
    known_ips_count: int
    recent_threats: List[Dict[str, Any]]

# ----- Security Functions -----

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify the API key."""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key

# ----- Middleware -----

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and record access attempts."""
    start_time = time.time()
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Process the request
    response = await call_next(request)
    
    # Record the access attempt
    success = response.status_code < 400
    if not success and response.status_code == 401:
        attack_type = "authentication_failure"
    elif not success and response.status_code == 403:
        attack_type = "authorization_failure"
    elif not success:
        attack_type = "api_error"
    else:
        attack_type = None
    
    request.app.state.defense.record_access_attempt(client_ip, success, attack_type=attack_type)
    
    # Log the request
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} {response.status_code} "
        f"Client: {client_ip} Time: {process_time:.3f}s"
    )
    
    return response

# ----- Encryption Endpoints -----

@app.post("/encrypt", tags=["encryption"])
async def encrypt_data(request: EncryptRequest, api_key: str = Depends(verify_api_key)):
    """Encrypt data using the Borg Encryption System."""
    try:
        # Create encryption object
        borg = BorgEncryption(request.password)
        
        # Encrypt the data
        encrypted = borg.encrypt(request.data, request.password)
        
        return {"encrypted_data": encrypted}
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        raise HTTPException(status_code=500, detail=f"Encryption error: {str(e)}")

@app.post("/encrypt/file", tags=["encryption"])
async def encrypt_file(request: EncryptFileRequest, api_key: str = Depends(verify_api_key)):
    """Encrypt a file using the Borg Encryption System."""
    try:
        # Decode the base64 file content
        file_content = base64.b64decode(request.file_content)
        
        # Create encryption object
        borg = BorgEncryption(request.password)
        
        # Encrypt the file
        encrypted = borg.encrypt(file_content, request.password)
        
        return {"encrypted_data": encrypted, "filename": request.filename}
    except Exception as e:
        logger.error(f"Error encrypting file: {e}")
        raise HTTPException(status_code=500, detail=f"File encryption error: {str(e)}")

@app.post("/decrypt", tags=["encryption"])
async def decrypt_data(request: DecryptRequest, api_key: str = Depends(verify_api_key)):
    """Decrypt data using the Borg Encryption System."""
    try:
        # Create encryption object
        borg = BorgEncryption(request.password)
        
        # Decrypt the data
        decrypted = borg.decrypt_to_string(request.encrypted_data, request.password)
        
        return {"decrypted_data": decrypted}
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        raise HTTPException(status_code=500, detail=f"Decryption error: {str(e)}")

@app.post("/decrypt/file", tags=["encryption"])
async def decrypt_file(request: DecryptFileRequest, api_key: str = Depends(verify_api_key)):
    """Decrypt a file using the Borg Encryption System."""
    try:
        # Create encryption object
        borg = BorgEncryption(request.password)
        
        # Decrypt the file
        decrypted = borg.decrypt(request.encrypted_file_content, request.password)
        
        # Encode the decrypted content as base64
        decrypted_base64 = base64.b64encode(decrypted).decode('utf-8')
        
        return {"decrypted_data": decrypted_base64}
    except Exception as e:
        logger.error(f"Error decrypting file: {e}")
        raise HTTPException(status_code=500, detail=f"File decryption error: {str(e)}")

# ----- Key Management Endpoints -----

@app.post("/keys/generate", tags=["key-management"])
async def generate_keys(request: KeyGenerationRequest, api_key: str = Depends(verify_api_key)):
    """Generate new encryption keys."""
    try:
        # Create key manager
        KeyManager(request.master_password)
        
        return {"status": "success", "message": "Encryption keys generated successfully"}
    except Exception as e:
        logger.error(f"Error generating keys: {e}")
        raise HTTPException(status_code=500, detail=f"Key generation error: {str(e)}")

@app.post("/keys/rotate", tags=["key-management"])
async def rotate_keys(request: KeyRotationRequest, api_key: str = Depends(verify_api_key)):
    """Rotate encryption keys."""
    try:
        # Create key manager
        manager = KeyManager(request.master_password)
        
        # Rotate keys
        rotated = manager.rotate_keys(force=request.force)
        
        if rotated:
            return {"status": "success", "message": "Encryption keys rotated successfully"}
        else:
            return {
                "status": "not_rotated", 
                "message": "Keys not rotated. Use force=true to rotate before the scheduled rotation."
            }
    except Exception as e:
        logger.error(f"Error rotating keys: {e}")
        raise HTTPException(status_code=500, detail=f"Key rotation error: {str(e)}")

@app.post("/keys/export", tags=["key-management"])
async def export_public_keys(request: PublicKeysExportRequest, api_key: str = Depends(verify_api_key)):
    """Export public keys."""
    try:
        # Create key manager
        manager = KeyManager(request.master_password)
        
        # Export public keys
        public_keys = manager.export_public_keys()
        
        return {"public_keys": public_keys}
    except Exception as e:
        logger.error(f"Error exporting public keys: {e}")
        raise HTTPException(status_code=500, detail=f"Public key export error: {str(e)}")

# ----- Security Endpoints -----

@app.get("/security/threat-report", response_model=SecurityReport, tags=["security"])
async def get_threat_report(api_key: str = Depends(verify_api_key)):
    """Get the current threat report."""
    try:
        # Get threat report
        report = app.state.defense.get_threat_report()
        
        return report
    except Exception as e:
        logger.error(f"Error getting threat report: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting threat report: {str(e)}")

@app.get("/security/parameters", tags=["security"])
async def get_security_parameters(api_key: str = Depends(verify_api_key)):
    """Get the current security parameters."""
    try:
        # Get security parameters
        params = app.state.defense.get_security_parameters()
        
        return {"security_parameters": params}
    except Exception as e:
        logger.error(f"Error getting security parameters: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting security parameters: {str(e)}")

# ----- Health Check Endpoint -----

@app.get("/health", tags=["system"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": time.time()}

# Function to run the API server
def run_server(host="0.0.0.0", port=8000, reload=False):
    """Run the API server."""
    uvicorn.run("borg_encryption.api:app", host=host, port=port, reload=reload)

if __name__ == "__main__":
    run_server(reload=True)
