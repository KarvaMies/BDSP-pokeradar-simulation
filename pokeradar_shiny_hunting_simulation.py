import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import sys
import shutil

def end_menu(data_total, data_avg, shinies, hunt):
    choice = '-1'
    while choice != '0':
        print("\nWhat would you like to do?")
        if hunt:
            print("1) See the total time spent shiny hunting")
        print("2) See the total time spent of all data sets")
        if hunt:
            print("3) See the chart of average time spent/shiny")
        print("4) See the chart of average time spent/shiny for all the data sets")
        if os.listdir("data/"):
            print("5) Delete all data files")
        if os.path.exists("charts/avg/") or os.path.exists("charts/total/"):
            if os.listdir("charts/avg/") or os.listdir("charts/total/"):
                print("6) Delete all charts")
        print("0) Exit\n")
        choice = input("Your choice: ").strip()

        try:
            if choice == '1' and hunt:
                time_spent_chart(data_total, -1, shinies)
            elif choice == '2':
                time_spent_all_chart(data_total, -1, hunt)
            elif choice == '3' and hunt:
                time_spent_chart(-1, data_avg, shinies)
            elif choice == '4':
                time_spent_all_chart(-1, data_avg, hunt)
            elif os.listdir("data/") and choice == '5':
                delete_files("data/")
            elif (os.listdir("charts/avg/") or os.listdir("charts/total/")) and choice == '6':
                delete_files("charts/")
            elif choice == '0':
                print("Exiting the program..")
                sys.exit(0)
            else:
                print("Invalid input. Please enter valid choice\n")
        except FileNotFoundError:
            print("Why would you try to delete files that you just moved or deleted?")

def time_spent_chart(total, avg, n):
    plt.figure(figsize=(10, 6))
    if total == -1:
        x_values = np.arange(len(avg))
        plt.plot(x_values, avg, marker='o', label="Average Times")
        if n == 1:
            plt.legend(["Total time"])
        else:
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

    if not os.path.exists('charts'):
        os.makedirs('charts')
    if not os.path.exists('charts/total'):
        os.makedirs('charts/total')
    if not os.path.exists('charts/total'):
        os.makedirs('charts/avg')
    if total == -1:
        if n == 1:
            filename = f"charts/avg/time_for_1_shiny_per_chain.png"
        else:
            filename = f"charts/avg/avg_time_for_{n}_shinies_per_chain.png"
    elif avg == -1:
        if n == 1:
            filename = f"charts/total/time_for_1_shiny_per_chain.png"
        else:
            filename = f"charts/total/avg_time_for_{n}_shinies_per_chain.png"
    else:
        print("If you see this something really weird happened. Check the code!")
        print("Exiting program..")
        sys.exit(1)
    plt.savefig(filename, dpi=300)
    plt.show()

def time_spent_all_chart(total, avg, hunt):
    data_matches = False
    plt.figure(figsize=(10, 6))
    try:
        if total == -1:
            if hunt:
                time_data = str(avg)
                x_values = np.arange(len(avg))
            with open("data/avg_time_data.txt", "r") as file:
                lines = file.readlines()
        elif avg == -1:
            if hunt:
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
    legend_marker = 0   # Tracks line number from file
    legend_num_list = []
    skip_first_line = True
    for line in lines:
        if skip_first_line: # Metadata line
            legend_marker += 1
            skip_first_line = False
            continue

        line = line.strip()
        if not line:    # Empty line
            legend_marker += 1
            continue
        legend_num_list.append(legend_marker)

        if hunt and line == str(time_data):
            data_matches = True
    
        line = line.strip().strip('[]').split(',')
        line = [int(item.strip()) for item in line]
        data.append(line)
        legend_marker += 1

    if not hunt:
        x_values = np.arange(len(data[0]))
    
    if not data_matches and hunt:
        time_data = time_data.strip().strip('[]').split(',')
        time_data = [int(item.strip()) for item in time_data]
        data.append(time_data)

    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker='o', label=f"Chain {i + 1}")
    
    legend_labels = []
    legend_nums = ""
    if total == -1:
        for n in legend_num_list:
            legend_nums = f"{legend_nums}_{str(n)}"
            if n == 1:
                legend_labels.append("Time spent looking for a shiny")
            else:
                legend_labels.append(f"Average time spent / shiny for {n} shinies")
    elif avg == -1:
        for n in legend_num_list:
            legend_nums = f"{legend_nums}_{str(n)}"
            if n == 1:
                legend_labels.append("Time spent looking for a shiny")
            else:
                legend_labels.append(f"Total time for {n} shinies")
    if legend_nums.startswith("_"):
        legend_nums = legend_nums[1:]

    plt.legend(legend_labels)
    plt.xlabel("Chain Number")
    plt.ylabel("Time (minutes)")
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.ylim(bottom=0)
    
    if not os.path.exists('charts'):
        os.makedirs('charts')
    if not os.path.exists('charts/total'):
        os.makedirs('charts/total')
    if not os.path.exists('charts/avg'):
        os.makedirs('charts/avg')
    if total == -1:
        filename = f"charts/avg/avg_time_for_{legend_nums}_shinies_per_chain.png"
    elif avg == -1:
        filename = f"charts/total/total_time_for_{legend_nums}_shinies_per_chain.png"
    plt.savefig(filename, dpi=300)
    plt.show()

def delete_files(src_folder):
    cont = input(f"Are you sure you want to delete all contents inside '{src_folder}' folder? (y/n) ").strip()
    while cont.lower() not in ('y', 'n'):
        print("Invalid input. Please enter 'y' or 'n'\n")
        cont = input(f"Are you sure you want to delete all the files inside '{src_folder}' folder? (y/n) ").strip()
    
    if cont.lower() == 'y':
        dest_folder = f"deleted/{src_folder}"
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        timestamp = datetime.now().strftime("%d.%m.%Y_%H-%M")
        for src_dir, dirs, files in os.walk(src_folder):
            dst_dir = src_dir.replace(src_folder, dest_folder)
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)

                file_name, extension = os.path.splitext(file_)
                name = f"{file_name}_{timestamp}{extension}"
                file = os.path.join(dst_dir, name)
                os.rename(dst_file, file)
        print(f"Contents from '{src_folder}' are now moved to '{dest_folder}'.")
        print("If you want to permanently delete the files, please do it manually.")

def main():
    MAX_CHAIN = 40
    SAMPLE_SIZE = 5000
    num_of_shinies = 0

    print("Welcome to Pokéradar shiny hunting simulation tool for Pokémon Brilliand Diamond and Shining Pearl!\n")

    if os.path.exists("data/avg_time_data.txt") and os.path.exists("data/total_time_data.txt"):
        while True:
            print("What would you like to do?")
            print("1) Simulate shiny hunting")
            print("2) Inspect and analyze existing data")
            choice = input("Your choice: ").strip()

            if choice == '1':
                break
            elif choice == '2':
                end_menu(0, 0, -1, False)
            else:
                print("Invalid input. Please enter '1' or '2'\n")

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

    print(f"Total time spent:\n{total_times}")
    print(f"Avg time spent/shiny:\n{avg_times}")
    save_data(total_times, avg_times, num_of_shinies)
    end_menu(total_times, avg_times, num_of_shinies, True)

def save_data(total, avg, n):
    try:
        with open("data/total_time_data.txt", "r") as total_file:
            total_lines = total_file.readlines()
        with open("data/avg_time_data.txt", "r") as avg_file:
            avg_lines = avg_file.readlines()
    except FileNotFoundError:
        with open("data/total_time_data.txt", "w") as total_file:
            total_file.write("METADATA: row number = number of shinies hunted\n")
        with open("data/avg_time_data.txt", "w") as avg_file:
            avg_file.write("METADATA: row number = number of shinies hunted\n")
        

    if n < len(total_lines):
        total_lines[n] = str(total) + "\n"
        avg_lines[n] = str(avg) + "\n"
    else:
        total_lines.extend(["\n"] * (n - len(total_lines)))
        total_lines.append(str(total) + "\n")

        avg_lines.extend(["\n"] * (n - len(avg_lines)))
        avg_lines.append(str(avg) + "\n")

    with open("data/total_time_data.txt", "w") as total_file:
        total_file.writelines(total_lines)

    with open("data/avg_time_data.txt", "w") as avg_file:
        avg_file.writelines(avg_lines)

if __name__ == "__main__":
    main()