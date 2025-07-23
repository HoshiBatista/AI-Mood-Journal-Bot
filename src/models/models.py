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

class Client(BaseUser):
    __tablename__ = "clients"
    
    alias = Column(String(32), nullable=False)  
    psychologist_id = Column(UUID(as_uuid=True), ForeignKey('psychologists.id'))
    
    psychologist = relationship("Psychologist", back_populates="clients")
    mood_entries = relationship("MoodEntry", back_populates="client")
    feedbacks = relationship("PsychologistFeedback", back_populates="client")

class Psychologist(BaseUser):
    __tablename__ = "psychologists"
    
    qualification = Column(String(128), nullable=False)
    specialization = Column(String(128))
    license_number = Column(String(32))
    experience_years = Column(Integer)
    
    clients = relationship("Client", back_populates="psychologist")
    feedbacks = relationship("PsychologistFeedback", back_populates="psychologist")
    
class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'), nullable=False)
    date = Column(DateTime, default=datetime.now)
    mood_level = Column(Enum(MoodLevel), nullable=False)
    note = Column(Text)
    analyzed = Column(Boolean, default=False)
    
    client = relationship("Client", back_populates="mood_entries")
    triggers = relationship("EntryTrigger", back_populates="entry")
    activities = relationship("EntryActivity", back_populates="entry")
    analysis = relationship("EmotionAnalysis", back_populates="entry", uselist=False)
    feedbacks = relationship("PsychologistFeedback", back_populates="entry")