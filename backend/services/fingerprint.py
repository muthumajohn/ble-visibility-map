def analyze_ble_scan(scan_data: dict) -> dict:
    """
    Analyzes raw BLE scan data (RSSI, MAC, adv_data) to determine
    vendor, device type, and an initial threat score.
    """
    mac = scan_data.get('mac_address', '00:00:00:00:00:00')
    adv_data = scan_data.get('advertisement_data', '')
    
    # Vendor Lookup (based on OUI - first 3 bytes of MAC)
    oui = mac[:8].replace(':', '').upper()
    
    vendor_db = {
        "D4A651": "Apple", 
        "54A6B1": "Xiaomi",
    }
    
    vendor = vendor_db.get(oui, "Unknown")
    
    # Device Type & Initial Threat Scoring Logic
    device_type = "Uncategorized"
    threat_score = 0.0 # Scale of 0.0 (safe) to 1.0 (high risk)

    if vendor == "Apple" and 'service_uuids' in adv_data: 
        # More complex logic for Apple devices like AirTags or iPhones...
        device_type = "Apple iDevice/Tracker"
        threat_score = 0.4
    elif vendor == "Unknown":
        threat_score = 0.6 # Elevated risk for entirely unknown devices

    return {
        "vendor": vendor,
        "device_type": device_type,
        "threat_score": threat_score,
    }