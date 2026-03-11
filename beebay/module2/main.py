import csv
from pathlib import Path

CSV_FIELDS = (
    "num_workers",
    "num_queens",
    "distance_km",
    "bonus_code",
    "final_cost",
)
CSV_FILENAME = "sales.csv"


def create_csv():
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS,
        )
        writer.writeheader()


def save_bee(bee):
    with open(CSV_FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=CSV_FIELDS,
        )
        writer.writerow(
            {
                "num_workers": str(bee["num_workers"]),
                "num_queens": str(bee["num_queens"]),
                "distance_km": str(bee["distance_km"]),
                "bonus_code": bee["bonus_code"],
                "final_cost": str(bee["final_cost"]),
            }
        )


def check_queen_count(new_queens):
    """
    Check if adding new_queens would exceed the daily limit of 10.
    Returns True if safe, False if limit exceeded.
    """
    total_queens = 0
    if not Path(CSV_FILENAME).exists():
        return True

    with open(CSV_FILENAME, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_queens += int(row["num_queens"])

    return (total_queens + new_queens) <= 10


def get_valid_code():
    valid_codes = ("SALE", "FREEPOST", "HALFPOST")

    while True:
        bonus_code = (
            input("Bonus code (SALE / FREEPOST / HALFPOST or blank): ").upper().strip()
        )

        if bonus_code not in valid_codes and bonus_code != "":
            print("Invalid value! Please try again.\n")
        else:
            break

    return bonus_code


def get_valid_bees(input_txt):
    while True:
        num_bees = input(input_txt)

        try:
            num_bees = int(num_bees)
        except ValueError:
            print("Invalid value! Please try again.\n")
            continue

        if num_bees < 0:
            print("Invalid value! Please try again.\n")
        else:
            break

    return num_bees


def get_valid_distance():
    while True:
        num_kms = input("Delivery distance (km): ")

        try:
            num_kms = float(num_kms)
        except ValueError:
            print("Invalid value! Please try again.\n")
            continue

        if num_kms < 0:
            print("Invalid value! Please try again.\n")
        else:
            break

    return num_kms


def calculate_post(distance_km):
    """
    Determine postage cost based on delivery distance.

    Distance rules:
    - up to 50 km      -> $10
    - up to 150 km     -> $20
    - 150 km or more   -> $30
    """

    if distance_km <= 50:
        return 10
    elif distance_km <= 150:
        return 20
    else:
        return 30


def main():
    if not Path(CSV_FILENAME).exists():
        create_csv()

    # --- constants ---
    worker_price = 0.05
    queen_price = 15.00
    queen_surcharge_rate = 0.125

    print("BeeBay Order Cost Calculator")
    print("-----------------------------")

    # --- input ---
    num_workers = get_valid_bees("Number of worker bees: ")
    num_queens = get_valid_bees("Number of queen bees: ")
    distance_km = get_valid_distance()
    bonus_code = get_valid_code()

    # --- queen stock check ---
    can_save = True
    if num_queens > 10:
        can_save = False
    elif num_queens > 0:
        can_save = check_queen_count(num_queens)

    if not can_save:
        print("Queen count exceeds daily limit")
        return

    # --- processing ---
    worker_cost = num_workers * worker_price
    queen_cost = num_queens * queen_price
    bee_subtotal = worker_cost + queen_cost

    if num_queens > 0:
        surcharge_amount = bee_subtotal * queen_surcharge_rate
    else:
        surcharge_amount = 0

    postage_cost = calculate_post(distance_km)

    if bonus_code == "FREEPOST":
        postage_cost = 0
    elif bonus_code == "HALFPOST":
        postage_cost /= 2

    subtotal = bee_subtotal + surcharge_amount + postage_cost

    if bonus_code == "SALE":
        discount_amount = subtotal * 0.1
    else:
        discount_amount = 0

    final_cost = subtotal - discount_amount

    # --- output ---
    print()
    print("Order Summary")
    print("-----------------------------")

    print(f"Bee subtotal:   ${bee_subtotal:.2f}")
    print(f"Surcharge:      ${surcharge_amount:.2f}")
    print(f"Postage:        ${postage_cost:.2f}")
    print(f"Discount:       ${discount_amount:.2f}")
    print(f"Final total:    ${final_cost:.2f}")

    # --- save to CSV ---
    save_bee(
        {
            "num_workers": num_workers,
            "num_queens": num_queens,
            "distance_km": round(distance_km),
            "bonus_code": bonus_code,
            "final_cost": f"{final_cost:.2f}",  # always ends with a .00
        }
    )


if __name__ == "__main__":
    main()
