import models 
from database import SessionLocal 

async def check_and_notify(db_device: models.BLEDevice, current_rssi: int):
    """
    Checks if a device is tagged for notifications and triggers an alert if needed.
    (Currently prints a console notification, which can be expanded to WebSockets/email later)
    """
    if db_device.allow_notifications:
        # In a real app, this would send a WebSocket message to the frontend, 
        # push notification, or log a high-priority event.
        
        # For now, we'll log it to the backend console:
        message = (
            f"!!! ALERT !!! Tagged device DETECTED: "
            f"MAC={db_device.mac_address} | Name='{db_device.friendly_name}' "
            f"| RSSI={current_rssi} dBm | Risk={db_device.threat_score:.1f}"
        )
        print("\n" + "="*50)
        print(message)
        print("="*50 + "\n")
        
        # We can also save an Event record to the database (which we'll define later)
        # For now, this is a placeholder:
        # await log_event(db_device.mac_address, "REAPPEARANCE_ALERT")
        
        return True
    return False

# Placeholder for future event logging (optional for now)
# async def log_event(mac: str, event_type: str):
#     """Logs an alert event to the database (requires an Event model)."""
#     db = SessionLocal()
#     # ... logic to create Event object ...
#     db.close()