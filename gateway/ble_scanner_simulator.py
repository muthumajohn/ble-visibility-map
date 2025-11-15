import asyncio
import json
import httpx
from bleak import BleakScanner
from datetime import datetime

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/scans"
GATEWAY_ID = "python_laptop_scanner_01" 
SCAN_INTERVAL_SECONDS = 10 

def format_scan_data(device, advertisement_data):
    """
    Formats the data from bleak into the structure expected by the FastAPI backend.
    """
    # Stringify the key parts of the advertisement data for the backend to parse
    adv_data_str = json.dumps({
        "local_name": advertisement_data.local_name,
        "manufacturer_data": advertisement_data.manufacturer_data, 
        "service_uuids": advertisement_data.service_uuids,
        "tx_power": advertisement_data.tx_power,
    })

    return {
        "mac_address": device.address,
        "rssi": advertisement_data.rssi,
        "gateway_id": GATEWAY_ID,
        "advertisement_data": adv_data_str,
        "timestamp": datetime.utcnow().isoformat()
    }

async def scan_and_post():
    """
    Performs a single BLE scan, processes the results, and posts to the backend.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting BLE scan...")
    
    # scanner = BleakScanner()
    detected_devices = {} 

    def detection_callback(device, advertisement_data):
        # We process each unique device only once per scan cycle
        if device.address not in detected_devices:
            data = format_scan_data(device, advertisement_data)
            detected_devices[device.address] = data
            
    # We also use the 'async with' context manager for cleaner start/stop
    async with BleakScanner(detection_callback=detection_callback) as scanner:
        # The scanner starts immediately upon entering the 'async with' block.
        print("Scanning for 8 seconds...")
        await asyncio.sleep(8) # Scan for 8 seconds
        # The scanner stops automatically upon exiting the 'async with' block.

    
    #scanner.register_detection_callback(detection_callback)
    
    # Run the scan for a short duration
    #await scanner.start()
    #await asyncio.sleep(8) # Scan for 8 seconds
    #await scanner.stop()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scan finished. Found {len(detected_devices)} unique devices. Posting...")
    
    # Post data to the backend
    async with httpx.AsyncClient(timeout=10.0) as client:
        for mac, scan_data in detected_devices.items():
            try:
                response = await client.post(BACKEND_URL, json=scan_data)
                
                if response.status_code != 201:
                    print(f"ERROR: Failed to post {mac}. Status: {response.status_code}. Response: {response.text}")
            except httpx.RequestError as e:
                print(f"ERROR: HTTP Request failed for {mac}: {e}")

async def main_loop():
    """Runs the scan in a continuous loop."""
    while True:
        await scan_and_post()
        print(f"Waiting for {SCAN_INTERVAL_SECONDS} seconds until next scan...")
        await asyncio.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    print("BLE Scanner Simulator Started.")
    print("NOTE: This script requires 'bleak' and may need elevated permissions (e.g., sudo) to access the Bluetooth adapter on Linux/macOS.")
    print(f"Posting to: {BACKEND_URL}")
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nScanner stopped by user.")