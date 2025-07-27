from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    JSON,
    Boolean,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from core.enums import MoodLevel, TriggerType, ActivityType

Base = declarative_base()


class BaseUser(Base):
    """
    @brief Базовый класс для пользователей системы
    @details Содержит общие поля для клиентов и психологов
    @var id UUID - уникальный идентификатор пользователя
    @var telegram_id Integer - ID пользователя в Telegram
    @var first_name String - имя пользователя
    @var last_name String - фамилия пользователя
    @var phone String - номер телефона
    @var created_at DateTime - дата регистрации
    @var is_active Boolean - флаг активности аккаунта
    """

    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(Integer, unique=True, nullable=False)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    phone = Column(String(12), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)


class Client(BaseUser):
    """
    @brief Модель клиента (пользователя)
    @var alias String - сгенерированный псевдоним для анонимности
    @var psychologist_id UUID - ссылка на прикрепленного психолога
    @relationship psychologist - связь с психологом
    @relationship mood_entries - записи настроения клиента
    @relationship feedbacks - отзывы психолога для клиента
    """

    __tablename__ = "clients"

    alias = Column(String(32), nullable=False)
    psychologist_id = Column(UUID(as_uuid=True), ForeignKey("psychologists.id"))

    psychologist = relationship("Psychologist", back_populates="clients")
    mood_entries = relationship("MoodEntry", back_populates="client")
    feedbacks = relationship("PsychologistFeedback", back_populates="client")


class Psychologist(BaseUser):
    """
    @brief Модель психолога
    @var qualification String - квалификация/образование
    @var specialization String - специализация
    @var license_number String - номер лицензии
    @var experience_years Integer - опыт работы (лет)
    @relationship clients - клиенты психолога
    @relationship feedbacks - оставленные отзывы
    """

    __tablename__ = "psychologists"

    qualification = Column(String(128), nullable=False)
    specialization = Column(String(128))
    license_number = Column(String(32))
    experience_years = Column(Integer)

    clients = relationship("Client", back_populates="psychologist")
    feedbacks = relationship("PsychologistFeedback", back_populates="psychologist")


class MoodEntry(Base):
    """
    @brief Запись о настроении пользователя
    @var client_id UUID - ссылка на клиента
    @var date DateTime - дата записи
    @var mood_level Enum - уровень настроения (1-5)
    @var note Text - текстовое описание дня
    @var analyzed Boolean - флаг проведения AI-анализа
    @relationship client - связь с клиентом
    @relationship triggers - триггеры для этой записи
    @relationship activities - активности для этой записи
    @relationship analysis - результаты AI-анализа
    @relationship feedbacks - отзывы психолога
    """

    __tablename__ = "mood_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    date = Column(DateTime, default=datetime.now)
    mood_level = Column(Enum(MoodLevel), nullable=False)
    note = Column(Text)
    analyzed = Column(Boolean, default=False)

    client = relationship("Client", back_populates="mood_entries")
    triggers = relationship("EntryTrigger", back_populates="entry")
    activities = relationship("EntryActivity", back_populates="entry")
    analysis = relationship("EmotionAnalysis", back_populates="entry", uselist=False)
    feedbacks = relationship("PsychologistFeedback", back_populates="entry")


class EntryTrigger(Base):
    """
    @brief Триггер для записи настроения
    @var entry_id UUID - ссылка на запись настроения
    @var trigger_type Enum - тип триггера
    @var intensity Integer - интенсивность воздействия (1-5)
    @relationship entry - связь с основной записью
    """

    __tablename__ = "entry_triggers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("mood_entries.id"), nullable=False)
    trigger_type = Column(Enum(TriggerType), nullable=False)
    intensity = Column(Integer)

    entry = relationship("MoodEntry", back_populates="triggers")


class EntryActivity(Base):
    """
    @brief Активность для записи настроения
    @var entry_id UUID - ссылка на запись настроения
    @var activity_type Enum - тип активности
    @var duration Integer - продолжительность в минутах
    @relationship entry - связь с основной записью
    """

    __tablename__ = "entry_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("mood_entries.id"), nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    duration = Column(Integer)

    entry = relationship("MoodEntry", back_populates="activities")


class EmotionAnalysis(Base):
    """
    @brief Результаты AI-анализа записи
    @var entry_id UUID - ссылка на запись настроения
    @var emotions JSON - эмоции и их confidence score
    @var summary Text - текстовое резюме анализа
    @var insights JSON - ключевые инсайты
    @var model_version String - версия модели анализа
    @var created_at DateTime - дата создания анализа
    @relationship entry - связь с основной записью
    """

    __tablename__ = "emotion_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("mood_entries.id"), nullable=False)
    emotions = Column(JSON)
    summary = Column(Text)
    insights = Column(JSON)
    model_version = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    entry = relationship("MoodEntry", back_populates="analysis")


class PsychologistFeedback(Base):
    """
    @brief Отзыв психолога на запись клиента
    @var entry_id UUID - ссылка на запись настроения
    @var psychologist_id UUID - ссылка на психолога
    @var client_id UUID - ссылка на клиента
    @var feedback_text Text - текст отзыва
    @var created_at DateTime - дата создания отзыва
    @var is_read Boolean - флаг прочтения отзыва клиентом
    @relationship entry - связь с записью настроения
    @relationship psychologist - связь с психологом
    @relationship client - связь с клиентом
    """

    __tablename__ = "psychologist_feedbacks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("mood_entries.id"), nullable=False)
    psychologist_id = Column(
        UUID(as_uuid=True), ForeignKey("psychologists.id"), nullable=False
    )
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    feedback_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

    entry = relationship("MoodEntry", back_populates="feedbacks")
    psychologist = relationship("Psychologist", back_populates="feedbacks")
    client = relationship("Client", back_populates="feedbacks")
