import matplotlib.pyplot as plt
import numpy as np
import os, modules


def time_spent_chart(mode: str, ss: int = 0):
    """
    Draws and shows chart from a chosen simulation data.

    Args:
        mode (str): Tell if the chart is generated from total or average data.
            Must be either 'total' or 'avg'
        ss (int): Sample Size of the simulation (if asked before)

    Returns:
        None
    """

    if ss == 0:
        ss = modules.graph_menu()
        if ss == None:
            return

    data_path = f"data/{mode}_time_data_SS_{ss}.txt"
    if mode == "avg":
        label = "Average Times"
        legend = ["Average time / shiny"]
    elif mode == "total":
        label = "Total Times"
        legend = ["Total time"]
    else:
        print("Unexpected data encountered while trying to draw a chart.")
        return

    result = modules.line_menu(data_path)
    if result is None:
        return
    data, n_shinies = result

    if mode == "avg" and n_shinies == 1:
        legend = ["Total time"]

    if n_shinies == 1:
        filename = f"charts/total/SS_{ss}/time_for_1_shiny_per_chain.png"
    else:
        filename = (
            f"charts/{mode}/SS_{ss}/{mode}_time_for_{n_shinies}_shinies_per_chain.png"
        )

    if os.path.exists(filename) and use_existing_graph():
        plt.imshow(plt.imread(filename))
        plt.axis("off")
        plt.show()
        return

    plt.figure(figsize=(10, 6))
    x_values = np.arange(len(data))
    plt.plot(x_values, data, marker="o", label=label)
    plt.legend(legend)
    plt.ylabel("Time (minutes)")
    plt.xlabel("Chain Number")
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.ylim(bottom=0)

    if n_shinies == 1:
        os.makedirs(f"charts/total/SS_{ss}", exist_ok=True)
    elif n_shinies > 1:
        os.makedirs(f"charts/{mode}/SS_{ss}", exist_ok=True)
    else:
        print("Something went wrong while drawing the graph.")
        return
    plt.savefig(filename, dpi=300)
    plt.show()


def time_spent_all_chart(mode: str):
    """
    Draws and shows chart with all simulated hunts for given sample size.

    Args:
        mode (str): Tell if the chart is generated from total or average data.
            Must be either 'total' or 'avg'.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    ss = modules.graph_menu()
    if ss == None:
        return

    try:
        with open(f"data/{mode}_time_data_SS_{ss}.txt", "r") as file:
            lines = file.readlines()
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

    if len(legend_num_list) == 1:
        time_spent_chart(mode, ss, data)
        return

    legend_labels = []
    legend_nums = ""

    for num in legend_num_list:
        legend_nums = f"{legend_nums}_{str(num)}"
        if num == 1:
            legend_labels.append("Time spent looking for a shiny")
        elif mode == "avg":
            legend_labels.append(f"Average time spent / shiny for {num} shinies")
        elif mode == "total":
            legend_labels.append(f"Total time for {num} shinies")

    if legend_nums.startswith("_"):
        legend_nums = legend_nums[1:]

    filename = (
        f"charts/{mode}/SS_{ss}/{mode}_time_for_{legend_nums}_shinies_per_chain.png"
    )

    if os.path.exists(filename) and use_existing_graph():
        plt.imshow(plt.imread(filename))
        plt.axis("off")
        plt.show()
        return

    x_values = np.arange(len(data[0]))

    for i, dataset in enumerate(data):
        plt.plot(x_values, dataset, marker="o", label=f"Chain {i + 1}")

    plt.legend(legend_labels)
    plt.xlabel("Chain Number")
    plt.ylabel("Time (minutes)")
    plt.grid(axis="both", linestyle="--", alpha=0.7)
    plt.ylim(bottom=0)

    os.makedirs(f"charts/{mode}/SS_{ss}", exist_ok=True)

    plt.savefig(filename, dpi=300)
    plt.show()


def use_existing_graph():
    """
    Asks if the user wants to use existing graph instead of drawing a new one

    Args:
        None

    Returns:
        bool
    """
    choice = "-1"
    choice = input(f"Graph already exists. Use existing graph? (y/n) ").strip()
    while choice.lower() not in ("y", "n"):
        print("Invalid input. Please enter 'y' or 'n'\n")
        choice = input(f"Graph already exists. Use existing graph? (y/n) ").strip()
        if choice == "y":
            return True
    return False
