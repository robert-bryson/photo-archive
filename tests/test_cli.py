import argparse
import subprocess
from pathlib import Path

import pytest

from parc.cli import validate_dir


def test_cli_version():
    result = subprocess.run(
        ["poetry", "run", "parc", "--version"], stdout=subprocess.PIPE, text=True
    )
    assert "parc 1.0.0" in result.stdout


def test_cli_help():
    result = subprocess.run(
        ["poetry", "run", "parc", "--help"], stdout=subprocess.PIPE, text=True
    )
    assert "usage:" in result.stdout


def test_validate_dir_valid(tmp_path):
    """Test that validate_dir returns a Path object for valid directories."""
    valid_dir = tmp_path / "valid_dir"
    valid_dir.mkdir()
    result = validate_dir(str(valid_dir))

    assert isinstance(result, Path)
    assert result == valid_dir


# def test_validate_dir_invalid(tmp_path):
#     """Test that validate_dir raises an error for invalid directories."""
#     invalid_dir = tmp_path / "invalid_dir"
#     with pytest.raises(
#         argparse.ArgumentTypeError, match=f"'{invalid_dir}' is not a valid directory."
#     ):
#         validate_dir(str(invalid_dir))
#
#
# def test_validate_dir_file(tmp_path):
#     """Test that validate_dir raises an error when the path is a file, not a directory."""
#     file_path = tmp_path / "file.txt"
#     file_path.touch()
#     with pytest.raises(
#         argparse.ArgumentTypeError, match=f"'{file_path}' is not a valid directory."
#     ):
#         validate_dir(str(file_path))
