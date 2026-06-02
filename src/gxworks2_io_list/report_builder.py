from .device_utils import device_sort_key


SPARE_COMMENT_KEYWORDS = [
    "spare",
    "unused",
    "reserve",
    "reserved",
    "予備",
    "未使用",
]


def is_spare_or_unused_comment(comment):
    normalized_comment = comment.strip().lower()

    return any(
        keyword.lower() in normalized_comment
        for keyword in SPARE_COMMENT_KEYWORDS
    )


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
                {
                    "Level": "WARN",
                    "Category": "Documentation",
                    "Type": "MISSING_DEVICE_COMMENT",
                    "Device": device,
                    "Message": "This I/O device is used in ladder CSV, but no device comment is registered.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if not item["logic_notes"]:
            check_rows.append(
                {
                    "Level": "INFO",
                    "Category": "LogicContext",
                    "Type": "MISSING_LOGIC_NOTE",
                    "Device": device,
                    "Message": "No nearby ladder logic note was found for this device.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if len(item["files"]) > 1:
            check_rows.append(
                {
                    "Level": "WARN",
                    "Category": "Usage",
                    "Type": "MULTIPLE_USED_FILES",
                    "Device": device,
                    "Message": "This I/O device is referenced in multiple ladder CSV files. Check whether the shared usage is intentional.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if len(item["logic_notes"]) > 1:
            check_rows.append(
                {
                    "Level": "WARN",
                    "Category": "LogicContext",
                    "Type": "MULTIPLE_LOGIC_NOTES",
                    "Device": device,
                    "Message": "Multiple logic notes were linked to this device. Review the context before using them as signal descriptions.",
                    "Details": ",".join(sorted(item["logic_notes"])),
                }
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
                {
                    "Level": "INFO",
                    "Category": "Documentation",
                    "Type": "SPARE_OR_UNUSED_DEVICE",
                    "Device": device,
                    "Message": "This X/Y device is documented as spare or unused and was not found in ladder CSV.",
                    "Details": device_comment,
                }
            )
            continue

        check_rows.append(
            {
                "Level": "WARN",
                "Category": "Documentation",
                "Type": "COMMENTED_BUT_NOT_USED",
                "Device": device,
                "Message": "A device comment is registered, but this X/Y device was not found in ladder CSV. Check whether it is obsolete, spare, or missing from the analyzed ladder files.",
                "Details": device_comment,
            }
        )

    return check_rows
