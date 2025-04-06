#!/usr/bin/env python3
"""
Borg Adaptive Defense System
---------------------------
Monitors and responds to attempted breaches of the Borg Encryption System.
Implements adaptive security measures to strengthen the system against attacks.
"""

import os
import time
import json
import base64
import hashlib
import logging
from typing import Dict, List, Tuple, Optional, Any, Union
from collections import defaultdict, Counter
import threading
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='borg_defense.log'
)
logger = logging.getLogger('borg_defense')

# Constants
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 30 * 60  # 30 minutes in seconds
THREAT_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
DEFENSE_LOG_FILE = "borg_defense_data.json"


class AdaptiveDefense:
    """
    Implements adaptive security measures for the Borg Encryption System.
    Monitors for attacks and adapts security parameters accordingly.
    """
    
    def __init__(self):
        """Initialize the adaptive defense system."""
        self.failed_attempts = defaultdict(int)
        self.lockouts = {}
        self.threat_level = "LOW"
        self.attack_patterns = Counter()
        self.defense_data = self._load_defense_data() or {
            "known_ips": {},
            "attack_patterns": {},
            "security_parameters": {
                "iterations": 1_000_000,
                "memory_cost": 2**20,
                "encryption_layers": 3
            },
            "threat_history": []
        }
        
        # Start the monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._security_monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _load_defense_data(self) -> Optional[Dict[str, Any]]:
        """
        Load defense data from the storage file.
        
        Returns:
            Dictionary containing the defense data, or None if the file doesn't exist
        """
        if not os.path.exists(DEFENSE_LOG_FILE):
            return None
        
        try:
            with open(DEFENSE_LOG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading defense data: {e}")
            return None
    
    def _save_defense_data(self) -> None:
        """Save the defense data to the storage file."""
        try:
            with open(DEFENSE_LOG_FILE, 'w') as f:
                json.dump(self.defense_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving defense data: {e}")
    
    def _security_monitor(self) -> None:
        """
        Background thread that monitors security and adapts parameters.
        """
        while self.monitoring_active:
            try:
                # Check for expired lockouts
                current_time = time.time()
                expired_lockouts = []
                
                for ip, lockout_time in self.lockouts.items():
                    if current_time - lockout_time > LOCKOUT_DURATION:
                        expired_lockouts.append(ip)
                
                for ip in expired_lockouts:
                    self.lockouts.pop(ip)
                    self.failed_attempts[ip] = 0
                    logger.info(f"Lockout expired for {ip}")
                
                # Analyze attack patterns and adjust security parameters
                self._analyze_threats()
                
                # Save defense data periodically
                self._save_defense_data()
                
                # Sleep for a random interval to make timing attacks harder
                time.sleep(random.uniform(55, 65))
            except Exception as e:
                logger.error(f"Error in security monitor: {e}")
                time.sleep(60)
    
    def _analyze_threats(self) -> None:
        """
        Analyze attack patterns and adjust security parameters.
        """
        # Count active lockouts
        active_lockouts = len(self.lockouts)
        
        # Determine threat level based on lockouts and attack patterns
        if active_lockouts >= 10 or any(count >= 20 for count in self.attack_patterns.values()):
            new_threat_level = "CRITICAL"
        elif active_lockouts >= 5 or any(count >= 10 for count in self.attack_patterns.values()):
            new_threat_level = "HIGH"
        elif active_lockouts >= 2 or any(count >= 5 for count in self.attack_patterns.values()):
            new_threat_level = "MEDIUM"
        else:
            new_threat_level = "LOW"
        
        # If threat level changed, update security parameters
        if new_threat_level != self.threat_level:
            self.threat_level = new_threat_level
            logger.warning(f"Threat level changed to {self.threat_level}")
            
            # Record the threat level change
            self.defense_data["threat_history"].append({
                "timestamp": int(time.time()),
                "threat_level": self.threat_level,
                "active_lockouts": active_lockouts,
                "attack_patterns": dict(self.attack_patterns)
            })
            
            # Limit history to last 100 entries
            if len(self.defense_data["threat_history"]) > 100:
                self.defense_data["threat_history"] = self.defense_data["threat_history"][-100:]
            
            # Adjust security parameters based on threat level
            self._adjust_security_parameters()
    
    def _adjust_security_parameters(self) -> None:
        """
        Adjust security parameters based on the current threat level.
        """
        params = self.defense_data["security_parameters"]
        
        if self.threat_level == "CRITICAL":
            params["iterations"] = 2_000_000
            params["memory_cost"] = 2**22  # 4 MB
            params["encryption_layers"] = 5
        elif self.threat_level == "HIGH":
            params["iterations"] = 1_500_000
            params["memory_cost"] = 2**21  # 2 MB
            params["encryption_layers"] = 4
        elif self.threat_level == "MEDIUM":
            params["iterations"] = 1_200_000
            params["memory_cost"] = 2**20  # 1 MB
            params["encryption_layers"] = 3
        else:  # LOW
            params["iterations"] = 1_000_000
            params["memory_cost"] = 2**20  # 1 MB
            params["encryption_layers"] = 3
        
        logger.info(f"Security parameters adjusted: {params}")
    
    def record_access_attempt(self, ip_address: str, success: bool, 
                             username: Optional[str] = None, 
                             attack_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Record an access attempt and check if it should be blocked.
        
        Args:
            ip_address: IP address of the attempt
            success: Whether the attempt was successful
            username: Optional username associated with the attempt
            attack_type: Optional type of attack detected
            
        Returns:
            Dictionary with status information
        """
        current_time = time.time()
        
        # Check if IP is locked out
        if ip_address in self.lockouts:
            lockout_time = self.lockouts[ip_address]
            remaining_time = int(LOCKOUT_DURATION - (current_time - lockout_time))
            
            if remaining_time > 0:
                logger.warning(f"Blocked attempt from locked out IP: {ip_address}")
                return {
                    "status": "blocked",
                    "reason": "ip_lockout",
                    "remaining_lockout_time": remaining_time
                }
        
        # Record the attempt
        if not success:
            self.failed_attempts[ip_address] += 1
            
            if attack_type:
                self.attack_patterns[attack_type] += 1
            
            # Check if we should lock out the IP
            if self.failed_attempts[ip_address] >= MAX_FAILED_ATTEMPTS:
                self.lockouts[ip_address] = current_time
                logger.warning(f"IP address locked out due to too many failed attempts: {ip_address}")
                return {
                    "status": "blocked",
                    "reason": "too_many_failures",
                    "lockout_duration": LOCKOUT_DURATION
                }
        else:
            # Reset failed attempts on success
            self.failed_attempts[ip_address] = 0
        
        # Update known IPs
        if ip_address not in self.defense_data["known_ips"]:
            self.defense_data["known_ips"][ip_address] = {
                "first_seen": int(current_time),
                "successful_attempts": 0,
                "failed_attempts": 0,
                "last_seen": int(current_time)
            }
        
        ip_data = self.defense_data["known_ips"][ip_address]
        ip_data["last_seen"] = int(current_time)
        
        if success:
            ip_data["successful_attempts"] += 1
        else:
            ip_data["failed_attempts"] += 1
        
        # Update attack patterns
        if attack_type:
            if attack_type not in self.defense_data["attack_patterns"]:
                self.defense_data["attack_patterns"][attack_type] = 0
            self.defense_data["attack_patterns"][attack_type] += 1
        
        return {
            "status": "allowed",
            "threat_level": self.threat_level,
            "failed_attempts": self.failed_attempts[ip_address]
        }
    
    def get_security_parameters(self) -> Dict[str, Any]:
        """
        Get the current security parameters.
        
        Returns:
            Dictionary containing the security parameters
        """
        return self.defense_data["security_parameters"]
    
    def get_threat_report(self) -> Dict[str, Any]:
        """
        Generate a report of the current threat landscape.
        
        Returns:
            Dictionary containing threat information
        """
        return {
            "threat_level": self.threat_level,
            "active_lockouts": len(self.lockouts),
            "attack_patterns": dict(self.attack_patterns),
            "security_parameters": self.defense_data["security_parameters"],
            "known_ips_count": len(self.defense_data["known_ips"]),
            "recent_threats": self.defense_data["threat_history"][-5:] if self.defense_data["threat_history"] else []
        }
    
    def shutdown(self) -> None:
        """Shutdown the defense system cleanly."""
        self.monitoring_active = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        self._save_defense_data()


if __name__ == "__main__":
    defense = AdaptiveDefense()
    
    # Simulate some access attempts
    print("Simulating access attempts...")
    
    # Successful attempt
    result = defense.record_access_attempt("192.168.1.1", True)
    print(f"Successful attempt: {result}")
    
    # Failed attempts
    for i in range(6):
        result = defense.record_access_attempt("192.168.1.2", False, attack_type="password_guessing")
        print(f"Failed attempt {i+1}: {result}")
    
    # Try again with locked out IP
    result = defense.record_access_attempt("192.168.1.2", True)
    print(f"Attempt from locked out IP: {result}")
    
    # Get threat report
    report = defense.get_threat_report()
    print("\nThreat Report:")
    print(json.dumps(report, indent=2))
    
    # Clean shutdown
    defense.shutdown()
