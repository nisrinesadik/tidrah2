# backend/validation.py

def is_in_dakhla_region(lat, lon):
    """
    Check whether the given coordinates are within the Dakhla-Oued Ed-Dahab region.
    Args:
        lat (float): Latitude
        lon (float): Longitude
    Returns:
        bool: True if coordinates are within the region, False otherwise
        str: Message indicating result
    """
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return False, "Invalid GPS coordinates."

    if 21.358144 <= lat <= 24.595275 and -17.028126 <= lon <= -15.013220:
        return True, "Coordinates are within Dakhla region."
    else:
        return False, "Coordinates are outside the Dakhla region."

