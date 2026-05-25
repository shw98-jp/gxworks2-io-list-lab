import csv
from pathlib import Path


SAMPLE_DIR = Path("samples/ladder")
OUTPUT_DIR = Path("output")
OUTPUT_PATH = OUTPUT_DIR / "io_list.csv"

STEP_INDEX = 0
INSTRUCTION_INDEX = 2
DEVICE_INDEX = 3
NOTE_INDEX = 6


def device_sort_key(device):
    device_type = device[0]
    address = device[1:]

    try:
        address_number = int(address, 16)
    except ValueError:
        address_number = 999999

    return device_type, address_number


def add_device(target, device, instruction, file_name, step):
    if device not in target:
        target[device] = {
            "device": device,
            "files": set(),
            "instructions": set(),
            "logic_notes": set(),
            "steps": set(),
        }

    target[device]["files"].add(file_name)

    if instruction:
        target[device]["instructions"].add(instruction)

    if step:
        target[device]["steps"].add(f"{file_name}:{step}")


def add_logic_note(target, device, note):
    if device in target and note:
        target[device]["logic_notes"].add(note)


def is_note_only_row(row, note):
    if not note:
        return False

    return all(
        not row[index].strip()
        for index in range(min(len(row), NOTE_INDEX))
    )


def read_ladder_csv_files(sample_dir):
    inputs = {}
    outputs = {}
    raw_rows = []

    for sample_path in sorted(sample_dir.glob("*.csv")):
        current_io_type = None
        current_device = None

        with sample_path.open("r", encoding="utf-16", newline="") as file:
            reader = csv.reader(file, delimiter="\t")

            for row_number, row in enumerate(reader, start=1):
                if len(row) <= DEVICE_INDEX:
                    continue

                step = row[STEP_INDEX].strip()
                instruction = row[INSTRUCTION_INDEX].strip()
                device = row[DEVICE_INDEX].strip()
                note = row[NOTE_INDEX].strip() if len(row) > NOTE_INDEX else ""

                if is_note_only_row(row, note) and current_device:
                    if current_io_type == "INPUT":
                        add_logic_note(inputs, current_device, note)
                    elif current_io_type == "OUTPUT":
                        add_logic_note(outputs, current_device, note)
                    continue

                if not device.startswith(("X", "Y")):
                    continue

                raw_rows.append(
                    {
                        "source_file": sample_path.name,
                        "row_number": row_number,
                        "step": step,
                        "instruction": instruction,
                        "device": device,
                        "logic_note": note,
                    }
                )

                if device.startswith("X"):
                    add_device(inputs, device, instruction, sample_path.name, step)
                    current_io_type = "INPUT"
                    current_device = device
                elif device.startswith("Y"):
                    add_device(outputs, device, instruction, sample_path.name, step)
                    current_io_type = "OUTPUT"
                    current_device = device

    return inputs, outputs, raw_rows


def build_output_rows(io_type, devices):
    rows = []

    for index, device in enumerate(sorted(devices, key=device_sort_key), start=1):
        item = devices[device]
        address_number = device_sort_key(device)[1]

        rows.append(
            {
                "No": index,
                "Type": io_type,
                "Device": item["device"],
                "AddressNo": address_number,
                "UsedFiles": ",".join(sorted(item["files"])),
                "Instructions": ",".join(sorted(item["instructions"])),
                "LogicNotes": ",".join(sorted(item["logic_notes"])),
                "Steps": ",".join(sorted(item["steps"])),
            }
        )

    return rows


def write_io_list_csv(output_path, inputs, outputs):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    rows.extend(build_output_rows("INPUT", inputs))
    rows.extend(build_output_rows("OUTPUT", outputs))

    fieldnames = [
        "No",
        "Type",
        "Device",
        "AddressNo",
        "UsedFiles",
        "Instructions",
        "LogicNotes",
        "Steps",
    ]

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return rows


def print_summary(inputs, outputs, output_path):
    print(f"Input devices : {len(inputs)}")
    print(f"Output devices: {len(outputs)}")
    print(f"Output file   : {output_path}")


def main():
    inputs, outputs, _ = read_ladder_csv_files(SAMPLE_DIR)
    write_io_list_csv(OUTPUT_PATH, inputs, outputs)
    print_summary(inputs, outputs, OUTPUT_PATH)


if __name__ == "__main__":
    main()