import sys
import os
import json
import httpx
import time
from datetime import datetime
from bluepy.btle import Scanner, DefaultDelegate, BTLEException

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/scans"
# BACKEND_URL = "http://192.168.100.41:8000/scans"
GATEWAY_ID = "python_kali_bluepy_scanner_01" 
SCAN_INTERVAL_SECONDS = 10 
SCAN_DURATION_SECONDS = 8

# A dictionary to store unique devices found in the current scan window
detected_devices = {}

def format_scan_data(device):
    """
    Formats the data from bluepy into the structure expected by the FastAPI backend.
    """
    # Parse advertisement data from bluepy's format
    # The 'adData' is a list of tuples: (type_code, description, value)
    
    adv_data_fields = {}
    for (ad_type, desc, value) in device.getScanData():
        # Example: 0x09 is 'Complete Local Name', 0xFF is 'Manufacturer Specific Data'
        adv_data_fields[desc] = value
        
    adv_data_str = json.dumps({
        "local_name": adv_data_fields.get('Complete Local Name') or adv_data_fields.get('Shortened Local Name', ''),
        "manufacturer_data": adv_data_fields.get('Manufacturer Specific Data', ''),
        "service_uuids": adv_data_fields.get('16b Service Data', ''),
    })

    return {
        "mac_address": device.addr.upper(),
        "rssi": device.rssi,
        "gateway_id": GATEWAY_ID,
        "advertisement_data": adv_data_str,
        "timestamp": datetime.utcnow().isoformat()
    }

class ScanDelegate(DefaultDelegate):
    """Handles discovered devices during the scan."""
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr not in detected_devices:
            data = format_scan_data(dev)
            detected_devices[dev.addr] = data
            # Optionally print for debugging
            # print(f"  -> Found {dev.addr} ({dev.rssi} dBm)")

def scan_and_post():
    """
    Performs a single BLE scan using bluepy, processes the results, and posts to the backend.
    """
    global detected_devices
    detected_devices = {} # Reset for a new scan cycle
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting BLE scan with bluepy...")
    
    try:
        # Initialize the scanner object
        scanner = Scanner().withDelegate(ScanDelegate())
        
        # Start the blocking scan
        scanner.scan(SCAN_DURATION_SECONDS) 

    except BTLEException as e:
        print(f"ERROR: Bluepy BTLEException. Ensure permissions are correct (e.g., setcap). Details: {e}")
        # If running without setcap, you MUST run this script with sudo.
        return
    except Exception as e:
        print(f"An unexpected error occurred during scan: {e}")
        return

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scan finished. Found {len(detected_devices)} unique devices. Posting...")
    
    # Post data to the backend
    try:
        with httpx.Client(timeout=10.0) as client:
            for mac, scan_data in detected_devices.items():
                response = client.post(BACKEND_URL, json=scan_data)
                
                if response.status_code != 201:
                    print(f"ERROR: Failed to post {mac}. Status: {response.status_code}. Response: {response.text}")

    except httpx.RequestError as e:
        print(f"ERROR: HTTP Request failed: {e}")

def main_loop():
    """Runs the scan in a continuous loop."""
    while True:
        scan_and_post()
        print(f"Waiting for {SCAN_INTERVAL_SECONDS} seconds until next scan...")
        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    print("BLE Scanner Simulator (Bluepy) Started.")
    print("NOTE: This script is known to require elevated permissions on Linux.")
    print(f"Posting to: {BACKEND_URL}")
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nScanner stopped by user.")