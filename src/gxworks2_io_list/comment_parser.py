import csv


def read_device_comments(comment_csv_path):
    comments = {}

    if not comment_csv_path.exists():
        return comments

    with comment_csv_path.open("r", encoding="utf-16", newline="") as file:
        reader = csv.reader(file, delimiter="\t")

        # First row is the project name. Second row is the header.
        next(reader, None)
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            device = row[0].strip()
            comment = row[1].strip()

            if device and comment:
                comments[device] = comment

    return comments
