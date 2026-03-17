from datetime import date

import pytest

from app.loader import csv_loader
from app.loader.models import StudyRecord


def test_csv_loader_success():
    """Тест успешной загрузки CSV файла."""
    result = csv_loader(["data/math.csv"])

    assert isinstance(result[0], StudyRecord)
    assert result[0].student == "Алексей Смирнов"
    assert result[0].date == date(2024, 6, 1)
    assert result[0].coffee_spent == 450
    assert result[0].sleep_hours == 4.5
    assert result[0].study_hours == 12
    assert result[0].mood == "норм"
    assert result[0].exam == "Математика"


def test_csv_loader_multiple_files(tmp_path):
    """Тест загрузки нескольких файлов."""
    file1 = tmp_path / "file1.csv"
    file1.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика",
        encoding="utf-8"
    )

    file2 = tmp_path / "file2.csv"
    file2.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика",
        encoding="utf-8"
    )

    result = csv_loader([str(file1), str(file2)])

    assert len(result) == 2
    students = {r.student for r in result}
    assert students == {"Алексей Смирнов", "Иван Кузнецов"}


def test_csv_loader_file_not_found():
    """Тест обработки несуществующего файла."""
    with pytest.raises(SystemExit) as exc_info:
        csv_loader(["file_name.csv"])
    assert "Файл 'file_name.csv' не найден!" in str(exc_info.value)
