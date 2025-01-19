import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def time_spent_chart(total: list, avg: list, n: int):
    """
    Draws and shows chart for simulated n number of shinies.
    Either total or avg must be an empty list.

    Args:
        total (list): List of times taken for hunts
        avg (list): List of average times taken for hunts
        n (int): Number of shinies hunted

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    if len(total) != 0 and len(avg) != 0:
        print(
            "Unexpected data encountered while trying to draw a chart. Check the code."
        )
        print("Exiting program..")
        sys.exit(1)
    elif len(total) == 0:
        x_values = np.arange(len(avg))
        plt.plot(x_values, avg, marker="o", label="Average Times")
        if n == 1:
            plt.legend(["Total time"])
        else:
            plt.legend(["Average time / shiny"])
    elif len(avg) == 0:
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
    if not os.path.exists("charts/total"):
        os.makedirs("charts/total")
    if not os.path.exists("charts/avg"):
        os.makedirs("charts/avg")
    if len(total) == 0:
        if n == 1:
            filename = f"charts/avg/time_for_1_shiny_per_chain.png"
        else:
            filename = f"charts/avg/avg_time_for_{n}_shinies_per_chain.png"
    elif len(avg) == 0:
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


def time_spent_all_chart(total: list, avg: list, hunt: bool):
    """
    Draws and shows chart with all hunts.
    Either total or avg must be an empty list.

    Args:
        total (list): List of times taken for hunts
        avg (list): List of average times taken for hunts
        hunt (bool): Tells if hunt simulation has been done since the program started

    Returns:
        None
    """
    data_matches = False
    plt.figure(figsize=(10, 6))
    try:
        if len(total) == 0:
            if hunt:
                time_data = str(avg)
                x_values = np.arange(len(avg))
            with open("data/avg_time_data.txt", "r") as file:
                lines = file.readlines()
        elif len(avg) == 0:
            if hunt:
                time_data = str(total)
                x_values = np.arange(len(total))
            with open("data/total_time_data.txt", "r") as file:
                lines = file.readlines()
        else:
            print(
                "Unexpected data encountered while trying to draw a chart. Check the code."
            )
            print("Exiting program..")
            sys.exit(1)
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

        if hunt and line == str(time_data):
            data_matches = True

        line = line.strip().strip("[]").split(",")
        line = [int(item.strip()) for item in line]
        data.append(line)
        legend_marker += 1

    if not hunt:
        x_values = np.arange(len(data[0]))

    if not data_matches and hunt:
        print(f"total: {total}\navg: {avg}")
        print(f"timedata1:\n{time_data}")
        time_data = time_data.strip().strip("[]").split(",")
        print(f"timedata2:\n{time_data}")
        time_data = [int(item.strip()) for item in time_data]
        print(f"timedata3:\n{time_data}")
        data.append(time_data)

    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker="o", label=f"Chain {i + 1}")

    legend_labels = []
    legend_nums = ""
    if len(total) == 0:
        for n in legend_num_list:
            legend_nums = f"{legend_nums}_{str(n)}"
            if n == 1:
                legend_labels.append("Time spent looking for a shiny")
            else:
                legend_labels.append(f"Average time spent / shiny for {n} shinies")
    elif len(avg) == 0:
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
    if len(total) == 0:
        filename = f"charts/avg/avg_time_for_{legend_nums}_shinies_per_chain.png"
    elif len(avg) == 0:
        filename = f"charts/total/total_time_for_{legend_nums}_shinies_per_chain.png"
    plt.savefig(filename, dpi=300)
    plt.show()
