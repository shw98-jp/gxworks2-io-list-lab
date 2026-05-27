def device_sort_key(device):
    device_type = device[0]
    address = device[1:]

    try:
        address_number = int(address, 16)
    except ValueError:
        address_number = 999999

    return device_type, address_number
