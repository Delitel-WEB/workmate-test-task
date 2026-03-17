from collections import defaultdict
from statistics import median

from app.loader.models import StudyRecord
from app.reports.base import BaseReport


class MedianCoffee(BaseReport):
    """Отчёт о медианных тратах на кофе."""

    name = "median-coffee"

    def build(self, records: list[StudyRecord]):
        """Формирование отчёта."""
        student_spending = defaultdict(list)
        for record in records:
            student_spending[record.student].append(record.coffee_spent)

        result = []
        for student, coffee_spent in student_spending.items():
            median_value = median(coffee_spent)
            result.append({
                "student": student,
                "median_coffee_spent": median_value
            })

        result.sort(key=lambda x: x["median_coffee_spent"], reverse=True)
        self.results = result

        return result
