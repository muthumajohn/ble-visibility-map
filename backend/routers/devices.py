from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
from models import BLEDeviceOut, ScanDataIn 

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

@router.get("/", response_model=List[BLEDeviceOut])
def list_devices(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """List all unique BLE devices in the database."""
    devices = db.query(models.BLEDevice).offset(skip).limit(limit).all()
    return devices

@router.get("/{mac_address}/history", response_model=List[models.ScanEvent]) 
def get_device_history(mac_address: str, db: Session = Depends(get_db), limit: int = 100):
    """Get the scan history (signal trend) for a specific device."""
    mac = mac_address.upper()
    history = db.query(models.ScanEvent).filter(models.ScanEvent.device_mac == mac).limit(limit).all()
    
    if not history:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device history not found")
         
    return history