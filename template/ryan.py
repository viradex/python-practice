import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv


class AdminSearchForm(ttk.Frame):
    def ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist"""
        if not self.events_bookings_csv.exists():
            with open(self.events_bookings, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "booking_id",
                        "event_date",
                        "ticket_tier" "num_adults" "num_children",
                        "total_cost",
                        "date_entered",
                    ]
                )

    # links the Tkinter mainloop and CSV file do eachother
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")
        self.event_date_var = tk.StringVar()
        self.sort_by_var = tk.StringVar(value="total_cost")

        self.setup_grid()
        self.create_widgets()

        # File setup
        BASE_DIR = Path(__file__).resolve().parent
        self.events_bookings_csv = BASE_DIR / "events_bookings.csv"

        # Ensure file exists
        self.ensure_csv_exists()

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def create_widgets(self):
        lbl_heading = ttk.Label(self, text="Admin Search", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        lbl_event_date = ttk.Label(self, text="Event date:")
        lbl_event_date.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        ent_event_date = ttk.Entry(self, textvariable=self.event_date_var)
        ent_event_date.grid(row=1, column=1, sticky="ew", pady=5)

        lbl_sort_by = ttk.Label(self, text="Sort by:")
        lbl_sort_by.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort_by = ttk.Combobox(
            self,
            textvariable=self.sort_by_var,
            state="readonly",
            values=["total_cost", "date_entered"],
        )
        cbo_sort_by.grid(row=2, column=1, sticky="ew", pady=5)

        btn_search = ttk.Button(self, text="Search")
        btn_search.grid(row=3, column=0, sticky="w", pady=(10, 10))

        columns = (
            "booking_id",
            "event_date",
            "ticket_tier",
            "num_adults",
            "num_children",
            "total_cost",
            "date_entered",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

        headings = {
            "booking_id": "Booking ID",
            "event_date": "Event Date",
            "ticket_tier": "Tier",
            "num_adults": "Adults",
            "num_children": "Children",
            "total_cost": "Total Cost",
            "date_entered": "Date Entered",
        }

        for column_name in columns:
            self.tree.heading(column_name, text=headings[column_name])
            self.tree.column(column_name, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)


def ensure_csv_exists(self):
    """Create CSV file with headers if it doesn't exist"""
    if not self.events_bookings.exists():
        with open(self.events_bookings, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "booking_id",
                    "event_date",
                    "ticket_tier" "num_adults" "num_children",
                    "total_cost",
                    "date_entered",
                ]
            )

    def load_results(self):
        """Load, filter, sort, and display CSV data"""

    matches = []
    queens_match = self.filter_var.get() == "Orders with queens"
    sort_by_var = self.sort_var.get()

    try:
        with open(
            self.events_bookings_csv, newline="", encoding="utf-8"
        ) as events_bookings_file:
            reader = csv.DictReader(events_bookings_file)

            for row in reader:
                try:
                    # Convert values safely
                    num_queens = int(row["num_queens"])

                    # Filter logic
                    has_queens = num_queens > 0
                    if queens_match == has_queens:
                        matches.append(row)

                except ValueError:
                    # Skip bad rows instead of crashing
                    continue

    except FileNotFoundError:
        messagebox.showerror("Error", "events_bookings.csv not found.")
        return

    # Sort results numerically
    try:
        sorted_matches = sorted(matches, key=lambda r: float(r[sort_by_var]))
    except ValueError:
        messagebox.showerror("Error", "Sorting failed due to bad data.")
        return

    # Clear table
    for item in self.tree.get_children():
        self.tree.delete(item)

    # Insert sorted data
    for row in sorted_matches:
        self.tree.insert("", tk.END, values=list(row.values()))

    messagebox.showinfo("Loaded", f"{len(sorted_matches)} records displayed.")


def main():
    root = tk.Tk()
    root.title("Event Ticketing Admin Search")
    root.geometry("900x450")

    AdminSearchForm(root)

    root.mainloop()


if __name__ == "__main__":
    main()
