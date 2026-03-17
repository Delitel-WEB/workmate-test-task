from dataclasses import dataclass
from datetime import date


@dataclass
class StudyRecord:
    """Строка в csv файле."""

    student: str
    date: date
    coffee_spent: str
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str
