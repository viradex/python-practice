import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import csv


class BeeBayAdmin(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.grid(row=0, column=0, sticky="nsew")

        self.filter_var = tk.StringVar(value="Orders with queens")
        self.sort_var = tk.StringVar(value="final_cost")

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
        lbl_heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        lbl_filter = ttk.Label(self, text="Filter:")
        lbl_filter.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_filter = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            state="readonly",
            values=["Orders with queens", "Orders with no queens"]
        )
        cbo_filter.grid(row=1, column=1, sticky="ew", pady=5)

        lbl_sort = ttk.Label(self, text="Sort by:")
        lbl_sort.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)

        cbo_sort = ttk.Combobox(
            self,
            textvariable=self.sort_var,
            state="readonly",
            values=["final_cost", "distance_km"]
        )
        cbo_sort.grid(row=2, column=1, sticky="ew", pady=5)

        btn_go = ttk.Button(self, text="Load Results", command=self.load_results)
        btn_go.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=5)

        columns = (
            "sale_id",
            "num_workers",
            "num_queens",
            "distance_km",
            "bonus_code",
            "final_cost"
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=(10, 0))

        headings = {
            "sale_id": "Sale ID",
            "num_workers": "Workers",
            "num_queens": "Queens",
            "distance_km": "Distance (km)",
            "bonus_code": "Bonus Code",
            "final_cost": "Final Cost"
        }

        widths = {
            "sale_id": 90,
            "num_workers": 90,
            "num_queens": 90,
            "distance_km": 120,
            "bonus_code": 120,
            "final_cost": 100
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky="ns", pady=(10, 0))

        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def load_results(self):
        #ToDo: implement search and filter code
        matches = []
        queens_match = (self.filter_var.get() == "Orders with queens")
        sort_by = self.sort_var.get()

        # 1. load file for reading
        with open(self.sales_csv, newline="", encoding="utf-8") as sales_file:
        # 2. add matching rows to a list
            for row in csv.DictReader(sales_file):
                
                if queens_match:
                    if(int(row["num_queens"])) > 0:
                        matches.append(row)
                else:
                    if(int(row["num_queens"])) == 0:
                        matches.append(row)

                #OR - there are other ways to code this
                """
                has_queens = int(row["num_queens"]) > 0
                if queens_match == has_queens:
                    matches.append(row)
                """

        # 3. sort matching list
        # sorted_matches = sorted(matches, key=lambda item_to_sort: float(item_to_sort[sort_by]))

        #OR - clearer
        def sort_key(row):
            return float(row[sort_by]) #sort_by comes directly from the input
        sorted_matches = sorted(matches, key=sort_key)

        # 4. load list to treeview
        #clear treeview first
        for i in self.tree.get_children(): 
            self.tree.delete(i)

        for row in sorted_matches:
            self.tree.insert("", tk.END, values=list(row.values()))

        #  - do you need multiple functions? 
        # - each of these could be a function - pass in the parameters, then return the list

def main():

    root = tk.Tk()
    root.title("BeeBay Admin")
    root.geometry("760x420")

    BeeBayAdmin(root)

    root.mainloop()


if __name__ == "__main__":
    main()