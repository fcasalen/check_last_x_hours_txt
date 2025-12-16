from datetime import UTC, datetime
from pathlib import Path


def datetime_is_in_last_x_hours(file_path_to_datetime: str, hours: int = 24) -> bool:
    """
    Check if a datetime stored in a file is within the last X `hours` (default is 24).

    This function reads the first value from a file (assumed to be in ISO 8601 datetime
    format), converts it to a `datetime` object, and checks if it falls within the
    last `hours`.

    Args:
        file_path_to_datetime (str): The file path containing the datetime string in
            ISO 8601 format.
        hours (int, optional): The number of hours to check against. Defaults to 24.

    Returns:
        bool:
            - `True` if the datetime is within the last `hours`.
            - `False` if the file is not found, the datetime is not in ISO 8601 format,
              or the datetime is outside the specified time range.

    Exceptions:
        - `ValueError`: If the datetime string is invalid or not in ISO 8601 format,
          a warning is printed via `CLIPPrinter.yellow`, and `False` is returned.

    Example:
        >>> # Assuming `test_file.txt` contains "2023-10-01T12:00:00"
        >>> datetime_is_in_last_X_hours("test_file.txt")
        True
        >>> datetime_is_in_last_X_hours("nonexistent_file.txt")
        False
        >>> datetime_is_in_last_X_hours("malformed_file.txt")
        Error converting string to date. Check if the string in malformed_file.txt
        is in isoformat
        False
    """
    if not Path(file_path_to_datetime).exists():
        return False
    try:
        with open(file_path_to_datetime, "r", encoding="utf-8") as file:
            last = file.readline().strip()
        last = datetime.fromisoformat(last)
        if (datetime.now(UTC) - last).total_seconds() < 3600 * hours:
            return True
        return False
    except ValueError:
        print(
            f"Error converting string to date. The string in {file_path_to_datetime} "
            "is not in isoformat"
        )
        return False
