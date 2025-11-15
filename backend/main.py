from fastapi import FastAPI
from database import create_db_and_tables
from routers import scans
from routers import tags

# Initialize DB (creates file and tables if they don't exist)
create_db_and_tables()

app = FastAPI(
    title="BLE Visibility Map Backend",
    version="1.0.0",
)

# Include the first router
app.include_router(scans.router)
app.include_router(tags.router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the BLE Visibility Map API. Visit /docs for available endpoints."}

