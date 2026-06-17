import csv

from .constants import IO_CSV_FIELDNAMES


def write_io_list_csv(output_path, rows):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=IO_CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
