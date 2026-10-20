
# Task Manager with User Accounts


import sqlite3 #This module is used to interact with SQLite databases.

DB_NAME = 'user_database.db' #This is the name of the SQLite database file that will be used to store user and task information.

# This code establishes a connection to the SQLite database and creates a cursor object that will be used to execute SQL commands.
con = sqlite3.connect(DB_NAME)
cursor = con.cursor()

# user table is created to store user information, including an auto-incrementing ID, name, email, and password. The email field is set to be unique to prevent duplicate entries.
cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
# task table is created to store task information, including an auto-incrementing ID, a foreign key referencing the user who created the task, and fields for the task details.
cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Pending',
                date_exu TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')


con.commit()

# The following functions are defined to handle user registration, login, task addition, and task viewing.

# register and login function is child of main function. It is used to register a new user by inserting their name, email, and password into the users table in the database.
def register(name, email, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, password)
        )
        con.commit()


def login(email, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, password)
        )
        result = cursor.fetchone()

        if result:
            print("\n")
            print("LOGIN SUCCESSFUL")
            user_id = result[0]
            task_manager_main(user_id)
            print("\n")
        else:
            print("\n")
            print("INVALID EMAIL OR PASSWORD")
            print("\n")

        con.commit()
     
# add and view task function is child of task_manager_main function. It is used to add a new task for a specific user by inserting the task details into the user_task table in the database.
def add_task(user_id, title, description, priority, status, date):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            'INSERT INTO user_task (user_id, task_title, description, priority, status, date_exu) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, title, description, priority, status, date)
        )
        con.commit()


def view_task(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        tasks = conn.execute(
            'SELECT * FROM user_task WHERE user_id = ?',
            (user_id,)
        ).fetchall()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print(task)

        con.commit()

# task_manager_main function is the main interface for the task manager. It presents a menu to the user, allowing them to add tasks, view tasks, or exit the task manager. Depending on the user's choice, it calls the appropriate functions to handle task management.
def task_manager_main(user_id):
    while True:
        print("\n")
        print("WELCOME TO TASK-MANAGER")
        print("\n")

        print("1. ADD TASK")
        print("2. VIEW TASK")
        print("3. EXIT FROM TASK MANAGER")
        print("\n")

        option = input("ENTER YOUR OPTION ---> ").strip()

        if option == '1':
            title = input("ENTER YOUR TITLE ---> ").strip()
            description = input("ENTER YOUR DESCRIPTION ---> ").strip()
            priority = input("ENTER YOUR PRIORITY ---> ").strip() or 'Medium'
            status = input("ENTER YOUR STATUS ---> ").strip() or 'Pending'
            date = input("ENTER YOUR DATE ---> ").strip()
            add_task(user_id, title, description, priority, status, date)

        elif option == '2':
            view_task(user_id)

        elif option == '3':
            break

        else:
            print("INVALID OPTION. TRY AGAIN")

# main function is the entry point of the application. It presents a menu to the user, allowing them to register, log in, or exit the application. Depending on the user's choice, it calls the appropriate functions to handle user registration and login.
def main():

    while True:
        print("\n")
        print("WELCOME TO TASK-MANAGER")
        print("\n")

        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("\n")

        user = input("ENTER YOUR OPTION ---> ").strip()

        if user == '1':
            name = input("ENTER YOUR NAME ---> ").strip()
            email = input("ENTER YOUR EMAIL ---> ").strip()
            password = input("ENTER YOUR PASSWORD ---> ").strip()
            register(name, email, password)

        elif user == '2':
            email = input("ENTER YOUR EMAIL ---> ").strip()
            password = input("ENTER YOUR PASSWORD ---> ").strip()
            login(email, password)

        elif user == '3':
            break

        else:
            print("INVALID OPTION. PLEASE TRY AGAIN")


if __name__ == '__main__':
    main()




# This code defines a simple task manager application with user accounts. It allows users to register, log in, add tasks, and view their tasks. The application uses SQLite as the database to store user and task information.
