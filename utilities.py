from pyubx2 import ubxhelpers


def hex_string_to_bytes(hex_str: str) -> str:
    """
    Converts a space-separated hex string into a bytes object.
    Example: "06 01 02 AB F0 05" -> b'\x06\x01\x02\xab\xf0\x05'
    """
    # Remove spaces and convert to bytes
    return bytes.fromhex(hex_str)


def bytes_string_to_hex(byte_str: str) -> str:
    """
    Converts a bytes object into an uppercase, space-separated hex string.
    Ensures single digits like \x09 become '09'.
    """
    # .hex(" ") handles the spacing (Python 3.8+)
    # .upper() makes it "8A" instead of "8a"
    return byte_str.hex(" ").upper()


def calc_checksum(msg_data: str) -> str:
    return ubxhelpers.calc_checksum(msg_data)
