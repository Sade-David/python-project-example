from pyubx2 import ubxhelpers
import math

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


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two WGS84 points in meters.
    """
    # Earth's radius in meters
    R = 6371000 

    # Convert degrees to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
