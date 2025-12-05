from sqlalchemy.orm import Session
from datetime import datetime
import models 
from database import SessionLocal 

def log_event(db: Session, mac: str, event_type: str, message: str, risk_score: float):
    """Logs an alert event to the database and returns the new event object."""
    db_event = models.Event(
        device_mac=mac,
        event_type=event_type,
        message=message,
        timestamp=datetime.utcnow(),
        risk_score=risk_score
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def check_and_notify(db: Session, db_device: models.BLEDevice, current_rssi: int):
    """
    Checks if a device is tagged for notifications and triggers an alert 
    by logging an Event to the database.
    """
    if db_device.allow_notifications:
        message = (
            f"Tagged device '{db_device.friendly_name}' reappeared. "
            f"Signal strength: {current_rssi} dBm. "
            f"Vendor: {db_device.vendor}."
        )
        
        log_event(
            db=db,
            mac=db_device.mac_address,
            event_type="REAPPEARANCE_ALERT",
            message=message,
            risk_score=db_device.threat_score
        )
        # Note: In a production app, this is where you'd also send a WebSocket
        # message to the frontend for real-time update *after* logging to the DB.
        
        return True
    return False