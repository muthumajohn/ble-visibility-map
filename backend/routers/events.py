from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from database import get_db
import models
from models import EventOut, EventIn

router = APIRouter(
    prefix="/events",
    tags=["events"],
)

@router.get("/", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db), limit: int = 100):
    """List the most recent system events/alerts."""
    # Order by timestamp descending (most recent first)
    events = db.query(models.Event).order_by(desc(models.Event.timestamp)).limit(limit).all()
    return events

@router.post("/", response_model=EventOut)
def create_event(event_in: EventIn, db: Session = Depends(get_db)):
    """Allow internal or manual logging of a new event."""
    db_event = models.Event(
        device_mac=event_in.device_mac,
        event_type=event_in.event_type,
        message=event_in.message,
        risk_score=event_in.risk_score
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event