from abc import ABC, abstractmethod

from app.loader.models import StudyRecord


REPORTS = {}


class BaseReport(ABC):
    """Базовый класс отчётов."""

    name: str = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.name:
            if cls.name in REPORTS:
                raise ValueError(f"Дублирующий экземпляр: {cls.name}")
            REPORTS[cls.name] = cls

    @abstractmethod
    def build(self, records: list[StudyRecord]) -> None:
        """Метод создания отчёта."""
        ...
