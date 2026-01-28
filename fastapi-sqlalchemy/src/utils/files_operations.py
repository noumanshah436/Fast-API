import os
from pathlib import Path
import re
import shutil
from uuid import uuid4
from fastapi import UploadFile
from loguru import logger
import pandas as pd


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    Ensures compatibility across filesystems (especially Windows).

    Rules:
    - Replaces: < > : " | ? * \ / with underscores
    - Strips leading/trailing spaces and dots
    - Replaces spaces with underscores
    - Limits length to 200 chars
    """
    # Replace invalid characters with underscores
    invalid_chars = r'[<>:"|?*\\/]'
    sanitized = re.sub(invalid_chars, "_", filename)

    # Remove leading/trailing spaces and periods
    sanitized = sanitized.strip(" .")

    # Replace multiple spaces with single space
    sanitized = re.sub(r"\s+", " ", sanitized)

    # Replace spaces with underscores for better compatibility
    sanitized = sanitized.replace(" ", "_")

    # Limit length to 200 characters to be safe
    if len(sanitized) > 200:
        sanitized = sanitized[:200]

    # Ensure it's not empty
    if not sanitized:
        sanitized = "unnamed_file"

    return sanitized


def generate_unique_filename(original_name: str) -> str:
    """
    Generates a unique filename by appending a short UUID to the base name
    while preserving the original file extension. Handles filenames with or
    without extensions and sanitizes the base name for safe filesystem use.

    Args:
        original_name (str): The original filename (e.g., 'report.xlsx').

    Returns:
        str: A unique, sanitized filename (e.g., 'report_abc12345.xlsx').
    """
    unique_id = uuid4().hex[:8]

    # Use pathlib for safe extension handling
    path = Path(original_name)
    base_name = path.stem  # 'report' from 'report.xlsx'
    extension = path.suffix  # '.xlsx' (includes the dot)

    # Sanitize base name: replace spaces and remove unsafe chars
    safe_base_name = sanitize_filename(base_name)

    # Compose unique filename
    return f"{safe_base_name}_{unique_id}{extension}"


def cleanup_file(file_path: Path):
    """Safely clean up a file if it exists."""
    try:
        if file_path.exists():
            os.remove(file_path)
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")


def save_file(file: UploadFile, directory: str) -> Path:
    """
    Save an uploaded file to the specified directory with a unique name.

    Args:
        file: FastAPI UploadFile object.
        directory: Directory where the file will be stored.

    Returns:
        Path to the saved file.
    """
    temp_dir = Path(directory)
    temp_dir.mkdir(exist_ok=True)

    unique_filename = generate_unique_filename(file.filename)
    file_path = temp_dir / unique_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def save_df_to_file(df: pd.DataFrame, output_path: Path) -> Path:
    """
    Save a DataFrame to Excel at the given path.

    Args:
        df: DataFrame to save.
        output_path: Path object where the file will be saved.

    Returns:
        Path: The saved file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False, engine="openpyxl")

    return output_path


def append_suffix_to_filename(
    file_path: str, suffix: str, new_extension: str = None
) -> str:
    """
    Appends a suffix to a file name before the extension, with optional extension change.

    Args:
        file_path (str): Original file path.
        suffix (str): Suffix to append (e.g., '_processed').
        new_extension (str, optional): New file extension (without dot), e.g., 'xlsx'.
            If None, keeps the original extension.

    Returns:
        str: Modified file path with suffix and updated extension.
    """
    path = Path(file_path)
    # If new extension provided, ensure it starts with "."
    extension = f".{new_extension}" if new_extension else path.suffix
    new_name = f"{path.stem}{suffix}{extension}"
    return str(path.with_name(new_name))
