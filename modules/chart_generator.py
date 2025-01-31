import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from data_handler import get_SS


def time_spent_chart(total: list, avg: list, n: int, SS: int):
    """
    Draws and shows chart for simulated n number of shinies.
    Either total or avg must be an empty list.

    Args:
        total (list): List of times taken for hunts
        avg (list): List of average times taken for hunts
        n (int): Number of shinies hunted
        SS (int): Sample Size of the simulation

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    if not total and not avg:
        print(
            "Unexpected data encountered while trying to draw a chart. Check the code."
        )
        print("Exiting program..")
        sys.exit(1)
    elif avg:
        x_values = np.arange(len(avg))
        plt.plot(x_values, avg, marker="o", label="Average Times")
        if n == 1:
            plt.legend(["Total time"])
        else:
            plt.legend(["Average time / shiny"])
    elif total:
        x_values = np.arange(len(total))
        plt.plot(x_values, total, marker="o", label="Total Times")
        plt.legend(["Total time"])
    else:
        print(
            "Unexpected data encountered while trying to draw a chart. Check the code."
        )
        print("Exiting program..")
        sys.exit(1)

    plt.ylabel("Time (minutes)")
    plt.xlabel("Chain Number")
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.ylim(bottom=0)

    if not os.path.exists("charts"):
        os.makedirs("charts")
    if not os.path.exists("charts/total") and total:
        os.makedirs("charts/total")
    if not os.path.exists("charts/avg") and avg:
        os.makedirs("charts/avg")

    if avg:
        if not os.path.exists(f"charts/avg/SS_{SS}"):
            os.makedirs(f"charts/avg/SS_{SS}")
        if n == 1:
            filename = f"charts/avg/SS_{SS}/time_for_1_shiny_per_chain.png"
        else:
            filename = f"charts/avg/SS_{SS}/avg_time_for_{n}_shinies_per_chain.png"
    elif total:
        if not os.path.exists(f"charts/total/SS_{SS}"):
            os.makedirs(f"charts/total/SS_{SS}")
        if n == 1:
            filename = f"charts/total/SS_{SS}/time_for_1_shiny_per_chain.png"
        else:
            filename = f"charts/total/SS_{SS}/avg_time_for_{n}_shinies_per_chain.png"
    else:
        print("If you see this something really weird happened. Check the code!")
        print("Exiting program..")
        sys.exit(1)
    plt.savefig(filename, dpi=300)
    plt.show()


def time_spent_all_chart(mode: str):
    """
    Draws and shows chart with all hunts.

    Args:
        mode (str): Tell if the chart is generated from total or average data.
                    Must be either 'total' or 'avg'.
        SS (int): Sample Size of the simulation

    Returns:
        None
    """
    SS_list = []
    choice = -1
    ss = ""
    plt.figure(figsize=(10, 6))

    SS_list = get_SS("data/")
    try:
        # Menu
        if len(SS_list) > 1:
            while choice < 0 or choice > len(SS_list):
                print("From which sample size would you like the graph from?")
                for i, num in enumerate(SS_list):
                    print(f"{i + 1}) Sample Size {num}")
                print("0) Cancel")

                choice = int(input("Your choice: ").strip())
                if choice == 0:
                    return
                elif 0 <= choice <= len(SS_list):
                    ss = SS_list[choice - 1]
                else:
                    print("Invalid input. Please enter a valid choice\n")
        else:
            ss = SS_list[0]

        if mode == "avg":
            with open(f"data/avg_time_data_SS_{ss}.txt", "r") as file:
                lines = file.readlines()
        elif mode == "total":
            with open(f"data/total_time_data_SS_{ss}.txt", "r") as file:
                lines = file.readlines()
        else:
            print("Unexpected mode encountered while trying to draw a chart.")
            return
    except FileNotFoundError:
        print(
            "Could not find the data file. Make sure you save the data to the file first."
        )
        return

    data = []
    legend_marker = 0  # Tracks line number from file
    legend_num_list = []
    skip_first_line = True
    for line in lines:
        if skip_first_line:  # Metadata line
            legend_marker += 1
            skip_first_line = False
            continue

        line = line.strip()
        if not line:  # Empty line
            legend_marker += 1
            continue
        legend_num_list.append(legend_marker)

        line = line.strip().strip("[]").split(",")
        line = [int(item.strip()) for item in line]
        data.append(line)
        legend_marker += 1

    x_values = np.arange(len(data[0]))

    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker="o", label=f"Chain {i + 1}")

    legend_labels = []
    legend_nums = ""
    if mode == "avg":
        for n in legend_num_list:
            legend_nums = f"{legend_nums}_{str(n)}"
            if n == 1:
                legend_labels.append("Time spent looking for a shiny")
            else:
                legend_labels.append(f"Average time spent / shiny for {n} shinies")
    elif mode == "total":
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
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.ylim(bottom=0)

    if not os.path.exists("charts"):
        os.makedirs("charts")
    if not os.path.exists("charts/total"):
        os.makedirs("charts/total")
    if not os.path.exists("charts/avg"):
        os.makedirs("charts/avg")

    if mode == "avg":
        if not os.path.exists(f"charts/avg/SS_{ss}"):
            os.makedirs(f"charts/avg/SS_{ss}")
        filename = (
            f"charts/avg/SS_{ss}/avg_time_for_{legend_nums}_shinies_per_chain.png"
        )
    elif mode == "total":
        if not os.path.exists(f"charts/total/SS_{ss}"):
            os.makedirs(f"charts/total/SS_{ss}")
        filename = (
            f"charts/total/SS_{ss}/total_time_for_{legend_nums}_shinies_per_chain.png"
        )
    plt.savefig(filename, dpi=300)
    plt.show()
