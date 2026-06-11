from .device_utils import device_sort_key


SPARE_COMMENT_KEYWORDS = [
    "spare",
    "unused",
    "reserve",
    "reserved",
]


def is_spare_or_unused_comment(comment):
    normalized_comment = comment.strip().lower()

    return any(
        keyword in normalized_comment
        for keyword in SPARE_COMMENT_KEYWORDS
    )


def make_check_row(level, priority, category, check_type, device, message, details):
    return {
        "Level": level,
        "Priority": priority,
        "ReviewStatus": "OPEN",
        "Category": category,
        "Type": check_type,
        "Device": device,
        "Message": message,
        "Details": details,
        "ReviewerNote": "",
    }


def build_output_rows(io_type, devices, device_comments):
    rows = []

    for index, device in enumerate(sorted(devices, key=device_sort_key), start=1):
        item = devices[device]
        address_number = device_sort_key(device)[1]

        rows.append(
            {
                "No": index,
                "Type": io_type,
                "Device": item["device"],
                "DeviceComment": device_comments.get(device, ""),
                "AddressNo": address_number,
                "UsedFiles": ",".join(sorted(item["files"])),
                "Instructions": ",".join(sorted(item["instructions"])),
                "LogicNotes": ",".join(sorted(item["logic_notes"])),
                "Steps": ",".join(sorted(item["steps"])),
            }
        )

    return rows


def get_device_usage_category(device_type):
    if device_type in ("K", "H"):
        return "Constant"

    if device_type in ("SM", "SD"):
        return "SpecialDevice"

    if device_type in ("D", "M", "L", "B", "W", "R", "ZR"):
        return "InternalDevice"

    if device_type in ("T", "C"):
        return "TimerCounter"

    return "Other"


def build_device_usage_rows(device_usage, device_comments):
    rows = []

    for device in sorted(device_usage, key=device_sort_key):
        item = device_usage[device]

        if item["device_type"] in ("X", "Y"):
            continue

        rows.append(
            {
                "No": len(rows) + 1,
                "UsageCategory": get_device_usage_category(item["device_type"]),
                "DeviceType": item["device_type"],
                "Device": item["device"],
                "DeviceComment": device_comments.get(item["device"], ""),
                "Occurrences": item["occurrences"],
                "UsedFiles": ",".join(sorted(item["files"])),
                "Instructions": ",".join(sorted(item["instructions"])),
                "Locations": ",".join(sorted(item["locations"])),
            }
        )

    return rows


def build_check_rows(inputs, outputs, device_comments):
    check_rows = []

    all_devices = {}
    all_devices.update(inputs)
    all_devices.update(outputs)
    used_devices = set(all_devices)

    for device in sorted(all_devices, key=device_sort_key):
        item = all_devices[device]

        if device not in device_comments:
            check_rows.append(
                make_check_row(
                    "WARN",
                    "P1",
                    "Documentation",
                    "MISSING_DEVICE_COMMENT",
                    device,
                    "This I/O device is used in ladder CSV, but no device comment is registered.",
                    ",".join(sorted(item["files"])),
                )
            )

        if not item["logic_notes"]:
            check_rows.append(
                make_check_row(
                    "INFO",
                    "P3",
                    "LogicContext",
                    "MISSING_LOGIC_NOTE",
                    device,
                    "No nearby ladder logic note was found for this device.",
                    ",".join(sorted(item["files"])),
                )
            )

        if len(item["files"]) > 1:
            check_rows.append(
                make_check_row(
                    "WARN",
                    "P2",
                    "Usage",
                    "MULTIPLE_USED_FILES",
                    device,
                    "This I/O device is referenced in multiple ladder CSV files. Check whether the shared usage is intentional.",
                    ",".join(sorted(item["files"])),
                )
            )

        if len(item["logic_notes"]) > 1:
            check_rows.append(
                make_check_row(
                    "WARN",
                    "P2",
                    "LogicContext",
                    "MULTIPLE_LOGIC_NOTES",
                    device,
                    "Multiple logic notes were linked to this device. Review the context before using them as signal descriptions.",
                    ",".join(sorted(item["logic_notes"])),
                )
            )

    commented_io_devices = {
        device
        for device in device_comments
        if device.startswith(("X", "Y"))
    }
    unused_commented_devices = commented_io_devices - used_devices

    for device in sorted(unused_commented_devices, key=device_sort_key):
        device_comment = device_comments[device]

        if is_spare_or_unused_comment(device_comment):
            check_rows.append(
                make_check_row(
                    "INFO",
                    "P3",
                    "Documentation",
                    "SPARE_OR_UNUSED_DEVICE",
                    device,
                    "This X/Y device is documented as spare or unused and was not found in ladder CSV.",
                    device_comment,
                )
            )
            continue

        check_rows.append(
            make_check_row(
                "WARN",
                "P2",
                "Documentation",
                "COMMENTED_BUT_NOT_USED",
                device,
                "A device comment is registered, but this X/Y device was not found in ladder CSV. Check whether it is obsolete, spare, or missing from the analyzed ladder files.",
                device_comment,
            )
        )

    return check_rows
