numbers = []

while True:
    try:
        num = int(input("Enter number (or enter nothing to exit): "))
    except ValueError:
        break

    numbers.append(num)

if numbers:
    print(f"Total: {len(numbers)}")
    print(f"Sum: {sum(numbers)}")
    print(f"Mean: {(sum(numbers) / len(numbers)):.2f}")
else:
    print("No valid numbers")
