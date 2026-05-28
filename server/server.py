from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

#database file name
SQLALCHEMY_DATABASE_URL = "sqlite:///./sensor_data.db"

#the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#session maker to talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base class to build tables off of
Base = declarative_base()

#Actual database table
class SensorDataDB(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    temperature = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

#Create the table
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sensor API", version="1.0")

class SensorReading(BaseModel):
    sensor_id: str
    temperature: float
    status: str


#helper to open/close database connection for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/sensors/data")
async def receive_sensor_data(reading: SensorReading, db: Session = Depends(get_db)):

    #package the incoming data to database model
    new_record = SensorDataDB(
        sensor_id=reading.sensor_id,
        temperature=reading.temperature,
        status=reading.status
    )

    #Save to db
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    print(f"Saved Record #{new_record.id}: {reading.sensor_id} -> {reading.temperature}*C")


    return {"message": "Data saved permanently", "database_id": new_record.id}


@app.get("/api/v1/sensors/data")
async def get_all_sensor_data(db: Session = Depends(get_db)):

    records = db.query(SensorDataDB).all()

    return {"total_records": len(records), "data": records}
