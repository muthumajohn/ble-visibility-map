from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field

from database import Base

# --- SQLAlchemy ORM Models ---

class BLEDevice(Base):
    """Stores the persistent profile for a unique BLE device (identified by MAC)."""
    __tablename__ = "ble_devices"

    id = Column(Integer, primary_key=True, index=True)
    mac_address = Column(String, unique=True, index=True, nullable=False)
    
    # tagging, notifications
    friendly_name = Column(String, default="")
    is_tagged = Column(Boolean, default=False)
    allow_notifications = Column(Boolean, default=False)

    # Profile/Fingerprinting fields
    vendor = Column(String, default="Unknown")
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, index=True)
    threat_score = Column(Float, default=0.0)
    device_type = Column(String, default="Uncategorized")
    total_detections = Column(Integer, default=1)

class ScanEvent(Base):
    """Stores a single instance of a device being scanned by a gateway (the raw data)."""
    __tablename__ = "scan_events"

    id = Column(Integer, primary_key=True, index=True)
    device_mac = Column(String, index=True, nullable=False) 
    rssi = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    gateway_id = Column(String, default="default_gateway")
    advertisement_data = Column(String, default="") # JSON of raw ADV data

# --- Pydantic Schemas (Data Transfer Objects) ---

class ScanDataIn(BaseModel):
    """Data received by the POST /scans endpoint."""
    mac_address: str = Field(..., description="The MAC address of the scanned device.")
    rssi: int = Field(..., description="The Received Signal Strength Indicator.")
    gateway_id: str = Field("default_gateway", description="Identifier of the scanning gateway.")
    advertisement_data: str = Field("", description="String representation of raw advertisement data ")
    timestamp: datetime = Field(None, description="Optional timestamp of the scan.")

class BLEDeviceOut(BaseModel):
    """Model for outputting the device profile to the frontend."""
    id: int
    mac_address: str
    friendly_name: str
    is_tagged: bool
    allow_notifications: bool
    vendor: str
    first_seen: datetime
    last_seen: datetime
    total_detections: int
    threat_score: float
    device_type: str

    class Config:
        from_attributes = True
