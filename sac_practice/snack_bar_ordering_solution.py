total_cost = 0

while True:
    item = input("Enter item (HOTDOG, BURGER, DRINK) or DONE: ").upper()

    if item == "DONE":
        break

    if item == "HOTDOG":
        total_cost += 4.50
    elif item == "BURGER":
        total_cost += 6.00
    elif item == "DRINK":
        total_cost += 2.50
    else:
        print("Invalid item")

discount = 0
if total_cost > 20:
    discount = total_cost * 0.10

final_total = total_cost - discount

print("Final total:", round(final_total, 2))
