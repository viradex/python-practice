def input_repeat(question, is_int=False):
    while True:
        value = input(question)

        if not value:
            print("Please enter a value!\n")
            continue

        try:
            if is_int:
                value = float(value)
        except ValueError:
            print("The value must be a number.\n")
            continue

        if is_int and value < 0:
            print("The value must be above zero.\n")
            continue

        break

    return value


try:
    distance_km = input_repeat("Enter distance in kms: ", is_int=True)
    weight_kg = input_repeat("Input weight in kgs: ", is_int=True)
    express = input_repeat("Express delivery (Y/N)? ").upper().startswith("Y")
except KeyboardInterrupt:
    print("\nExiting...")
    exit()

if distance_km <= 5:
    base_cost = 6
elif distance_km <= 15:
    base_cost = 10
else:
    base_cost = 18

if weight_kg <= 2:
    weight_charge = 0
elif weight_kg <= 5:
    weight_charge = 4
else:
    weight_charge = 10

final_cost = base_cost + weight_charge

if express:
    final_cost += 8

print(f"Final cost: ${final_cost:.2f}")
