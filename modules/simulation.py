import random
from tqdm import tqdm
from data_handler import save_data


def run_simulation(MAX_CHAIN: int, SAMPLE_SIZE: int, n_shinies: int, ODDS: list):
    """
    Runs the shiny hunting simulation.

    Args:
        MAX_CHAIN: The maximum number of chains allowed in simulation (1-40)
        SAMPLE_SIZE: The number the hunt is simulated. Values over 10000 will take a lot of time
        n_shinies: The number of shinies wanted in the hunt. Values over 5 will take a lot of time
        ODDS: The list of odds to get a shiny patch with 1/ODDS[current_chain] chance

    Returns:
        total_times (list): List of total times taken for each simulation
        avg_times (list): List of average times taken per shiny for each simulation
    """
    total_times = []
    avg_times = []

    for local_chain in tqdm(range(1, MAX_CHAIN + 1), desc="Chain progress", ncols=100):
        local_time = 0
        for _ in range(SAMPLE_SIZE):
            current_chain = 0
            found_shinies = 0
            found_all_shinies = False

            while current_chain < local_chain and not found_all_shinies:
                if found_all_shinies:
                    break
                patches = [random.randint(1, ODDS[current_chain]) for _ in range(4)]
                if 1 in patches:
                    found_shinies += 1
                    if found_shinies >= n_shinies:
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
                    patches = [
                        random.randint(1, ODDS[local_chain_copy]) for _ in range(4)
                    ]
                    if 1 in patches:
                        found_shinies += 1
                        if found_shinies >= n_shinies:
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

        total_times.append(round(local_time / (60 * SAMPLE_SIZE)))
        avg_times.append(round(local_time / (60 * SAMPLE_SIZE * n_shinies)))

    print(f"Total time spent:\n{total_times}")
    print(f"Avg time spent/shiny:\n{avg_times}")
    save_data(total_times, avg_times, n_shinies, SAMPLE_SIZE)

    return total_times, avg_times
