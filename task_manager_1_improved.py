# Improved version of the task_manager_1.py script
# 3 months after the first version


# Here we go

import datetime
import logging
from pathlib import Path
from typing import Dict, List

# Configures logging for warnings and errors.
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s: %(message)s")

# Adding constants.
USER_FILE: Path = Path("user.txt")
TASK_FILE: Path = Path("tasks.txt")


def read_file_lines(file_path: Path) -> List[str]:
    """
    Reads all lines from a file and returns a list of strings.
    """
    try:
        with file_path.open("r") as file:
            return file.readlines()
    except FileNotFoundError:
        logging.warning("File %s not found.", file_path)
        return []


def append_to_file(file_path: Path, content: str) -> None:
    """
    Appends a string to a file.
    """
    try:
        with file_path.open("a") as file:
            file.write(content)
    except Exception as e:
        logging.error("Error writing to %s: %s", file_path, e)


def load_users() -> Dict[str, str]:
    """
    Loads users from the user file into a dictionary.
    """
    users: Dict[str, str] = {}
    lines = read_file_lines(USER_FILE)
    for line in lines:
        try:
            username, password = line.strip().split(", ")
            users[username] = password
        except ValueError:
            logging.error("User file formatting error on line: %s",
                          line.strip())
    if not users:
        # Creates a new user file with the default admin account.
        logging.warning(
            "%s not found or empty. Creating a new file with default admin.",
            USER_FILE)
        with USER_FILE.open("w") as file:
            file.write("admin, adm1n\n")
        users["admin"] = "adm1n"
    return users


def register_user(users: Dict[str, str]) -> None:
    """
    Registers a new user if it does not already exist.
    """
    new_username = input("\nEnter new username: ").strip()
    if new_username in users:
        print("\nUsername already exists. Pick a different one.\n")
        return

    new_password = input("\nEnter new password: ").strip()
    confirm_password = input("\nConfirm password: ").strip()
    if new_password != confirm_password:
        print("\nPasswords do not match. Try again.\n")
        return

    append_to_file(USER_FILE, f"{new_username}, {new_password}\n")
    users[new_username] = new_password
    print("\nNew user registered successfully.\n")


def add_task(users: Dict[str, str]) -> None:
    """
    Adds a new task.
    """
    assignee = input("\nEnter username of the assignee: ").strip()
    if assignee not in users:
        print("\nUser does not exist. Please register the user first.\n")
        return

    title = input("\nEnter the task title: ").strip()
    description = input("\nEnter the task description: ").strip()
    due_date = input("\nEnter the due date (DD/MM/YYYY): ").strip()
    try:
        datetime.datetime.strptime(due_date, "%d/%m/%Y")
    except ValueError:
        print("\nInvalid date format. Please use DD/MM/YYYY.\n")
        return

    assigned_date = datetime.date.today().strftime("%d/%m/%Y")
    completed = "No"
    task_line = (
        f"{assignee}, {title}, {description}, {assigned_date}, "
        f"{due_date}, {completed}\n"
    )
    append_to_file(TASK_FILE, task_line)
    print("\nNew task successfully added.\n")


def print_task(task_data: List[str],
               include_username: bool = True) -> None:
    """
    A helper function to print a task in a structured format.
    """
    if include_username:
        if len(task_data) >= 6:
            print(f"Username   : {task_data[0]}")
            print(f"Title      : {task_data[1]}")
            print(f"Description: {task_data[2]}")
            print(f"Assigned   : {task_data[3]}")
            print(f"Due Date   : {task_data[4]}")
            print(f"Completed  : {task_data[5]}")
    else:
        if len(task_data) >= 6:
            print(f"Title      : {task_data[1]}")
            print(f"Description: {task_data[2]}")
            print(f"Assigned   : {task_data[3]}")
            print(f"Due Date   : {task_data[4]}")
            print(f"Completed  : {task_data[5]}")
    print("-" * 50)


def view_all_tasks() -> None:
    """
    Displays all the tasks in a structured format.
    """
    lines = read_file_lines(TASK_FILE)
    if not lines:
        print("\nNo tasks assigned.\n")
        return

    print("\n" + "=" * 50)
    for line in lines:
        try:
            task_data = line.strip().split(", ")
            if len(task_data) != 6:
                logging.error("Task formatting error: %s", line.strip())
                continue
            print_task(task_data, include_username=True)
        except Exception as e:
            logging.error("Error processing task: %s", e)


def view_my_tasks(username: str) -> None:
    """
    Displays the tasks assigned to the logged-in user.
    """
    lines = read_file_lines(TASK_FILE)
    user_tasks = []
    for line in lines:
        try:
            task_data = line.strip().split(", ")
            if len(task_data) != 6:
                logging.error("Task formatting error: %s", line.strip())
                continue
            if task_data[0] == username:
                user_tasks.append(task_data)
        except Exception as e:
            logging.error("Error processing task: %s", e)
    if not user_tasks:
        print("\nThere are no tasks assigned to you.\n")
        return

    print("\n" + "=" * 50)
    for task_data in user_tasks:
        print_task(task_data, include_username=False)


def login(users: Dict[str, str]) -> str:
    """
    Prompts the user for login credentials and returns the username.
    """
    while True:
        print("\n" + "=" * 5 + " LOGIN " + "=" * 5)
        username = input("\nEnter username: ").strip()
        password = input("Enter password: ").strip()
        if username in users and users[username] == password:
            print("\n" + "=" * 3 + " Login successful! " + "=" * 3)
            return username
        print("\nInvalid credentials. Try again.\n")


def main() -> None:
    """
    Main program loop.
    """
    users = load_users()
    username = login(users)

    menu_prompt = (
        "\nSelect one of the following options:\n\n"
        "r  - register a user\n"
        "a  - add task\n"
        "va - view all tasks\n"
        "vm - view my tasks\n"
        "e  - exit\n\n"
        "Make selection here: "
    )

    while True:
        menu = input(menu_prompt).lower().strip()
        if menu == "r":
            register_user(users)
        elif menu == "a":
            add_task(users)
        elif menu == "va":
            view_all_tasks()
        elif menu == "vm":
            view_my_tasks(username)
        elif menu == "e":
            print("\nThat is all then. Bye Bye now...\n" + "-" * 26 + "\n")
            break
        else:
            print("\nInvalid input. Try again.\n")


if __name__ == "__main__":
    main()
