import enum


class CONFIG_ACTION(enum.Enum):
    # Build wled-config files to generate config files per controller, and write them to file
    BUILD_AND_WRITE = 1,

    # Upload the generated configs to each specified controller's MDNS / IP
    UPLOAD = 2,

    # Upload the generated configs to the WLED access point (4.3.2.1)
    UPLOAD_WLED_AP_4321 = 3

    # GETs the actual config from the WLED http api, and compares it with the generated config. Logs if diffs found.
    TEST_COMPARE_ACTUAL_CONFIGS_TO_EXPECTED = 4  # GET

    # Rename a controller (name+mdns)
    RENAME = 5,
