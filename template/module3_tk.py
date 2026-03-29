import csv
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

PRICES = {
    "standard": {"adult": 40, "child": 25},
    "premium": {"adult": 70, "child": 45},
    "vip": {"adult": 110, "child": 70},
}


# ---------------- DATA LAYER ---------------- #
class SaveDataManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.csv_path = self.base_dir / "bookings.csv"
        self.fields = [
            "id",
            "tier",
            "adults",
            "children",
            "subtotal",
            "discount",
            "final",
        ]
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        if self.csv_path.exists():
            return
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()

    def load_all(self):
        self.ensure_csv_exists()
        data = []
        with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get("id", "").isdigit():
                    continue
                data.append(
                    {
                        "id": int(row["id"]),
                        "tier": row["tier"],
                        "adults": int(row["adults"]),
                        "children": int(row["children"]),
                        "subtotal": float(row["subtotal"]),
                        "discount": float(row["discount"]),
                        "final": float(row["final"]),
                    }
                )
        return sorted(data, key=lambda x: x["id"])

    def overwrite_all(self, data):
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def get_next_id(self):
        data = self.load_all()
        if not data:
            return 1
        return max(x["id"] for x in data) + 1


# ---------------- LOGIC ---------------- #
def calculate_booking(tier, adults, children):
    adult_price = PRICES[tier]["adult"]
    child_price = PRICES[tier]["child"]
    subtotal = adults * adult_price + children * child_price
    discount = subtotal * 0.1 if adults + children >= 5 else 0
    final = subtotal - discount
    return subtotal, discount, final


# ---------------- UI ---------------- #
class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Riverstone Arena")
        self.manager = SaveDataManager()
        self.bookings = []
        self.filtered = []

        self.table_frame = None
        self.form_frame = None
        self.current_edit = None

        self.create_table_frame()
        self.create_form_frame()
        self.show_table()
        self.load_data()

    # ---------- TABLE ---------- #
    def create_table_frame(self):
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill="both", expand=True)

        # Top controls
        top = ttk.Frame(self.table_frame, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Filter Tier:").pack(side="left")
        self.filter_var = tk.StringVar(value="All")
        ttk.Combobox(
            top,
            textvariable=self.filter_var,
            values=["All", "standard", "premium", "vip"],
            state="readonly",
            width=10,
        ).pack(side="left", padx=5)

        ttk.Label(top, text="Sort By:").pack(side="left", padx=(10, 0))
        self.sort_col = tk.StringVar(value="id")
        ttk.Combobox(
            top,
            textvariable=self.sort_col,
            values=[
                "id",
                "tier",
                "adults",
                "children",
                "subtotal",
                "discount",
                "final",
            ],
            state="readonly",
            width=12,
        ).pack(side="left", padx=5)

        self.sort_dir = tk.StringVar(value="Ascending")
        ttk.Combobox(
            top,
            textvariable=self.sort_dir,
            values=["Ascending", "Descending"],
            state="readonly",
            width=12,
        ).pack(side="left", padx=5)

        ttk.Button(top, text="Apply", command=self.apply_filter_sort).pack(
            side="left", padx=10
        )

        # Buttons
        mid = ttk.Frame(self.table_frame, padding=10)
        mid.pack(fill="x")
        ttk.Button(mid, text="Add", command=self.add_booking).pack(side="left", padx=5)
        ttk.Button(mid, text="Edit", command=self.edit_booking).pack(
            side="left", padx=5
        )
        ttk.Button(mid, text="Delete", command=self.delete_booking).pack(
            side="left", padx=5
        )
        ttk.Button(mid, text="Load", command=self.load_data).pack(side="left", padx=5)

        # Treeview
        cols = ("id", "tier", "adults", "children", "subtotal", "discount", "final")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show="headings")
        self.tree.pack(fill="both", expand=True)
        for col in cols:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

    def load_data(self):
        self.bookings = self.manager.load_all()
        self.apply_filter_sort()

    def apply_filter_sort(self):
        data = self.bookings.copy()
        tier = self.filter_var.get()
        if tier != "All":
            data = [x for x in data if x["tier"] == tier]
        reverse = self.sort_dir.get() == "Descending"
        col = self.sort_col.get()
        try:
            data.sort(key=lambda x: x[col], reverse=reverse)
        except:
            data.sort(key=lambda x: str(x[col]), reverse=reverse)
        self.filtered = data
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.filtered:
            self.tree.insert(
                "",
                "end",
                values=(
                    b["id"],
                    b["tier"],
                    b["adults"],
                    b["children"],
                    f"{b['subtotal']:.2f}",
                    f"{b['discount']:.2f}",
                    f"{b['final']:.2f}",
                ),
            )

    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "No booking selected")
            return None
        values = self.tree.item(sel[0])["values"]
        return {
            "id": int(values[0]),
            "tier": values[1],
            "adults": int(values[2]),
            "children": int(values[3]),
        }

    # ---------- CRUD ---------- #
    def add_booking(self):
        self.current_edit = None
        self.show_form()

    def edit_booking(self):
        sel = self.get_selected()
        if not sel:
            return
        self.current_edit = sel
        self.show_form(sel)

    def delete_booking(self):
        sel = self.get_selected()
        if not sel:
            return
        if messagebox.askyesno("Confirm", "Delete selected booking?"):
            self.bookings = [b for b in self.bookings if b["id"] != sel["id"]]
            self.manager.overwrite_all(self.bookings)
            self.load_data()

    # ---------- FORM ---------- #
    def create_form_frame(self):
        self.form_frame = ttk.Frame(self.root)
        # Form variables
        self.tier_var = tk.StringVar(value="standard")
        self.adults_var = tk.IntVar(value=1)
        self.children_var = tk.IntVar(value=0)
        # Widgets
        ttk.Label(self.form_frame, text="Tier").pack()
        ttk.Combobox(
            self.form_frame,
            textvariable=self.tier_var,
            values=list(PRICES),
            state="readonly",
        ).pack()
        ttk.Label(self.form_frame, text="Adults").pack()
        ttk.Entry(self.form_frame, textvariable=self.adults_var).pack()
        ttk.Label(self.form_frame, text="Children").pack()
        ttk.Entry(self.form_frame, textvariable=self.children_var).pack()
        ttk.Button(self.form_frame, text="Save", command=self.save_form).pack(pady=10)
        ttk.Button(self.form_frame, text="Cancel", command=self.show_table).pack()

    def show_form(self, booking=None):
        self.table_frame.pack_forget()
        if booking:
            self.tier_var.set(booking["tier"])
            self.adults_var.set(booking["adults"])
            self.children_var.set(booking["children"])
        else:
            self.tier_var.set("standard")
            self.adults_var.set(1)
            self.children_var.set(0)
        self.form_frame.pack(fill="both", expand=True)

    def show_table(self):
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True)

    def save_form(self):
        tier = self.tier_var.get()
        adults = self.adults_var.get()
        children = self.children_var.get()
        subtotal, discount, final = calculate_booking(tier, adults, children)

        if self.current_edit:
            # Edit
            for b in self.bookings:
                if b["id"] == self.current_edit["id"]:
                    b.update(
                        {
                            "tier": tier,
                            "adults": adults,
                            "children": children,
                            "subtotal": subtotal,
                            "discount": discount,
                            "final": final,
                        }
                    )
        else:
            # Add
            new = {
                "id": self.manager.get_next_id(),
                "tier": tier,
                "adults": adults,
                "children": children,
                "subtotal": subtotal,
                "discount": discount,
                "final": final,
            }
            self.bookings.append(new)

        self.manager.overwrite_all(self.bookings)
        self.load_data()
        self.show_table()


# ---------------- MAIN ---------------- #
def main():
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
