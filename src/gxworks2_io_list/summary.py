def print_summary(inputs, outputs, checks, device_comments, csv_path, excel_path):
    print(f"Input devices  : {len(inputs)}")
    print(f"Output devices : {len(outputs)}")
    print(f"Device comments: {len(device_comments)}")
    print(f"Check items    : {len(checks)}")
    print(f"CSV file       : {csv_path}")
    print(f"Excel file     : {excel_path}")
