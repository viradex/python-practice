import csv
from pathlib import Path

from models.booking import Booking


class BookingRepoCSV:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.csv_path = self.data_dir / "bookings.csv"
        self.fields = [
            "booking_id",
            "event_date",
            "ticket_tier",
            "num_adults",
            "num_children",
            "total_cost",
            "date_entered",
        ]

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_csv_exists(self):
        self._ensure_data_dir()

        if self.csv_path.exists() is True:
            return

        with open(self.csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()

    def load_all(self):
        self._ensure_csv_exists()

        bookings = []
        with open(self.csv_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("booking_id", "").isdigit() is False:
                    continue

                # booking_id,event_date,ticket_tier,num_adults,num_children,total_cost,date_entered
                bookings.append(
                    Booking(
                        booking_id=int(row.get("booking_id", 0)),
                        event_date=row.get("event_date", ""),
                        ticket_tier=row.get("ticket_tier", "Standard"),
                        num_adults=int(row.get("num_adults", 0)),
                        num_children=int(row.get("num_children", 0)),
                        total_cost=float(row.get("total_cost", 0)),
                        date_entered=row.get("date_entered", ""),
                    )
                )

        bookings.sort(key=lambda booking: booking.booking_id)
        return bookings

    def save_all(self, bookings: list[Booking]):
        self._ensure_csv_exists()

        with open(self.csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()

            for booking in bookings:
                writer.writerow(booking.to_csv_row())

    def save(self, bookings, booking):
        self._ensure_csv_exists()

        bookings.append(booking)
        with open(self.csv_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(booking.to_csv_row())

    def update(self, bookings, updated_booking):
        for i, item in enumerate(bookings):
            if item.booking_id == updated_booking.booking_id:
                bookings[i] = updated_booking
                bookings.sort(key=lambda b: b.booking_id)

                self.save_all(bookings)
                return True

        return False

    def delete(self, bookings, booking_id):
        for i, booking in enumerate(bookings):
            if booking.booking_id == int(booking_id):
                del bookings[i]

                self.save_all(bookings)
                return True

        return False

    def get_next_id(self):
        self._ensure_csv_exists()

        bookings = self.load_all()
        if not bookings:
            return 1

        return max(b.booking_id for b in bookings) + 1

    def create_booking(self, event_date, tier, adults, children, booking_id=None):
        booking_id = self.get_next_id() if booking_id is None else booking_id
        return Booking.create(booking_id, event_date, tier, adults, children)
