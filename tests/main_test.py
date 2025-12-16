from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from src.check_last_x_hours_txt.main import datetime_is_in_last_x_hours


def test_datetime_within_last_24_hours(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text((datetime.now(UTC) - timedelta(hours=23)).isoformat())
    assert datetime_is_in_last_x_hours(file_path) is True


def test_datetime_outside_last_24_hours(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text((datetime.now(UTC) - timedelta(hours=25)).isoformat())
    assert datetime_is_in_last_x_hours(file_path) is False


def test_file_not_found(tmp_path: Path):
    file_path = tmp_path / "non_existing_file.txt"
    assert datetime_is_in_last_x_hours(file_path) is False


@patch("builtins.print")
def test_invalid_datetime_format(mock_printer, tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text(("invalid-datetime"))
    assert datetime_is_in_last_x_hours(file_path) is False
    mock_printer.assert_called_once_with(
        f"Error converting string to date. The string in {str(file_path)} "
        "is not in isoformat"
    )


def test_custom_hours_parameter_inside_interval(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text((datetime.now(UTC) - timedelta(hours=9)).isoformat())
    assert datetime_is_in_last_x_hours(file_path, hours=10) is True


def test_custom_hours_parameter_outside_interval(tmp_path: Path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text((datetime.now(UTC) - timedelta(hours=11)).isoformat())
    assert datetime_is_in_last_x_hours(file_path, hours=10) is False
