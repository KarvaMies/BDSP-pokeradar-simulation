import os
import sys
import traceback
import glob
from tqdm import tqdm
import modules


def main_menu():
    """
    Displays the main menu and handles user choices.

    Args:
        None

    Returns:
        None
    """

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
                shiny_list = get_n_shinies()
                if shiny_list is None:
                    continue

                if len(shiny_list) > 1:
                    print("\n🔄  Runnin multiple simulations... 🔄")
                for n_shinies in shiny_list:
                    print(
                        f"\n✨  Simulating {n_shinies} shin{'ies' if n_shinies > 1 else 'y'}... ✨"
                    )
                    modules.run_simulation(n_shinies)
                if len(shiny_list) > 1:
                    print("\n✅  All simulations completed! ✅")

            elif choice == "2" and total_exists:
                modules.time_spent_chart("total")
            elif choice == "3" and total_exists:
                modules.time_spent_all_chart("total")
            elif choice == "4" and avg_exists:
                modules.time_spent_chart("avg")
            elif choice == "5" and avg_exists:
                modules.time_spent_all_chart("avg")
            elif choice == "6" and os.path.exists("data/") and os.listdir("data/"):
                modules.delete_files("data/")
            elif choice == "7" and (
                (os.path.exists("charts/avg/") and os.listdir("charts/avg/"))
                or (os.path.exists("charts/total/") and os.listdir("charts/total/"))
            ):
                modules.delete_files("charts/")
            elif choice == "8" and os.path.exists("deleted/"):
                modules.restore_files()
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
    Asks the user how many shinies they plan to hunt, 0 exits the program and multiple simulations are allowed.

    Example input: "1, 3" → Runs two simulations (one for 1 shiny, one for 3 shinies)

    Args:
        None

    Returns:
        list[int]: A list of numbers representing how many shinies to hunt in each simulation
    """
    while True:
        num_of_shinies = input(
            "How many shinies do you plan to hunt? (Separate multiple values with commas, 0 exits) "
        ).strip()

        if num_of_shinies == "0":
            return None

        try:
            hunt_list = [
                int(n.strip()) for n in num_of_shinies.split(",") if n.strip().isdigit()
            ]

            if all(n > 0 for n in hunt_list):
                total_shinies = sum(hunt_list)

                if len(hunt_list) > 2 or total_shinies > 4:
                    print(
                        f"⚠️  Warning: You're running {len(hunt_list)} simulations for a total of {total_shinies} shinies. ⚠️"
                    )
                    print("This may take a long time!")
                    while True:
                        cont = input(
                            "Are you sure you want to continue? (y/n) "
                        ).strip()
                        if cont == "y":
                            break
                        elif cont == "n":
                            return None
                        else:
                            print("Invalid input. PLease type only 'y' or 'n'\n")

                    return hunt_list
            else:
                print("Invalid input. Please enter only psoitive numbers.\n")

        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.\n")


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
    SS_list = modules.get_SS("data/")

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
