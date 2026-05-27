from pathlib import Path


COMMENT_CSV_PATH = Path("samples/device_comments/device_comments.csv")

ENCODINGS = [
    "utf-16",
    "cp932",
    "shift_jis",
    "utf-8-sig",
    "utf-8",
]


def main():
    if not COMMENT_CSV_PATH.exists():
        print(f"File not found: {COMMENT_CSV_PATH}")
        return

    for encoding in ENCODINGS:
        try:
            text = COMMENT_CSV_PATH.read_text(encoding=encoding)
        except UnicodeError:
            print(f"Failed: {encoding}")
            continue

        print(f"Success: {encoding}")
        print()
        print(text[:1500])
        return

    print("Could not read the file with known encodings.")


if __name__ == "__main__":
    main()