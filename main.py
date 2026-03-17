import argparse

from app.loader import csv_loader
from app.reports.base import REPORTS, BaseReport


def parse_args() -> argparse.Namespace:
    """Парсер аргументов проекта."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    report_class = REPORTS.get(args.report)
    if not report_class:
        raise SystemExit(f"Неизвестный отчёт: {args.report}")

    records = csv_loader(args.files)
    report: BaseReport = report_class()
    report.build(records)
    report.print_report()


if __name__ == "__main__":
    main()
