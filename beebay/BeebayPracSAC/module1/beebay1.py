# beebay_cli.py

def calculate_post(distance_km):
    """
    Determine postage cost based on delivery distance.

    TODO:
    Implement the distance rules:
        up to 50 km      -> $10
        up to 150 km     -> $20
        150 km or more   -> $30
    """

    postage_cost = 0

    # TODO: determine postage_cost using distance_km

    return postage_cost


def main():

    # --- constants ---
    worker_price = 0.05
    queen_price = 15.00
    queen_surcharge_rate = 0.125

    print("BeeBay Order Cost Calculator")
    print("-----------------------------")

    # --- input ---
    num_workers = int(input("Number of worker bees: "))
    num_queens = int(input("Number of queen bees: "))
    distance_km = float(input("Delivery distance (km): "))
    bonus_code = input("Bonus code (SALE / FREEPOST / HALFPOST or blank): ").upper()

    # --- processing ---

    # TODO: calculate worker_cost
    worker_cost = 0

    # TODO: calculate queen_cost
    queen_cost = 0

    # TODO: calculate bee_subtotal
    bee_subtotal = 0

    # TODO: calculate queen surcharge amount if queen bees are ordered
    surcharge_amount = 0

    # TODO: determine postage using calculate_post()
    postage_cost = 0

    # TODO: adjust postage if bonus code is FREEPOST or HALFPOST

    # TODO: calculate subtotal including bees, surcharge and postage
    subtotal = 0

    # TODO: calculate discount amount if bonus code is SALE
    discount_amount = 0

    # TODO: calculate final total
    final_cost = 0

    # --- output ---
    print()
    print("Order Summary")
    print("-----------------------------")

    print("Bee subtotal:   $", bee_subtotal)
    print("Surcharge:      $", surcharge_amount)
    print("Postage:        $", postage_cost)
    print("Discount:       $", discount_amount)
    print("Final total:    $", final_cost)


if __name__ == "__main__":
    main()