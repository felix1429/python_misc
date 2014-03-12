calculate_to = int(input("Up to what number would you like to find primes? "))
print(1)
for x in range(2,(calculate_to + 1)):
    counter = 2
    value = 0
    for counter in range(2,(x//2)):
        if x % counter == 0:
            pass
            value += 1
    if value == 0:
        print(x)

