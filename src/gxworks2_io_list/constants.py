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

IO_SHEET_FIELDNAMES = [
    "No",
    "Device",
    "DeviceComment",
    "UsedFiles",
    "Steps",
    "Instructions",
    "LogicNotes",
]

IO_CSV_FIELDNAMES = [
    "No",
    "Direction",
    "Device",
    "DeviceComment",
    "UsedFiles",
    "Steps",
    "Instructions",
    "LogicNotes",
]

CHECK_FIELDNAMES = [
    "Priority",
    "Severity",
    "ReviewStatus",
    "Category",
    "CheckType",
    "Device",
    "Message",
    "Evidence",
    "ReviewerNote",
]

CHECK_REFERENCE_FIELDNAMES = [
    "CheckType",
    "Severity",
    "Priority",
    "Category",
    "Meaning",
    "ReviewPoint",
    "SuggestedAction",
]

RAW_FIELDNAMES = [
    "SourceFile",
    "CsvRow",
    "StepNo",
    "Instruction",
    "Device",
    "LogicNote",
]

DEVICE_USAGE_FIELDNAMES = [
    "No",
    "DeviceCategory",
    "DeviceType",
    "Device",
    "DeviceComment",
    "Occurrences",
    "UsedFiles",
    "Instructions",
    "UsageLocations",
]

INSTRUCTION_REFERENCE_FIELDNAMES = [
    "Instruction",
    "Meaning",
    "LadderExample",
    "Description",
]

DEVICE_TYPE_REFERENCE_FIELDNAMES = [
    "DeviceType",
    "DeviceCategory",
    "Meaning",
    "Example",
    "Description",
]
