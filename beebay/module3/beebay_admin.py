import tkinter as tk
from tkinter import ttk
from pathlib import Path
import csv


class BeeBayAdmin(ttk.Frame):
    """
    Admin interface for viewing BeeBay order data.

    The program loads sales data from a CSV files and allows filtering
    orders based on the amount of queen bee purchases and sorting by
    cost or delivery distance.
    """

    def __init__(self, parent: tk.Tk):
        """Initializes the BeeBayAdmin interface and sets up the UI."""

        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="NSEW")

        # CSV headers and fields in table (excluding sale_id)
        self.fields = (
            "sale_id",
            "num_workers",
            "num_queens",
            "distance_km",
            "bonus_code",
            "final_cost",
        )

        # Dropdown valid values
        self.filter_values = ("Orders with queens", "Orders with no queens")
        self.sort_values = ("Cost", "Distance")

        self.filter_var = tk.StringVar(value=self.filter_values[0])
        self.sort_var = tk.StringVar(value=self.sort_values[0])

        self.setup_grid()
        self.create_widgets()

        BASE_DIR = Path(__file__).resolve().parent
        self.sales_csv = BASE_DIR / "sales.csv"

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

    def create_widgets(self):
        lbl_heading = ttk.Label(self, text="BeeBay Admin", font=("Arial", 16, "bold"))
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="W", pady=(0, 15))

        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="W", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=self.filter_values,
        )
        cbo_filter.grid(row=1, column=1, sticky="EW", pady=5)

        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="W", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=self.sort_values,
        )
        cbo_sort.grid(row=2, column=1, sticky="EW", pady=5)

        btn_go = ttk.Button(self, text="Load Results", command=self.load_results)
        btn_go.grid(row=2, column=2, sticky="W", padx=(10, 0), pady=5)

        self.tree = ttk.Treeview(self, columns=self.fields, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="NSEW", pady=(10, 0))

        headings = {
            "sale_id": "Sale ID",
            "num_workers": "Workers",
            "num_queens": "Queens",
            "distance_km": "Distance (km)",
            "bonus_code": "Bonus Code",
            "final_cost": "Final Cost",
        }

        widths = {
            "sale_id": 90,
            "num_workers": 90,
            "num_queens": 90,
            "distance_km": 120,
            "bonus_code": 120,
            "final_cost": 100,
        }

        for col in self.fields:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="NS", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.parent.bind("<Return>", self.load_results)

    def load_csv(self) -> list:
        """
        Load order data from the sales CSV file.

        If the file does not exist, it is created with the correct column
        headers before reading.

        Returns:
            list: A list of order dictionaries
        """

        if not self.sales_csv.exists():
            with open(self.sales_csv, mode="w", newline="", encoding="utf-8") as file:
                # Create CSV file with no data other than headers
                writer = csv.DictWriter(
                    file,
                    fieldnames=self.fields,
                )
                writer.writeheader()

        data = []
        with open(self.sales_csv, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert data to valid data types corresponding to the value and add to data
                data.append(
                    {
                        "sale_id": int(row.get("sale_id", "")),
                        "num_workers": int(row.get("num_workers", "")),
                        "num_queens": int(row.get("num_queens", "")),
                        "distance_km": float(row.get("distance_km", "")),
                        "bonus_code": row.get("bonus_code", ""),
                        "final_cost": float(row.get("final_cost", "")),
                    }
                )

        return data

    def filter_rows(self, data: list, queen_filter: bool) -> list:
        """
        Filter orders depending on whether they contain queen bees.

        Parameters:
            data (list): List of order dictionaries
            queen_filter (bool): True if orders with queens should be shown

        Returns:
            list: Filtered order list
        """

        if queen_filter:
            # Return only orders that contain at least one queen
            return [row for row in data if row["num_queens"] > 0]
        else:
            return [row for row in data if row["num_queens"] == 0]

    def sort_rows(self, data: list, sorter: str) -> list:
        """
        Sort orders based on either total cost or distance kilometers, in descending order.

        Parameters:
            data (list): List of order dictionaries
            sorter (str): The sorting criteria, either 'cost' or 'distance'

        Returns:
            list: Sorted order list

        Raises:
            TypeError: If the sorting criteria does not match 'cost' or 'distance'
        """

        if sorter == "cost":
            return sorted(data, key=lambda row: row["final_cost"], reverse=True)
        elif sorter == "distance":
            return sorted(data, key=lambda row: row["distance_km"], reverse=True)
        else:
            # Raise error if an unsupported sorting criteria is provided
            raise TypeError(f"Sort option {sorter} does not exist")

    def refresh_tree(self, data: list):
        """
        Show data in the treeview by clearing all existing rows and re-adding them to UI.

        Parameters:
            data (list): List of order dictionaries
        """

        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row["sale_id"],
                    row["num_workers"],
                    row["num_queens"],
                    row["distance_km"],
                    row["bonus_code"],
                    row["final_cost"],
                ),
            )

    def load_results(self, _=None):
        """Load, filter, sort, and display sales data in the treeview."""

        # Load file for reading
        data = self.load_csv()

        # Filter by queens
        queen_filter = self.filter_var.get().lower() == self.filter_values[0].lower()
        data = self.filter_rows(data, queen_filter)

        # Sort by either cost or distance
        sorter = self.sort_var.get().lower()
        data = self.sort_rows(data, sorter)

        # Display data
        self.refresh_tree(data)


def main():
    """Create the main window and run the BeeBayAdmin application."""

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")

    BeeBayAdmin(root)
    root.mainloop()


if __name__ == "__main__":
    main()
