from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class PowerDataRecord(Base):
    """Model for storing power data records"""
    __tablename__ = "power_data_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    raw_data = Column(Text)  # Store full JSON response
    result_code = Column(String)
    result_msg = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "result_code": self.result_code,
            "result_msg": self.result_msg,
            "data": json.loads(self.raw_data) if self.raw_data else None
        }


# Create database engine
DATABASE_URL = "sqlite:///./power_data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_power_data(data: dict):
    """Save power data to database"""
    db = SessionLocal()
    try:
        record = PowerDataRecord(
            raw_data=json.dumps(data),
            result_code=data.get("result_code", "0"),
            result_msg=data.get("result_msg")
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def get_latest_power_data():
    """Get the most recent power data record"""
    db = SessionLocal()
    try:
        record = db.query(PowerDataRecord).order_by(PowerDataRecord.timestamp.desc()).first()
        return record.to_dict() if record else None
    finally:
        db.close()


def get_all_power_data(limit: int = 100):
    """Get all power data records with optional limit"""
    db = SessionLocal()
    try:
        records = db.query(PowerDataRecord).order_by(PowerDataRecord.timestamp.desc()).limit(limit).all()
        return [record.to_dict() for record in records]
    finally:
        db.close()

