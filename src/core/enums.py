
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    PSYCHOLOGIST = "psychologist"
    
class MoodLevel(int, Enum):
    VERY_BAD = 1
    BAD = 2
    NEUTRAL = 3
    GOOD = 4
    EXCELLENT = 5
    
class TriggerType(str, Enum):
    WORK = "work"
    RELATIONSHIPS = "relationships"
    HEALTH = "health"
    FINANCE = "finance"
    FAMILY = "family"
    SOCIAL = "social"
    SELF_CARE = "self_care"