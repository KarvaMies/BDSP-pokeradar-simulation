import os, shutil
from datetime import datetime


def save_data(total: list, avg: list, n: int, SS: int):
    """
    Saves the simulated data to txt files.

    Args:
        total (list): List of times taken for hunts
        avg (list): List of average times taken for hunts
        n (int): Number of shinies hunted
        SS (int): sample_size

    Returns:
        None
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(f"data/total_time_data_SS_{SS}.txt"):
        with open(f"data/total_time_data_SS_{SS}.txt", "w") as total_file:
            total_file.write("METADATA: row number = number of shinies hunted\n")

    if not os.path.exists(f"data/avg_time_data_SS_{SS}.txt"):
        with open(f"data/avg_time_data_SS_{SS}.txt", "w") as avg_file:
            avg_file.write("METADATA: row number = number of shinies hunted\n")

    with open(f"data/total_time_data_SS_{SS}.txt", "r") as total_file:
        total_lines = total_file.readlines()
    with open(f"data/avg_time_data_SS_{SS}.txt", "r") as avg_file:
        avg_lines = avg_file.readlines()

    if n < len(total_lines):
        total_lines[n] = str(total) + "\n"
        avg_lines[n] = str(avg) + "\n"
    else:
        total_lines.extend(["\n"] * (n - len(total_lines)))
        total_lines.append(str(total) + "\n")

        avg_lines.extend(["\n"] * (n - len(avg_lines)))
        avg_lines.append(str(avg) + "\n")

    with open(f"data/total_time_data_SS_{SS}.txt", "w") as total_file:
        total_file.writelines(total_lines)

    with open(f"data/avg_time_data_SS_{SS}.txt", "w") as avg_file:
        avg_file.writelines(avg_lines)


def delete_files(src: str):
    """
    Moves the files from 'src' folder to deleted/ folder while maintaining the original folder structure.
    It also adds a timestamp to the moved files.

    Args:
        src_folder (str): The name of the folder to be deleted.

    Returns:
        None
    """
    ss_files_map = {}

    # Iterate through all subdirectories of src
    for root, _, files in os.walk(src, topdown=False):
        SS_list = get_SS(root)

        for ss in SS_list:
            # Ensure there are files matching SS om tjos folder
            matching_files = [os.path.join(root, f) for f in files if f"SS_{ss}" in f]
            if not matching_files and f"SS_{ss}" in os.path.basename(root):
                matching_files = [os.path.join(root, f) for f in files]

            if matching_files:
                if ss not in ss_files_map:
                    ss_files_map[ss] = []
                ss_files_map[ss].extend(matching_files)

    for ss, files in ss_files_map.items():
        if files:
            cont_item = input(
                f"\nDo you want to delete all 'SS_{ss}' files? (y/n) "
            ).strip()
            while cont_item.lower() not in ("y", "n"):
                print("Invalid input. Please enter 'y' or 'n'\n")
                cont_item = input(
                    f"Do you want to delete all 'SS_{ss}' files? (y/n) "
                ).strip()

            if cont_item.lower() == "y":
                timestamp = datetime.now().strftime("%d.%m.%Y_%H-%M")
                for file_path in files:
                    dest_folder = os.path.join("deleted", os.path.dirname(file_path))
                    os.makedirs(dest_folder, exist_ok=True)

                    # Move and rename the file
                    filename = os.path.basename(file_path)
                    f_name, ext = os.path.splitext(filename)
                    new_name = f"{f_name}_{timestamp}{ext}"
                    dest_path = os.path.join(dest_folder, new_name)

                    shutil.move(file_path, dest_path)
                    print(f"Moved: {file_path} -> {dest_path}")

    # Remove empty folders
    for root, _, _ in os.walk(src, topdown=False):
        if not os.listdir(root):
            os.rmdir(root)
            print(f"Removed empty folder: {root}")

    print("File deletion completed.")


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


def get_SS(src: str):
    """
    Gets sample sizes from the files of the folder.

    Args:
        src (str): The folder
    Returns:
        List of unique sample size values found in filenames
    """
    SS_list = set()

    # Extract from folder name
    folder_name = os.path.basename(src)
    ss_part = folder_name.split("_")[-1]
    if ss_part.isdigit():
        SS_list.add(ss_part)

    # Extract from filename
    for f in os.listdir(src):
        file_name, _ = os.path.splitext(f)
        ss_part = file_name.split("_")[-1]
        if ss_part.isdigit():
            SS_list.add(ss_part)
    return sorted(list(SS_list))
