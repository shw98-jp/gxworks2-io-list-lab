import csv
import re

from .constants import DEVICE_INDEX, INSTRUCTION_INDEX, NOTE_INDEX, STEP_INDEX


def get_device_type(device):
    match = re.match(r"^([A-Z]+)", device.upper())

    if match is None:
        return "UNKNOWN"

    return match.group(1)


def add_device_usage(target, device, instruction, file_name, row_number, step):
    if device not in target:
        target[device] = {
            "device": device,
            "device_type": get_device_type(device),
            "files": set(),
            "instructions": set(),
            "locations": set(),
            "occurrences": 0,
        }

    target[device]["occurrences"] += 1
    target[device]["files"].add(file_name)

    if instruction:
        target[device]["instructions"].add(instruction)

    location = f"{file_name}:row{row_number}"

    if step:
        location = f"{location}:step{step}"

    target[device]["locations"].add(location)


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
    device_usage = {}

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

                if device and device != "I/O(デバイス)":
                    add_device_usage(
                        device_usage,
                        device,
                        instruction,
                        sample_path.name,
                        row_number,
                        step,
                    )

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
                        "SourceFile": sample_path.name,
                        "RowNumber": row_number,
                        "Step": step,
                        "Instruction": instruction,
                        "Device": device,
                        "LogicNote": note,
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

    return inputs, outputs, raw_rows, device_usage
