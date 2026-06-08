INSTRUCTION_REFERENCE_ROWS = [
    {
        "Instruction": "LD",
        "Meaning": "Load",
        "LadderExample": "|--[ X0 ]--",
        "Description": "Starts a condition using a normally open contact.",
    },
    {
        "Instruction": "AND",
        "Meaning": "And",
        "LadderExample": "|--[ X0 ]--[ X1 ]--",
        "Description": "Adds a serial condition. All serial conditions must be true.",
    },
    {
        "Instruction": "OR",
        "Meaning": "Or",
        "LadderExample": "Parallel branch",
        "Description": "Adds a parallel condition. Any branch can make the condition true.",
    },
    {
        "Instruction": "ANI",
        "Meaning": "And Not",
        "LadderExample": "|--[ X0 ]--[/ X1 ]--",
        "Description": "Adds a serial normally closed condition.",
    },
    {
        "Instruction": "OUT",
        "Meaning": "Output",
        "LadderExample": "|--[ X0 ]--( Y0 )--",
        "Description": "Writes the condition result to an output coil or internal bit.",
    },
    {
        "Instruction": "SET",
        "Meaning": "Set",
        "LadderExample": "|--[ X0 ]--( SET M0 )--",
        "Description": "Turns a bit on and keeps it on until it is reset.",
    },
    {
        "Instruction": "RST",
        "Meaning": "Reset",
        "LadderExample": "|--[ X1 ]--( RST M0 )--",
        "Description": "Turns a set bit off.",
    },
    {
        "Instruction": "MOV",
        "Meaning": "Move",
        "LadderExample": "MOV D0 D10",
        "Description": "Copies a value from a source device to a destination device.",
    },
    {
        "Instruction": "DMOV",
        "Meaning": "Double Move",
        "LadderExample": "DMOV SD1880 D2000",
        "Description": "Copies a 32-bit value, usually using two consecutive words.",
    },
    {
        "Instruction": "INC",
        "Meaning": "Increment",
        "LadderExample": "INC D0",
        "Description": "Increases the target device value by one.",
    },
]


DEVICE_TYPE_REFERENCE_ROWS = [
    {
        "DeviceType": "X",
        "Meaning": "Input",
        "Example": "X0",
        "Description": "Physical input such as a sensor, push button, or switch.",
    },
    {
        "DeviceType": "Y",
        "Meaning": "Output",
        "Example": "Y0",
        "Description": "Physical output such as a lamp, relay, solenoid, or actuator signal.",
    },
    {
        "DeviceType": "M",
        "Meaning": "Internal relay",
        "Example": "M100",
        "Description": "Internal bit used inside the PLC program.",
    },
    {
        "DeviceType": "SM",
        "Meaning": "Special relay",
        "Example": "SM402",
        "Description": "System bit provided by the PLC CPU or special function area.",
    },
    {
        "DeviceType": "D",
        "Meaning": "Data register",
        "Example": "D2000",
        "Description": "Word register used to store numeric values.",
    },
    {
        "DeviceType": "SD",
        "Meaning": "Special data register",
        "Example": "SD1880",
        "Description": "System data register provided by the PLC CPU or special function area.",
    },
    {
        "DeviceType": "K",
        "Meaning": "Decimal constant",
        "Example": "K1000",
        "Description": "Fixed decimal value used as an instruction parameter.",
    },
    {
        "DeviceType": "H",
        "Meaning": "Hex constant",
        "Example": "H1",
        "Description": "Fixed hexadecimal value used as an instruction parameter.",
    },
    {
        "DeviceType": "T",
        "Meaning": "Timer",
        "Example": "T0",
        "Description": "Timer device used for time-based control.",
    },
    {
        "DeviceType": "C",
        "Meaning": "Counter",
        "Example": "C0",
        "Description": "Counter device used for count-based control.",
    },
]
