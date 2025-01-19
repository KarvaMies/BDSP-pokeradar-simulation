import os
import shutil
from datetime import datetime


def save_data(total: list, avg: list, n: int):
    """
    Saves the simulated data to txt files.

    Args:
        total (list): List of times taken for hunts
        avg (list): List of average times taken for hunts
        n (int): Number of shinies hunted

    Returns:
        None
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("data/total_time_data.txt"):
        with open("data/total_time_data.txt", "w") as total_file:
            total_file.write("METADATA: row number = number of shinies hunted\n")

    if not os.path.exists("data/avg_time_data.txt"):
        with open("data/avg_time_data.txt", "w") as avg_file:
            avg_file.write("METADATA: row number = number of shinies hunted\n")

    with open("data/total_time_data.txt", "r") as total_file:
        total_lines = total_file.readlines()
    with open("data/avg_time_data.txt", "r") as avg_file:
        avg_lines = avg_file.readlines()

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


def delete_files(src_folder: str):
    """
    Moves the files from src_folder to deleted/ folder and creates the folder if it doesn't exist.

    Args:
        src_folder (str): The name of the folder to be deleted

    Returns:
        None
    """
    cont = input(
        f"Are you sure you want to delete all contents inside '{src_folder}' folder? (y/n) "
    ).strip()
    while cont.lower() not in ("y", "n"):
        print("Invalid input. Please enter 'y' or 'n'\n")
        cont = input(
            f"Are you sure you want to delete all the files inside '{src_folder}' folder? (y/n) "
        ).strip()

    if cont.lower() == "y":
        dest_folder = f"deleted/{src_folder}"
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        timestamp = datetime.now().strftime("%d.%m.%Y_%H-%M")
        for src_dir, _, files in os.walk(src_folder):
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

            if not os.listdir(src_dir):
                os.rmdir(src_dir)
                print(f"Removed empty '{src_dir}' folder.")

        if not os.listdir(src_folder):
            os.rmdir(src_folder)
            print(f"Removed empty '{src_folder}' folder.")

        print(f"The contents from '{src_folder}' are now moved to '{dest_folder}'.")
        print("If you want to permanently delete the files, please do it manually.")
    else:
        print(f"The contents of '{src_folder}' were not deleted.")


def restore_files():
    """
    Restores files from deleted/ folder to their original location.

    Args:
        None

    Returns:
        None
    """
    deleted_folder = "deleted/"
    if not os.path.exists(deleted_folder):
        print("No deleted data found. You shouldn't even have the option to do this.")
        return

    subfolders = [f.path for f in os.scandir(deleted_folder) if f.is_dir()]
    if not subfolders:
        print("No folders to restore in 'deleted/' folder. Deleting the folder")
        os.rmdir(deleted_folder)
        return

    for folder in subfolders:
        folder_name = os.path.basename(folder)
        cont = input(
            f"Do you want to restore the folder '{folder_name}'? (y/n) "
        ).strip()
        while cont.lower() not in ("y", "n"):
            print("Invalid input. Please enter 'y' or 'n'\n")
            cont = input(
                f"Do you want to restore the folder '{folder_name}'? (y/n) "
            ).strip()

        if cont.lower() == "y":
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            for src_dir, _, files in os.walk(folder):
                dst_folder = src_dir.replace(folder, folder_name)
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)

                for f in files:
                    src_file = os.path.join(src_dir, f)

                    file_name, extension = os.path.splitext(f)
                    parts = file_name.split("_")

                    if parts[-2].count(".") == 2 and parts[-1].count("-") == 1:
                        restored_name = "_".join(parts[:-2]) + extension
                    else:
                        restored_name = f

                    dst_file = os.path.join(dst_folder, restored_name)

                    shutil.move(src_file, dst_file)

            shutil.rmtree(folder)
            print(f"Restored '{folder_name}' to its original location.")
        else:
            print(f"Folder '{folder_name}' was not restored.")

    if not os.listdir(deleted_folder):
        os.rmdir(deleted_folder)
        print(f"Removed empty '{deleted_folder}' folder.")
