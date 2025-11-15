from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime

import models
from database import get_db
from models import ScanDataIn, BLEDeviceOut
from services.fingerprint import analyze_ble_scan
from services.notifier import check_and_notify 

router = APIRouter(
    prefix="/scans",
    tags=["scans"],
)

def _update_device_profile(db: Session, mac_address: str, fingerprint_data: dict, is_new_device: bool):
    """Helper to create or update the persistent device profile."""
    current_time = datetime.utcnow()
    
    if is_new_device:
        db_device = models.BLEDevice(
            mac_address=mac_address,
            first_seen=current_time,
            last_seen=current_time,
            vendor=fingerprint_data['vendor'],
            device_type=fingerprint_data['device_type'],
            threat_score=fingerprint_data['threat_score'],
            total_detections=1
        )
        db.add(db_device)
    else:
        db_device = db.query(models.BLEDevice).filter(models.BLEDevice.mac_address == mac_address).first()
        if db_device:
            db_device.last_seen = current_time
            db_device.total_detections += 1
            # Update fingerprint data only if the device was previously unknown
            if db_device.vendor == "Unknown":
                 db_device.vendor = fingerprint_data['vendor']
                 db_device.device_type = fingerprint_data['device_type']
                 db_device.threat_score = fingerprint_data['threat_score']
                 
    db.commit()
    db.refresh(db_device)
    return db_device


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BLEDeviceOut)
async def submit_scan_event(scan_in: ScanDataIn, db: Session = Depends(get_db)):
    """
    Receives a new BLE scan event, stores the raw event, 
    and updates the device's persistent profile.
    """
    mac_address = scan_in.mac_address.upper()
    current_time = scan_in.timestamp if scan_in.timestamp else datetime.utcnow()

    # Store the raw scan event
    db_scan = models.ScanEvent(
        device_mac=mac_address,
        rssi=scan_in.rssi,
        gateway_id=scan_in.gateway_id,
        advertisement_data=scan_in.advertisement_data,
        timestamp=current_time,
    )
    db.add(db_scan)

    # Check existence & Fingerprint
    device_exists = db.query(models.BLEDevice).filter(models.BLEDevice.mac_address == mac_address).first()
    is_new_device = device_exists is None
    fingerprint_data = analyze_ble_scan(scan_in.dict())
    
    # Create/Update the persistent BLEDevice profile
    db_device = _update_device_profile(db, mac_address, fingerprint_data, is_new_device)
    
    await check_and_notify(db_device, scan_in.rssi)
    
    return db_device
    
  