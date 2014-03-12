def largest_prime_factor(z):
    x = 2
    counter = 2
    factor_list = []
    value = 0
    for x in range(2,(int(z ** .5) + 1)):
        if z % x == 0:
            factor_list.extend([int((z/x)), x])
    factor_list = sorted(list(set(factor_list)), reverse = True)
    for foo in factor_list:
        value = 0
        for counter in range(2,(int(foo ** .5) + 1)):
            if foo % counter == 0:
                value += 1
        if value == 0:
            print(foo)
            break

            
