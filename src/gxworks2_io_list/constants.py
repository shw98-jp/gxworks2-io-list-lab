from pathlib import Path


SAMPLE_DIR = Path("samples/ladder")
COMMENT_CSV_PATH = Path("samples/device_comments/device_comments.csv")
OUTPUT_DIR = Path("output")
OUTPUT_CSV_PATH = OUTPUT_DIR / "io_list.csv"
OUTPUT_EXCEL_PATH = OUTPUT_DIR / "io_list_report.xlsx"

STEP_INDEX = 0
INSTRUCTION_INDEX = 2
DEVICE_INDEX = 3
NOTE_INDEX = 6

IO_FIELDNAMES = [
    "No",
    "Type",
    "Device",
    "DeviceComment",
    "AddressNo",
    "UsedFiles",
    "Instructions",
    "LogicNotes",
    "Steps",
]

CHECK_FIELDNAMES = [
    "Level",
    "Type",
    "Device",
    "Message",
    "Details",
]

RAW_FIELDNAMES = [
    "SourceFile",
    "RowNumber",
    "Step",
    "Instruction",
    "Device",
    "LogicNote",
]
