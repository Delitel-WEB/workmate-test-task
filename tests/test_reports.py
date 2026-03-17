from datetime import date

import pytest

from app.loader.models import StudyRecord
from app.reports.base import REPORTS
from app.reports.median_coffee import MedianCoffee


class TestMedianCoffeeReport:
    """Тесты для отчёта о медианных тратах на кофе."""

    @pytest.fixture
    def sample_records(self):
        return [
            StudyRecord(
                student="Иван Кузнецов",
                date=date(2024, 6, 1),
                coffee_spent=600,
                sleep_hours=3.0,
                study_hours=15,
                mood="зомби",
                exam="Математика"
            ),
            StudyRecord(
                student="Иван Кузнецов",
                date=date(2024, 6, 2),
                coffee_spent=650,
                sleep_hours=2.5,
                study_hours=17,
                mood="зомби",
                exam="Математика"
            ),
            StudyRecord(
                student="Иван Кузнецов",
                date=date(2024, 6, 3),
                coffee_spent=700,
                sleep_hours=2.0,
                study_hours=18,
                mood="не выжил",
                exam="Математика"
            ),
            StudyRecord(
                student="Алексей Смирнов",
                date=date(2024, 6, 1),
                coffee_spent=450,
                sleep_hours=4.5,
                study_hours=12,
                mood="норм",
                exam="Математика"
            ),
            StudyRecord(
                student="Алексей Смирнов",
                date=date(2024, 6, 2),
                coffee_spent=500,
                sleep_hours=4.0,
                study_hours=14,
                mood="устал",
                exam="Математика"
            ),
            StudyRecord(
                student="Алексей Смирнов",
                date=date(2024, 6, 3),
                coffee_spent=550,
                sleep_hours=3.5,
                study_hours=16,
                mood="зомби",
                exam="Математика"
            )
        ]

    def test_build_calculates_correct_medians(self, sample_records):
        """Тест: правильно ли считаются медианы."""
        report = MedianCoffee()
        result = report.build(sample_records)

        result_dict = {item["student"]: item["median_coffee_spent"] for item in result}

        assert result_dict["Иван Кузнецов"] == 650.0
        assert result_dict["Алексей Смирнов"] == 500.0

    def test_build_sets_results_attribute(self, sample_records):
        """Тест: build сохраняет результат в self.results."""
        report = MedianCoffee()
        assert report.results is None

        report.build(sample_records)
        assert report.results is not None

    def test_single_student_multiple_records(self):
        """Тест: один студент с несколькими записями."""
        records = [
            StudyRecord(
                student="Один Студент",
                date=date(2024, 6, 1),
                coffee_spent=100,
                sleep_hours=8.0,
                study_hours=2,
                mood="отл",
                exam="Тест"
            ),
            StudyRecord(
                student="Один Студент",
                date=date(2024, 6, 2),
                coffee_spent=200,
                sleep_hours=7.0,
                study_hours=4,
                mood="норм",
                exam="Тест"
            ),
            StudyRecord(
                student="Один Студент",
                date=date(2024, 6, 3),
                coffee_spent=300,
                sleep_hours=6.0,
                study_hours=6,
                mood="устал",
                exam="Тест"
            )
        ]

        report = MedianCoffee()
        result = report.build(records)

        assert result[0]["student"] == "Один Студент"
        assert result[0]["median_coffee_spent"] == 200.0


class TestReportRegistry:
    """Регистрация отчётов."""

    def test_median_coffee_registered(self):
        """Тест: регистраиция отчёта median-coffee."""
        assert "median-coffee" in REPORTS
        assert REPORTS["median-coffee"] == MedianCoffee
