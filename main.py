from datetime import datetime

from src.gxworks2_io_list.comment_parser import read_device_comments
from src.gxworks2_io_list.constants import (
    COMMENT_CSV_PATH,
    OUTPUT_CSV_PATH,
    OUTPUT_EXCEL_PATH,
    SAMPLE_DIR,
)
from src.gxworks2_io_list.csv_exporter import write_io_list_csv
from src.gxworks2_io_list.excel_exporter import write_io_list_excel
from src.gxworks2_io_list.ladder_parser import read_ladder_csv_files
from src.gxworks2_io_list.report_builder import (
    build_check_rows,
    build_device_usage_rows,
    build_output_rows,
)
from src.gxworks2_io_list.summary import print_summary


def build_report_metadata(project_name):
    return {
        "ProjectName": project_name,
        "GeneratedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "LadderCsvFolder": str(SAMPLE_DIR),
        "DeviceCommentFile": str(COMMENT_CSV_PATH),
        "OutputCsv": str(OUTPUT_CSV_PATH),
        "OutputExcel": str(OUTPUT_EXCEL_PATH),
    }


def main():
    inputs, outputs, raw_rows, device_usage, project_name = read_ladder_csv_files(
        SAMPLE_DIR
    )
    device_comments = read_device_comments(COMMENT_CSV_PATH)

    input_rows = build_output_rows("INPUT", inputs, device_comments)
    output_rows = build_output_rows("OUTPUT", outputs, device_comments)
    device_usage_rows = build_device_usage_rows(device_usage, device_comments)
    all_rows = input_rows + output_rows
    check_rows = build_check_rows(inputs, outputs, device_comments)
    ladder_source_count = len(list(SAMPLE_DIR.glob("*.csv")))
    metadata = build_report_metadata(project_name)

    write_io_list_csv(OUTPUT_CSV_PATH, all_rows)
    write_io_list_excel(
        OUTPUT_EXCEL_PATH,
        metadata,
        input_rows,
        output_rows,
        check_rows,
        device_usage_rows,
        raw_rows,
        ladder_source_count,
        len(device_comments),
    )

    print_summary(
        inputs,
        outputs,
        check_rows,
        device_comments,
        device_usage_rows,
        OUTPUT_CSV_PATH,
        OUTPUT_EXCEL_PATH,
    )


if __name__ == "__main__":
    main()
