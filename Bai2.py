import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2

# Database configuration
DATABASE = {
    'dbname': 'BT2',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def connect_db():
    try:
        # Establish connection
        connection = psycopg2.connect(
            dbname=DATABASE['dbname'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port']
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # SQL command to create table if it does not exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            mssv VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            class VARCHAR(50),
            major VARCHAR(50)
        );
        """
        
        # Execute the query to create the table
        cursor.execute(create_table_query)
        connection.commit()
        
        # Close the cursor and return the connection
        cursor.close()
        return connection
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")
        return None

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "Nam" and password == "1234":
        login_window.destroy()
        create_student_management_window()
    else:
        messagebox.showerror("Error", "Incorrect username or password")

# Create student management interface
def create_student_management_window():
    management_window = tk.Tk()
    management_window.title("Student Management")
    management_window.config(bg="#ADD8E6")

    # Input fields for student information
    tk.Label(management_window, text="Student Name:", bg="#ADD8E6").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(management_window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(management_window, text="Student ID:", bg="#ADD8E6").grid(row=1, column=0, padx=10, pady=5)
    entry_mssv = tk.Entry(management_window)
    entry_mssv.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(management_window, text="Class:", bg="#ADD8E6").grid(row=2, column=0, padx=10, pady=5)
    entry_class = tk.Entry(management_window)
    entry_class.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(management_window, text="Major:", bg="#ADD8E6").grid(row=3, column=0, padx=10, pady=5)
    entry_major = tk.Entry(management_window)
    entry_major.grid(row=3, column=1, padx=10, pady=5)

    # Function buttons
    tk.Button(management_window, text="Add Student", command=lambda: add_student(entry_name, entry_mssv, entry_class, entry_major, students_tree), bg="#98FB98").grid(row=4, column=0, padx=10, pady=5)
    tk.Button(management_window, text="Delete Student", command=lambda: delete_student(entry_mssv, students_tree), bg="#FFCCCB").grid(row=4, column=1, padx=10, pady=5)
    tk.Button(management_window, text="Search Student", command=lambda: search_student(entry_mssv), bg="#FFA07A").grid(row=5, column=0, padx=10, pady=5)

    # Treeview to display student list
    columns = ("No", "Student ID", "Name", "Class", "Major")
    global students_tree
    students_tree = ttk.Treeview(management_window, columns=columns, show="headings")

    for col in columns:
        students_tree.heading(col, text=col, anchor="center")
        students_tree.column(col, anchor="center", width=150)

    students_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    management_window.mainloop()

# Add student to PostgreSQL and Treeview
def add_student(name, mssv, student_class, major, students_tree):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO students (mssv, name, class, major) VALUES (%s, %s, %s, %s)",
                (mssv.get(), name.get(), student_class.get(), major.get())
            )
            connection.commit()
            cursor.close()

            students_tree.insert("", "end", values=(len(students_tree.get_children()) + 1, mssv.get(), name.get(), student_class.get(), major.get()))
            update_stt()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding student: {e}")
        finally:
            connection.close()

# Delete student from PostgreSQL and Treeview
def delete_student(mssv, students_tree):
    mssv_value = mssv.get()
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE mssv = %s", (mssv_value,))
            connection.commit()
            cursor.close()

            for item in students_tree.get_children():
                if students_tree.item(item, "values")[1] == mssv_value:
                    students_tree.delete(item)
                    messagebox.showinfo("Notification", f"Deleted student with ID: {mssv_value}")
                    break
            update_stt()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting student: {e}")
        finally:
            connection.close()

# Search student in PostgreSQL
def search_student(mssv):
    mssv_value = mssv.get()
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE mssv = %s", (mssv_value,))
            student = cursor.fetchone()
            cursor.close()

            if student:
                messagebox.showinfo("Notification", f"Found student: ID: {student[0]}, Name: {student[1]}")
            else:
                messagebox.showerror("Error", "No student found with this ID")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching for student: {e}")
        finally:
            connection.close()

# Update row numbers in Treeview
def update_stt():
    for index, item in enumerate(students_tree.get_children()):
        students_tree.item(item, values=(index + 1,) + students_tree.item(item, "values")[1:])

# Login window
login_window = tk.Tk()
login_window.title("Login")
login_window.config(bg="#ADD8E6")

tk.Label(login_window, text="Username:", bg="#ADD8E6").grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(login_window)
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(login_window, text="Password:", bg="#ADD8E6").grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

tk.Button(login_window, text="Login", command=login, bg="#98FB98").grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
