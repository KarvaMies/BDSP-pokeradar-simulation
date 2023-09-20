import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def end_menu(data, shinies):
    choice = '-1'
    while choice != '0':
        print("\nWhat would you like to do?")
        print("1) See the chart of this data set")
        print("2) See the chart of all of the data sets together")
        print("0) Exit\n")
        choice = input("Your choice: ").strip()

        if choice == '1':
            chart_of_one(data, shinies)
        elif choice == '2':
            chart_of_all(data)
        elif choice == '0':
            pass
        else:
            print("Invalid input. Please enter '1', '2' or '0'\n")
    print("Exiting the program..")

def chart_of_one(total_times, shinies):
    x_values = np.arange(len(total_times))

    plt.plot(x_values, total_times, marker='o', label="Total Times")

    plt.xlabel("Chain Number")
    plt.ylabel("Time (minutes)")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.legend(["Avg time/shiny"])

    save = input("Would you like to save the chart? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Would you like to save the chart? (y/n) ").strip()

    if save.lower() == 'y':
        if not os.path.exists('charts'):
            os.makedirs('charts')
        timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        if shinies == 1:
            filename = f"charts/avg_time_for_a_shiny_per_chain_{timestamp}.png"
        else:
            filename = f"charts/avg_time_for_{shinies}_shinies_per_chain_{timestamp}.png"
        plt.savefig(filename)
    plt.show()

def chart_of_all(total_times):
    original_data = [ #might want to delete this
        161, 154, 146, 140, 135, 129, 126, 122, 120, 116, 114, 112, 111, 111, 110, 109, 109, 109, 111, 111, 112, 114, 115, 119, 120, 122, 127, 130, 135, 134, 138, 144, 149, 155, 161, 162, 163, 159, 161, 168
    ]
    data_matches = False

    with open("data/raw_data.txt", "r") as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        if line == str(total_times):
            data_matches = True
    
        line = line.strip().strip('[]').split(',')
        line = [int(item.strip()) for item in line]
        data.append(line)
    
    if not data_matches:
        total_times = str(total_times)
        total_times = total_times.strip().strip('[]').split(',')
        total_times = [int(item.strip()) for item in total_times]
        data.append(total_times)

    x_values = np.arange(len(original_data))
    plt.plot(x_values, original_data, marker='o', label="Test data")
    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker='o', label=f"Chain {i + 1}")

    plt.xlabel("Chain Number")
    plt.ylabel("Time (minutes)")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.legend(["Test data"] + [f"Avg min/shiny dataset {i + 1}" for i in range(len(data))])

    save = input("Would you like to save the chart? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Would you like to save the chart? (y/n) ").strip()
    
    if save.lower() == 'y':
        if not os.path.exists('charts'):
            os.makedirs('charts')
        timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        filename = f"charts/avg_time_for_shinies_per_chain_all_data_{timestamp}.png"
        plt.savefig(filename)
    plt.show()

def main():
    MAX_CHAIN = 40

    num_of_shinies = 0
    while True:
        num_of_shinies = input("How many shinies do you plan to hunt? ").strip()
        if num_of_shinies.isdigit():
            num_of_shinies = int(num_of_shinies)
            if num_of_shinies >= 1:
                break
            else:
                print("Please enter a number greater than or equal to 1.\n")
        else:
            print("Please enter a valid integer.\n")

    SAMPLE_SIZE = 5000
    odds = [4096, 3855, 3640, 3449, 3277, 3121, 2979, 2849, 2731, 2621,
            2521, 2427, 2341, 2259, 2185, 2114, 2048, 1986, 1927, 1872,
            1820, 1771, 1724, 1680, 1638, 1598, 1560, 1524, 1489, 1456,
            1310, 1285, 1260, 1236, 1213, 1192, 993, 799, 400, 200, 99]
    total_times = []

    for local_chain in tqdm(range(1, MAX_CHAIN + 1), desc="Chain progress", ncols=100):
        local_time = 0
        for _ in range(SAMPLE_SIZE):
            current_chain = 0
            found_shinies = 0
            found_all_shinies = False

            while current_chain < local_chain and not found_all_shinies:
                if found_all_shinies:
                    break
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

        total_times.append(round(local_time / (60 * SAMPLE_SIZE * num_of_shinies)))

    print(total_times)

    save = input("Do you want to save this data to a file? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Do you want to save this data? (y/n) ").strip()
    if save.lower() == 'y':
        with open("data/raw_data.txt", "a") as file:
            file.write(str(total_times) + "\n")

    end_menu(total_times, num_of_shinies)

if __name__ == "__main__":
    main()