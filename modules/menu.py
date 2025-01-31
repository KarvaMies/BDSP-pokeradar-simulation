import os
import sys
import traceback
import glob
from data_handler import delete_files, restore_files
from chart_generator import time_spent_chart, time_spent_all_chart
from simulation import run_simulation

MAX_CHAIN = 40
SAMPLE_SIZE = 51  # 00  # 30000
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


def menu(data_total: list, data_avg: list, shinies: int, hunt_done: bool):
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
    choice = "-1"
    total_list = data_total
    avg_list = data_avg
    n_shinies = shinies

    while choice != "0":
        avg_exists = glob.glob("data/avg_time_data_SS_*.txt")
        total_exists = glob.glob("data/total_time_data_SS_*.txt")

        print("\nWhat would you like to do?")
        print("1) Simulate shiny hunting")
        if hunt_done and total_list:
            print("2) See the total time spent shiny hunting")
        if total_exists:
            print("3) See the total time spent of all data sets")
        if hunt_done and avg_list:
            print("4) See the chart of average time spent/shiny")
        if avg_exists:
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
                total_list, avg_list = run_simulation(
                    MAX_CHAIN, SAMPLE_SIZE, n_shinies, ODDS
                )
                hunt_done = True

            elif choice == "2" and hunt_done:
                time_spent_chart(total_list, [], n_shinies, SAMPLE_SIZE)
            elif choice == "3" and total_exists:
                time_spent_all_chart("total")
            elif choice == "4" and hunt_done:
                time_spent_chart([], avg_list, n_shinies, SAMPLE_SIZE)
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


if __name__ == "__main__":
    print(
        "Welcome to Pokéradar shiny hunting simulation tool for Pokémon Brilliand Diamond and Shining Pearl!"
    )
    menu([], [], -1, False)
