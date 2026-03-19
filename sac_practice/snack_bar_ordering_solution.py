total_cost = 0

while True:
    item = input("Enter item (HOTDOG, BURGER, DRINK, or DONE to exit): ").upper()

    if item == "DONE":
        break

    if item == "HOTDOG":
        total_cost += 4.5
    elif item == "BURGER":
        total_cost += 6
    elif item == "DRINK":
        total_cost += 2.5
    else:
        print("Invalid item!\n")
        continue

    print(f"Added {item}!\n")

if total_cost > 20:
    discount = total_cost * 0.1
else:
    discount = 0

final_cost = total_cost - discount
print(f"Final cost: {final_cost:.2f}")
