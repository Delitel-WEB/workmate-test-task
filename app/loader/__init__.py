import csv
from datetime import datetime

from app.loader.models import StudyRecord


def csv_loader(files: list) -> list[StudyRecord]:
    """Загрузчик данных из csv файлов."""
    records = []

    for file in files:
        try:
            with open(file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = StudyRecord(
                        student=row["student"],
                        date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                        coffee_spent=int(row["coffee_spent"]),
                        sleep_hours=float(row["sleep_hours"]),
                        study_hours=int(row["study_hours"]),
                        mood=row["mood"],
                        exam=row["exam"]
                    )
                    records.append(record)
        except FileNotFoundError as err:
            raise SystemExit(f"Файл '{file}' не найден!") from err

    return records
