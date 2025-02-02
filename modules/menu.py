import os
import sys
import traceback
import glob
from data_handler import delete_files, restore_files, get_SS
from simulation import run_simulation

MAX_CHAIN = 40
SAMPLE_SIZE = 5000  # 30000
ODDS = [
    4096,
    3855,
    3640,
    3449,
    3277,
    3121,
    2979,
    2849,
    2731,
    2621,
    2521,
    2427,
    2341,
    2259,
    2185,
    2114,
    2048,
    1986,
    1927,
    1872,
    1820,
    1771,
    1724,
    1680,
    1638,
    1598,
    1560,
    1524,
    1489,
    1456,
    1310,
    1285,
    1260,
    1236,
    1213,
    1192,
    993,
    799,
    400,
    200,
    99,
]


def main_menu():
    """
    Prints and operates the menu.

    Args:
        data_total (list): List of times taken for hunts
        data_avg (list): List of average times taken for hunts
        shinies (int): Number of shinies hunted
        hunt (bool): Tells if hunt simulation has been done since the program started

    Returns:
        None
    """
    from chart_generator import time_spent_chart, time_spent_all_chart

    choice = "-1"

    while choice != "0":
        avg_exists = glob.glob("data/avg_time_data_SS_*.txt")
        total_exists = glob.glob("data/total_time_data_SS_*.txt")

        print("\nWhat would you like to do?")
        print("1) Simulate shiny hunting")
        if total_exists:
            print("2) See the total time spent shiny hunting")
            print("3) See the total time spent of all data sets")
        if avg_exists:
            print("4) See the chart of average time spent/shiny")
            print("5) See the chart of average time spent/shiny for all the data sets")
        if os.path.exists("data/") and os.listdir("data/"):
            print("6) Delete data files")
        if (os.path.exists("charts/avg/") and os.listdir("charts/avg/")) or (
            os.path.exists("charts/total/") and os.listdir("charts/total/")
        ):
            print("7) Delete charts")
        if os.path.exists("deleted/"):
            print("8) Restore deleted files")
        print("0) Exit\n")
        choice = input("Your choice: ").strip()

        try:
            if choice == "1":
                n_shinies = get_n_shinies()
                run_simulation(MAX_CHAIN, SAMPLE_SIZE, n_shinies, ODDS)

            elif choice == "2" and total_exists:
                time_spent_chart("total")
            elif choice == "3" and total_exists:
                time_spent_all_chart("total")
            elif choice == "4" and avg_exists:
                time_spent_chart("avg")
            elif choice == "5" and avg_exists:
                time_spent_all_chart("avg")
            elif choice == "6" and os.path.exists("data/") and os.listdir("data/"):
                delete_files("data/")
            elif choice == "7" and (
                (os.path.exists("charts/avg/") and os.listdir("charts/avg/"))
                or (os.path.exists("charts/total/") and os.listdir("charts/total/"))
            ):
                delete_files("charts/")
            elif choice == "8" and os.path.exists("deleted/"):
                restore_files()
            elif choice == "0":
                print("Exiting the program..")
                sys.exit(0)
            else:
                print("Invalid input. Please enter a valid choice\n")
        except FileNotFoundError:
            print("Why would you try to delete files that you just moved or deleted?")
            traceback.print_exc()


def get_n_shinies():
    """
    Asks the user how many shinies they plan to hunt, 0 exits the program.

    Args:
        None

    Returns:
        num_of_shinies (int): Number of wanted shinies
    """
    while True:
        num_of_shinies = input(
            "How many shinies do you plan to hunt? (0 exits) "
        ).strip()
        if num_of_shinies.isdigit() and int(num_of_shinies) > 0:
            return int(num_of_shinies)
        elif num_of_shinies == "0":
            print("Exiting the program..")
            sys.exit(0)
        else:
            print("Invalid input. Please enter a psoitive number.\n")


def graph_menu():
    """
    Asks the user which sample size the graph will be created from.

    Args:
        None

    Returns:
        int: The sample size used get the correct data for the graph
    """
    SS_list = []
    choice = -1
    SS_list = get_SS("data/")

    if len(SS_list) > 1:
        while choice < 0 or choice > len(SS_list):
            print("From which sample size would you like the graph from?")
            for i, num in enumerate(SS_list):
                print(f"{i + 1}) Sample Size {num}")
            print("0) Cancel")

            choice = int(input("Your choice: ").strip())
            if choice == 0:
                return None
            elif 0 <= choice <= len(SS_list):
                return SS_list[choice - 1]
            else:
                print("Invalid input. Please enter a valid choice\n")
    else:
        return SS_list[0]


def line_menu(file_path: str):
    """
    Asks the user which data line from the file should be used and returns the corresponding data.

    Args:
        file_path (str): Path to the data file

    Returns:
        tuple: (data list, choice) where:
            data list (list): The selected data line as a list of numbers
            choice (int): The number of shinies
        None if canceled
    """
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        if len(lines) < 2:
            print("The data file doesn't contain enough entries")
            return None

        choice = -1
        while choice < 0 or choice >= len(lines) - 1:
            print("\nSelect the number of shinies to use for the graph:")
            for i in range(1, len(lines)):  # Skip metadata line
                print(f"{i}) {i} shin{'ies' if i > 1 else 'y'}")
            print("0) Cancel")

            try:
                choice = int(input("Your choice: ").strip())
                if choice == 0:
                    return None
                elif 1 <= choice < len(lines):
                    return eval(lines[choice].strip()), choice
                else:
                    print("Invalid input. Please enter a valid choice.\n")
            except ValueError:
                print("Invalid input. Please enter a number.\n")
    except FileNotFoundError:
        print("Could not find the data file. Make sure it exists.")
        return None


if __name__ == "__main__":
    print(
        "Welcome to Pokéradar shiny hunting simulation tool for Pokémon Brilliand Diamond and Shining Pearl!"
    )
    main_menu()
