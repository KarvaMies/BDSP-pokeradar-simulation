# main.py - Main entry point for the program

import sys
import modules


def main():
    """Main function to start the program."""
    print(
        "\nWelcome to the Pokéradar Shiny Hunting Simulator for Pokémon Brilliand Diamond and Shining Pearl!"
    )
    modules.main_menu()  # Start the menu loop


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
