distance = float(input("Enter delivery distance (km): "))
weight = float(input("Enter package weight (kg): "))
express = input("Express delivery (Y/N): ").upper() == "Y"

# Distance cost
if distance <= 5:
    base_cost = 6
elif distance <= 15:
    base_cost = 10
else:
    base_cost = 18

# Weight surcharge
if weight <= 2:
    weight_charge = 0
elif weight <= 5:
    weight_charge = 4
else:
    weight_charge = 10

final_cost = base_cost + weight_charge

if express:
    final_cost += 8

print("Delivery cost:", final_cost)
