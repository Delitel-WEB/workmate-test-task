from app.loader import csv_loader
from app.reports.median_coffee import MedianCoffee


def test_full_pipeline(tmp_path):
    """Тест: загрузка -> отчёт."""
    csv_content = """student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика
Иван Кузнецов,2024-06-02,650,2.5,17,зомби,Математика
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика"""

    file_path = tmp_path / "data.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    records = csv_loader([str(file_path)])

    report = MedianCoffee()
    result = report.build(records)

    assert len(result) == 2
    assert result[0]["student"] == "Иван Кузнецов"
    assert result[0]["median_coffee_spent"] == 625.0
    assert result[1]["student"] == "Алексей Смирнов"
    assert result[1]["median_coffee_spent"] == 475.0


def test_multiple_files_pipeline(tmp_path):
    """Тест с несколькими файлами."""
    file1 = tmp_path / "data1.csv"
    file1.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика",
        encoding="utf-8"
    )

    file2 = tmp_path / "data2.csv"
    file2.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Иван Кузнецов,2024-06-02,700,2.0,18,не выжил,Математика",
        encoding="utf-8"
    )

    records = csv_loader([str(file1), str(file2)])
    report = MedianCoffee()
    result = report.build(records)

    assert len(result) == 1
    assert result[0]["student"] == "Иван Кузнецов"
    assert result[0]["median_coffee_spent"] == 650.0
