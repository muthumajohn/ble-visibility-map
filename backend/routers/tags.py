from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

class TagUpdateIn(models.BaseModel):
    friendly_name: str
    allow_notifications: bool
    
@router.post("/{mac_address}", response_model=models.BLEDeviceOut)
def update_device_tag(mac_address: str, tag_update: TagUpdateIn, db: Session = Depends(get_db)):
    """Add or update a friendly name and set notification preference."""
    db_device = db.query(models.BLEDevice).filter(models.BLEDevice.mac_address == mac_address.upper()).first()
    
    if not db_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    db_device.friendly_name = tag_update.friendly_name
    db_device.allow_notifications = tag_update.allow_notifications
    db_device.is_tagged = True if tag_update.friendly_name else False # Simplified tag logic

    db.commit()
    db.refresh(db_device)
    return db_device