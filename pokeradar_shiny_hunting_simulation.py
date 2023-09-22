import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import sys

def end_menu(data_total, data_avg, shinies):
    choice = '-1'
    while choice != '0':
        print("\nWhat would you like to do?")
        print("1) See the total time spent shiny hunting")
        print("2) See the total time spent of all data sets")
        print("3) See the chart of average time spent/shiny")
        print("4) See the chart of average time spent/shiny for all the data sets")
        print("0) Exit\n")
        choice = input("Your choice: ").strip()

        if choice == '1':
            time_spent_chart(data_total, -1, shinies)
        elif choice == '2':
            time_spent_all_chart(data_total, -1)
        elif choice == '3':
            time_spent_chart(-1, data_avg, shinies)
        elif choice == '4':
            time_spent_all_chart(-1, data_avg)
        elif choice == '0':
            pass
        else:
            print("Invalid input. Please enter '1', '2' or '0'\n")
    print("Exiting the program..")

def time_spent_chart(total, avg, n):
    if total == -1:
        x_values = np.arange(len(avg))
        plt.plot(x_values, avg, marker='o', label="Average Times")
        plt.legend(["Average time / shiny"])
    elif avg == -1:
        x_values = np.arange(len(total))
        plt.plot(x_values, total, marker='o', label="Total Times")
        plt.legend(["Total time"])
    else:
        print("Unexpected data encountered while trying to draw a chart. Check the code.")
        print("Exiting program..")
        sys.exit(1)
        
    plt.ylabel("Time (minutes)")
    plt.xlabel("Chain Number")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.ylim(bottom=0)

    save = input("Would you like to save the chart? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Would you like to save the chart? (y/n) ").strip()

    if save.lower() == 'y':
        if not os.path.exists('charts'):
            os.makedirs('charts')
        if not os.path.exists('charts/total'):
            os.makedirs('charts/total')
        if not os.path.exists('charts/total'):
            os.makedirs('charts/avg')
        timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        if total == -1:
            if n == 1:
                filename = f"charts/avg/time_for_a_shiny_per_chain_{timestamp}.png"
            else:
                filename = f"charts/avg/time_for_{n}_shinies_per_chain_{timestamp}.png"
        elif avg == -1:
            if n == 1:
                filename = f"charts/total/time_for_a_shiny_per_chain_{timestamp}.png"
            else:
                filename = f"charts/total/time_for_{n}_shinies_per_chain_{timestamp}.png"
        else:
            print("If you see this something really weird happened. Check the code!")
            print("Exiting program..")
            sys.exit(1)
        plt.savefig(filename)
    plt.show()

def time_spent_all_chart(total, avg):
    data_matches = False
    try:
        if total == -1:
            time_data = str(avg)
            x_values = np.arange(len(avg))
            with open("data/avg_time_data.txt", "r") as file:
                lines = file.readlines()
        elif avg == -1:
            time_data = str(total)
            x_values = np.arange(len(total))
            with open("data/total_time_data.txt", "r") as file:
                lines = file.readlines()
        else:
            print("Unexpected data encountered while trying to draw a chart. Check the code.")
            print("Exiting program..")
            sys.exit(1)
    except FileNotFoundError:
        print("Could not find the data file. Make sure you save the data to the file first.")
        return
    
    data = []
    for line in lines:
        if line == str(time_data):
            data_matches = True
    
        line = line.strip().strip('[]').split(',')
        line = [int(item.strip()) for item in line]
        data.append(line)
    
    if not data_matches:
        time_data = time_data.strip().strip('[]').split(',')
        time_data = [int(item.strip()) for item in time_data]
        data.append(time_data)

    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker='o', label=f"Chain {i + 1}")
    
    if total == -1:
        plt.legend([f"Average time spent / shiny for {i + 1} shinies" if i > 0 else f"Time spent looking for a shiny" for i in range(len(data))])
    elif avg == -1:
        plt.legend([f"Total time for {i + 1} shinies" if i > 0 else f"Time spent looking for a shiny" for i in range(len(data))])

    plt.xlabel("Chain Number")
    plt.ylabel("Time (minutes)")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.ylim(bottom=0)

    save = input("Would you like to save the chart? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Would you like to save the chart? (y/n) ").strip()
    
    if save.lower() == 'y':
        if not os.path.exists('charts'):
            os.makedirs('charts')
        if not os.path.exists('charts/total'):
            os.makedirs('charts/total')
        if not os.path.exists('charts/total'):
            os.makedirs('charts/avg')
        timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        if total == -1:
            filename = f"charts/avg/time_for_shinies_per_chain_all_data_{timestamp}.png"
        if avg == -1:
            filename = f"charts/total/time_for_shinies_per_chain_all_data_{timestamp}.png"
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

    SAMPLE_SIZE = 50#00 //TODO poista kommentit tästä
    odds = [4096, 3855, 3640, 3449, 3277, 3121, 2979, 2849, 2731, 2621,
            2521, 2427, 2341, 2259, 2185, 2114, 2048, 1986, 1927, 1872,
            1820, 1771, 1724, 1680, 1638, 1598, 1560, 1524, 1489, 1456,
            1310, 1285, 1260, 1236, 1213, 1192, 993, 799, 400, 200, 99]
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

        total_times.append(round(local_time / (60 * SAMPLE_SIZE)))
        avg_times.append(round(local_time / (60 * SAMPLE_SIZE * num_of_shinies)))

    print(f"Total time spent:\n{total_times}") #TODO posita tää ja alempi printti
    print(f"Avg time spent/shiny:\n{avg_times}")

    save = input("Do you want to save this data to a file? (y/n) ").strip()
    while save.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        save = input("Do you want to save this data? (y/n) ").strip()
    if save.lower() == 'y':
        with open("data/total_time_data.txt", "a") as file:
            file.write(str(total_times) + "\n")
        with open("data/avg_time_data.txt", "a") as file:
            file.write(str(avg_times) + "\n")

    end_menu(total_times, avg_times, num_of_shinies)

if __name__ == "__main__":
    main()