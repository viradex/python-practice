import tkinter as tk
from tkinter import ttk, messagebox
from models.order import Order
from repos.order_repo import OrderRepo


class OrderScreen(ttk.Frame):
    def __init__(self, parent, repo):
        super().__init__(parent, padding=20)
        self.parent = parent
        self.repo = repo  # passed from App
        self.order = None  # to use in class methods

        self.grid(row=0, column=0, sticky="nsew")

        self.num_workers_var = tk.StringVar()
        self.num_queens_var = tk.StringVar()
        self.distance_km_var = tk.StringVar()
        self.bonus_code_var = tk.StringVar()
        self.final_cost_var = tk.StringVar()

        self.setup_grid()
        self.create_widgets()

    def setup_grid(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):

        ttk.Label(self, text="BeeBay Order Entry", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

        ttk.Label(self, text="Number of worker bees:").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_workers_var).grid(
            row=1, column=1, sticky="ew", pady=5
        )

        ttk.Label(self, text="Number of queen bees:").grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.num_queens_var).grid(
            row=2, column=1, sticky="ew", pady=5
        )

        ttk.Label(self, text="Delivery distance (km):").grid(
            row=3, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.distance_km_var).grid(
            row=3, column=1, sticky="ew", pady=5
        )

        ttk.Label(self, text="Bonus code:").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Combobox(
            self,
            textvariable=self.bonus_code_var,
            state="readonly",
            values=["", "SALE", "FREEPOST", "HALFPOST"],
        ).grid(row=4, column=1, sticky="ew", pady=5)

        ttk.Label(self, text="Final cost:").grid(
            row=5, column=0, sticky="w", padx=(0, 10), pady=5
        )
        ttk.Entry(self, textvariable=self.final_cost_var, state="readonly").grid(
            row=5, column=1, sticky="ew", pady=5
        )

        ttk.Button(self, text="Calculate", command=self.calculate).grid(
            row=6, column=0, sticky="w", pady=(12, 0)
        )
        ttk.Button(self, text="Save Order", command=self.save).grid(
            row=6, column=1, sticky="e", pady=(12, 0)
        )

    def calculate(self):
        # validate inputs
        num_workers = int(self.num_workers_var.get())
        num_queens = int(self.num_queens_var.get())
        distance_km = float(self.distance_km_var.get())
        bonus_code = self.bonus_code_var.get()

        # create order object from validated values
        self.order = Order(
            num_workers,
            num_queens,
            distance_km,
            bonus_code,
            sales_id=self.repo.get_next_id(),
        )
        num_workers = int(self.num_workers_var.get().strip())
        num_queens = int(self.num_queens_var.get().strip())
        distance_km = int(self.distance_km_var.get().strip())
        bonus_code = self.bonus_code_var.get().strip()

        # create order object from validated values
        self.order = Order(num_workers, num_queens, distance_km, bonus_code)

        # calculate values
        self.order.calculate()

        # update total on screen
        self.final_cost_var.set(self.order.final_cost)

    def save(self):
        # TODO
        # call self.repo.save(self.order)
        if not self.order:
            messagebox.showerror(
                "Final Cost Not Available",
                "The final cost has not yet been calculated. Please press the Calculate button before saving data.",
            )
        else:
            self.repo.save(self.order)


def main():
    root = tk.Tk()
    root.title("BeeBay Ordering")
    root.geometry("620x320")

    OrderScreen(root)

    root.mainloop()


if __name__ == "__main__":
    main()
