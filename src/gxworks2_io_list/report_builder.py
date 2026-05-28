from .device_utils import device_sort_key


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
                    "Type": "MISSING_DEVICE_COMMENT",
                    "Device": device,
                    "Message": "Device comment is empty.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if not item["logic_notes"]:
            check_rows.append(
                {
                    "Level": "WARN",
                    "Type": "MISSING_LOGIC_NOTE",
                    "Device": device,
                    "Message": "Logic note is empty.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if len(item["files"]) > 1:
            check_rows.append(
                {
                    "Level": "WARN",
                    "Type": "MULTIPLE_USED_FILES",
                    "Device": device,
                    "Message": "Device is used in multiple files.",
                    "Details": ",".join(sorted(item["files"])),
                }
            )

        if len(item["logic_notes"]) > 1:
            check_rows.append(
                {
                    "Level": "WARN",
                    "Type": "MULTIPLE_LOGIC_NOTES",
                    "Device": device,
                    "Message": "Device has multiple logic notes.",
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
        check_rows.append(
            {
                "Level": "INFO",
                "Type": "COMMENTED_BUT_NOT_USED",
                "Device": device,
                "Message": "Device comment exists, but this device is not used in ladder CSV.",
                "Details": device_comments[device],
            }
        )

    return check_rows
