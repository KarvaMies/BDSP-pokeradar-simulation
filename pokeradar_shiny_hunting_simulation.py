import random

MAX_CHAIN = 40

num_of_shinies = int(input("How many shinies you plan to hunt? "))

SAMPLE_SIZE = 30000 # How many times the # of shinies are hunted for each chain
odds = [4096, 3855, 3640, 3449, 3277, 3121, 2979, 2849, 2731, 2621,
        2521, 2427, 2341, 2259, 2185, 2114, 2048, 1986, 1927, 1872,
        1820, 1771, 1724, 1680, 1638, 1598, 1560, 1524, 1489, 1456,
        1310, 1285, 1260, 1236, 1213, 1192, 993, 799, 400, 200, 99]
total_times = []

for local_chain in range(1, MAX_CHAIN + 1):
    local_time = 0
    found_shinies = 0
    for _ in range(SAMPLE_SIZE):
        current_chain = 0
        found_all_shinies = False

        while current_chain < local_chain and not found_all_shinies:
            patches = [random.randint(1, odds[current_chain]) for _ in range(4)]
            if 1 in patches:
                found_shinies += 1
                if found_shinies >= num_of_shinies:
                    found_all_shinies = True

            if not found_all_shinies:
                continue_chain = random.randint(1, 100) <= 93
                if continue_chain:
                    current_chain += 1
                    local_time += 50
                else:
                    current_chain = 0
                    local_time += 100

            while current_chain >= local_chain and not found_all_shinies:
                local_chain_copy = local_chain
                local_time += 10
                patches = [random.randint(1, odds[local_chain_copy]) for _ in range(4)]
                if 1 in patches:
                    found_shinies += 1
                    if found_shinies >= num_of_shinies:
                        found_all_shinies = True

                if not found_all_shinies:
                    continue_chain = random.randint(1, 100) <= 93
                    if continue_chain:
                        if local_chain_copy < MAX_CHAIN:
                            local_chain_copy += 1
                        local_time += 50
                    else:
                        current_chain = 0
                        local_time += 100

    total_times.append(local_time / (60 * SAMPLE_SIZE))

print(total_times)