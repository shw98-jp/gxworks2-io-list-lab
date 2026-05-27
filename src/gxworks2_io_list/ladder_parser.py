import csv

from .constants import DEVICE_INDEX, INSTRUCTION_INDEX, NOTE_INDEX, STEP_INDEX


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
