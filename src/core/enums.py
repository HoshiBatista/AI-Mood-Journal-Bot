from enum import Enum


class User_Role(str, Enum):
    USER = "user"
    PSYCHOLOGIST = "psychologist"


class Mood_Level(int, Enum):
    VERY_BAD = 1
    BAD = 2
    NEUTRAL = 3
    GOOD = 4
    EXCELLENT = 5


class Trigger_Type(str, Enum):
    WORK = "work"
    RELATIONSHIPS = "relationships"
    HEALTH = "health"
    FINANCE = "finance"
    FAMILY = "family"
    SOCIAL = "social"
    SELF_CARE = "self_care"


class Activity_Type(str, Enum):
    WORK = "work"
    EXERCISE = "exercise"
    SOCIAL = "social"
    HOBBY = "hobby"
    REST = "rest"
    LEARNING = "learning"
    MEDITATION = "meditation"
