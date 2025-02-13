# TASK 17 CAPSTONE PROJECT

# Compulsory task 1
# Small business task manager 1.0 - No restrictions

''' Note to assesor. I have considered security aspect of the code,
specifically, whether I should secure the passwords in the file by
hashing/salted hashing as well as using strong password policy etc.
but decided against it as this was not even implied in the task text.
In any case, just to let you know I am aware the script is vulnerable.'''

import os
import datetime

# Constants
USER_FILE = "user.txt"
TASK_FILE = "tasks.txt"

def load_users():
    """Loads users from the user file into a dictionary."""
    users = {}
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(", ")
                users[username] = password
    except FileNotFoundError:
        print(f"\nWarning: {USER_FILE} not found. Creating a new one.\n")
        with open(USER_FILE, "w") as file:
            file.write("admin, adm1n\n")
    return users

def register_user(users):
    """Registers a new user if it doesn't already exist."""
    new_username = input("\nEnter new username: ")
    if new_username in users:
        print("\nUsername already exists. Pick a different one.\n")
        return
    
    new_password = input("\nEnter new password: ")
    confirm_password = input("\nConfirm password: ")
    if new_password != confirm_password:
        print("\nPasswords do not match. Try again.\n")
        return
    
    with open(USER_FILE, "a") as file:
        file.write(f"{new_username}, {new_password}\n")
    users[new_username] = new_password
    print("\nNew user successfully registered!\n")

def add_task():
    """Adds a new task."""
    username = input("\nEnter username of the assignee: ")
    title = input("\nEnter task title: ")
    description = input("\nEnter task description: ")
    due_date = input("\nEnter due date (DD/MM/YYYY): ")
    try:
        datetime.datetime.strptime(due_date, "%d/%m/%Y")
    except ValueError:
        print("\nInvalid date format. Please use DD/MM/YYYY.")
        return
    
    assigned_date = datetime.date.today().strftime("%d/%m/%Y")
    completed = "No"
    
    with open(TASK_FILE, "a") as file:
        file.write(f"{username}, {title}, {description}, {assigned_date}, {due_date}, {completed}\n")
    print("\nNew task successfully added!")

def view_all_tasks():
    """Displays all tasks in a structured format."""
    try:
        with open(TASK_FILE, "r") as file:
            tasks = file.readlines()
            if not tasks:
                print("\nNo tasks assigned.")
                return
            
            print("\n" + "="*50)
            for task in tasks:
                username, title, desc, assigned, due, completed = task.strip().split(", ")
                print(f"Username   : {username}")
                print(f"Title      : {title}")
                print(f"Description: {desc}")
                print(f"Assigned   : {assigned}")
                print(f"Due Date   : {due}")
                print(f"Completed  : {completed}")
                print("-"*50)
            
    except FileNotFoundError:
        print(f"\nWarning: {TASK_FILE} not found.")

def view_my_tasks(username):
    """Display tasks assigned to the logged-in user in a structured format."""
    try:
        with open(TASK_FILE, "r") as file:
            tasks = file.readlines()
            user_tasks = [task for task in tasks if task.startswith(username)]
            if not user_tasks:
                print("\nNo tasks assigned to you.")
                return
            
            print("\n" + "="*50)
            for task in user_tasks:
                _, title, desc, assigned, due, completed = task.strip().split(", ")
                print(f"Title      : {title}")
                print(f"Description: {desc}")
                print(f"Assigned   : {assigned}")
                print(f"Due Date   : {due}")
                print(f"Completed  : {completed}")
                print("-"*50)
    except FileNotFoundError:
        print(f"\nWarning: {TASK_FILE} not found.")

def login(users):
    """Prompt user for login credentials."""
    while True:
        print("\n" + "="*5 + " LOGIN " + "="*5)
        username = input("\nEnter username: ")
        password = input("Enter password: ")
        if username in users and users[username] == password:
            print("\n" + "="*3 + " Login successful! " + "="*3)
            return username
        print("\nInvalid credentials. Try again.")

def main():
    """Main program loop."""
    users = load_users()
    username = login(users)
    
    while True:
        menu = input("""
Select one of the following options:
                     
r - register a user
a - add task
va - view all tasks
vm - view my tasks
e - exit
                     
Make selection here: """).lower()

        if menu == "r":
            register_user(users)
        elif menu == "a":
            add_task()
        elif menu == "va":
            view_all_tasks()
        elif menu == "vm":
            view_my_tasks(username)
        elif menu == "e":
            print("\nThat is all then. Bye Bye!\n" + "-"*26 + "\n")
            break
        else:
            print("\nInvalid input. Try again.")

if __name__ == "__main__":
    main()
