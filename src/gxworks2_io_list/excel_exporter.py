from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from .constants import CHECK_FIELDNAMES, IO_FIELDNAMES, RAW_FIELDNAMES


def write_sheet(ws, rows, fieldnames):
    ws.append(fieldnames)

    header_fill = PatternFill("solid", fgColor="D9EAF7")
    header_font = Font(bold=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font

    for row in rows:
        ws.append([row[field] for field in fieldnames])

    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for column_cells in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            value = "" if cell.value is None else str(cell.value)
            max_length = max(max_length, len(value))

        ws.column_dimensions[column_letter].width = min(max_length + 2, 80)


def write_summary_sheet(
    ws,
    input_rows,
    output_rows,
    check_rows,
    ladder_source_count,
    comment_count,
):
    ws.append(["Item", "Value"])
    ws.append(["Ladder CSV files", ladder_source_count])
    ws.append(["Device comments", comment_count])
    ws.append(["Input devices", len(input_rows)])
    ws.append(["Output devices", len(output_rows)])
    ws.append(["Total devices", len(input_rows) + len(output_rows)])
    ws.append(["Check items", len(check_rows)])

    header_fill = PatternFill("solid", fgColor="D9EAF7")
    header_font = Font(bold=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font

    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 18


def write_io_list_excel(
    output_path,
    input_rows,
    output_rows,
    check_rows,
    raw_rows,
    ladder_source_count,
    comment_count,
):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()

    summary_ws = wb.active
    summary_ws.title = "SUMMARY"
    write_summary_sheet(
        summary_ws,
        input_rows,
        output_rows,
        check_rows,
        ladder_source_count,
        comment_count,
    )

    input_ws = wb.create_sheet("INPUT")
    write_sheet(input_ws, input_rows, IO_FIELDNAMES)

    output_ws = wb.create_sheet("OUTPUT")
    write_sheet(output_ws, output_rows, IO_FIELDNAMES)

    check_ws = wb.create_sheet("CHECK")
    write_sheet(check_ws, check_rows, CHECK_FIELDNAMES)

    raw_ws = wb.create_sheet("RAW_DATA")
    write_sheet(raw_ws, raw_rows, RAW_FIELDNAMES)

    wb.save(output_path)
