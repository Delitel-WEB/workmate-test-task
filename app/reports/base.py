from abc import ABC, abstractmethod

from tabulate import tabulate

from app.loader.models import StudyRecord


REPORTS = {}


class BaseReport(ABC):
    """Базовый класс отчётов."""

    name: str = None

    def __init__(self):
        self.results: list[dict] = None

    def __init_subclass__(cls):
        if cls.name:
            if cls.name in REPORTS:
                raise ValueError(f"Дублирующий экземпляр: {cls.name}")
            REPORTS[cls.name] = cls

    @abstractmethod
    def build(self, records: list[StudyRecord]) -> None:
        """Метод создания отчёта."""
        ...

    def print_report(self):
        """Вывод отчёта в консоль."""
        if not self.results:
            return

        print(tabulate(self.results, headers="keys", tablefmt="grid", floatfmt=".2f"))

