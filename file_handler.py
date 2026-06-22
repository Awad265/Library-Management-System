"""
file_handler.py
---------------
Handles all CSV file read and write operations for the Library Management System.
"""

import csv
import os



##  Generic helpers                                                              


def ensure_file(filepath: str, headers: list) -> None:
    """
    Create a CSV file with headers if it does not already exist.

    Args:
        filepath (str): Path to the CSV file.
        headers (list): Column header names.
    """
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def read_csv(filepath: str) -> list:
    """
    Read all rows from a CSV file (excluding the header row).

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        list: A list of rows, each row being a list of strings.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    rows = []
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if row:  # Skip blank lines
                rows.append(row)
    return rows


def write_csv(filepath: str, headers: list, rows: list) -> None:
    """
    Overwrite a CSV file with new data.

    Args:
        filepath (str): Path to the CSV file.
        headers (list): Column header names.
        rows (list): List of rows (each row is a list of values).
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def append_csv(filepath: str, row: list) -> None:
    """
    Append a single row to an existing CSV file.

    Args:
        filepath (str): Path to the CSV file.
        row (list): The row to append.
    """
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)



##  File paths and headers                                                       


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

BOOKS_FILE = os.path.join(DATA_DIR, "books.csv")
BOOKS_HEADERS = ["isbn", "title", "author", "genre", "total_copies", "available_copies"]

MEMBERS_FILE = os.path.join(DATA_DIR, "members.csv")
MEMBERS_HEADERS = ["member_id", "name", "email", "borrowed_isbns"]

TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
TRANSACTIONS_HEADERS = ["transaction_id", "member_id", "isbn", "action", "date"]


def initialise_data_files() -> None:
    """Create all data CSV files with headers if they do not exist."""
    ensure_file(BOOKS_FILE, BOOKS_HEADERS)
    ensure_file(MEMBERS_FILE, MEMBERS_HEADERS)
    ensure_file(TRANSACTIONS_FILE, TRANSACTIONS_HEADERS)
