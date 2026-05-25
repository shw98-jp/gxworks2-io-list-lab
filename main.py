import csv
from pathlib import Path

sample_dir = Path("samples/ladder")

inputs = {}
outputs = {}


def device_sort_key(device):
    device_type = device[0]
    address = device[1:]

    try:
        address_number = int(address, 16)
    except ValueError:
        address_number = 999999

    return device_type, address_number


def add_device(target, device, instruction, note, file_name):
    if device not in target:
        target[device] = {
            "device": device,
            "files": set(),
            "instructions": set(),
            "notes": set(),
        }

    target[device]["files"].add(file_name)

    if instruction:
        target[device]["instructions"].add(instruction)

    if note:
        target[device]["notes"].add(note)


for sample_path in sample_dir.glob("*.csv"):
    with sample_path.open("r", encoding="utf-16", newline="") as file:
        next(file)
        next(file)

        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            device = row["I/O(デバイス)"].strip()
            instruction = row["命令"].strip()
            note = row["ノート"].strip()

            if device.startswith("X"):
                add_device(inputs, device, instruction, note, sample_path.name)

            elif device.startswith("Y"):
                add_device(outputs, device, instruction, note, sample_path.name)


print("INPUT")
for device in sorted(inputs, key=device_sort_key):
    item = inputs[device]
    print(
        item["device"],
        ",".join(sorted(item["files"])),
        ",".join(sorted(item["instructions"])),
        ",".join(sorted(item["notes"])),
    )

print()

print("OUTPUT")
for device in sorted(outputs, key=device_sort_key):
    item = outputs[device]
    print(
        item["device"],
        ",".join(sorted(item["files"])),
        ",".join(sorted(item["instructions"])),
        ",".join(sorted(item["notes"])),
    )