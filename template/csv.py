import csv
from pathlib import Path

# =========================
# CONFIG
# =========================

FILE_PATH = Path("data.csv")
FIELDNAMES = ["id", "name", "age"]  # EDIT


# =========================
# READ ALL
# =========================


def read_all():
    """Read all records"""
    if not FILE_PATH.exists():
        return []

    with FILE_PATH.open("r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# =========================
# GENERATE ID
# =========================


def generate_id():
    """Generate unique ID"""
    data = read_all()

    if not data:
        return "1"

    return str(max(int(row["id"]) for row in data) + 1)


# =========================
# CREATE (APPEND ONLY)
# =========================


def create_record(name, age):
    """Create record using append"""

    file_exists = FILE_PATH.exists()

    with FILE_PATH.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        # write header only if file new
        if not file_exists:
            writer.writeheader()

        writer.writerow({"id": generate_id(), "name": name, "age": age})


# =========================
# READ FILTERED
# =========================


def read_filtered(field, value):
    """Return filtered records"""
    data = read_all()
    return [row for row in data if row[field] == value]


# =========================
# UPDATE (OVERWRITE)
# =========================


def update_record(record_id, updated_data):
    """Update record (overwrite method)"""
    data = read_all()

    for row in data:
        if row["id"] == str(record_id):
            row.update(updated_data)

    write_all(data)


# =========================
# DELETE (OVERWRITE)
# =========================


def delete_record(record_id):
    """Delete record"""
    data = read_all()

    new_data = [row for row in data if row["id"] != str(record_id)]

    write_all(new_data)


# =========================
# WRITE ALL (OVERWRITE)
# =========================


def write_all(data):
    """Overwrite file with data"""
    with FILE_PATH.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)
