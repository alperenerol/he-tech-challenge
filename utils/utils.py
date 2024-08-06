from dateutil.parser import parse

def is_datetime(value):
    """
    Check if a given value is a datetime string.

    Parameters:
    value (str): The value to check.

    Returns:
    bool: True if the value is a datetime string, False otherwise.
    """
    if len(value) < 10:  # ISO 8601 format is at least 10 characters long (YYYY-MM-DD)
        return False
    
    try:
        parse(value)
        return True
    except (ValueError, TypeError):
        return False