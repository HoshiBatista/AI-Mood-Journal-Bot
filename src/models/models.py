from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, Text, JSON, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from core.enums import UserRole, MoodLevel, TriggerType, ActivityType

Base = declarative_base()

class BaseUser(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    phone = Column(String(12), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    