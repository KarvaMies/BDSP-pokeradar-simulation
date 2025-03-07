import random, modules, multiprocessing
from tqdm import tqdm
from config import MAX_CHAIN, SAMPLE_SIZE, ODDS


def simulate_sample(args: list):
    """
    Runs one batch of SAMPLE_SIZE divided across processes.

    Args:
        local_chain (int): The chain length being simulated.
        n_shinies (int): The number of wanted shinies.
        sample_split (int): The number of samples this process handles.

    Returns:
        tuple[int]: (total time spent, average time per shiny)
    """
    local_chain, n_shinies, sample_split = args
    local_time = 0

    for _ in range(sample_split):
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
                patches = [random.randint(1, ODDS[local_chain_copy]) for _ in range(4)]
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

    return round(local_time / (60 * sample_split)), round(
        local_time / (60 * sample_split * n_shinies)
    )


def run_simulation(n_shinies: int):
    """
    Runs the shiny hunting simulation with multiprocesssing.

    Args:
        n_shinies: The number of shinies wanted in the hunt.

    Returns:
        None
    """
    total_times = []
    avg_times = []

    num_workers = min(multiprocessing.cpu_count() - 1, SAMPLE_SIZE)

    # Ensure exact SAMPLE_SIZE amount is simulated
    base_sample_split = SAMPLE_SIZE // num_workers
    extra_samples = SAMPLE_SIZE % num_workers
    sample_splits = [
        base_sample_split + 1 if i < extra_samples else base_sample_split
        for i in range(num_workers)
    ]

    with multiprocessing.Pool(processes=num_workers) as pool:
        for local_chain in tqdm(
            range(1, MAX_CHAIN + 1),
            desc="🔹Chain progress",
            ncols=100,
            unit="chain",
            ascii="░▒█",
            mininterval=5,
        ):
            args_list = [
                (local_chain, n_shinies, sample_splits[i]) for i in range(num_workers)
            ]
            results = pool.map(simulate_sample, args_list)

            total_chain_time = sum(r[0] for r in results)
            avg_chain_time = sum(r[1] for r in results)

            total_times.append(total_chain_time)
            avg_times.append(avg_chain_time)

    modules.save_data(total_times, avg_times, n_shinies, SAMPLE_SIZE)
