import tkinter as tk
import sqlite3
from tkinter import Tk, messagebox, ttk

### Current Problems ###
# UNCUSTOMIZED GUI
# Role GUIs incomplete
# Create a way to add users into their role tables


# Purpose: Create the user database
def createTables() -> None:
    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()

    curs.execute("DELETE FROM Users")
    curs.execute('''CREATE TABLE IF NOT EXISTS Users
                (UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, Role TEXT)''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Courses
                (CourseID INTEGER PRIMARY KEY AUTOINCREMENT, CourseName TEXT, StudentIDs INTEGER, FacultyIDs INTEGER,
                FOREIGN KEY (StudentIDs) REFERENCES Users(UserID),
                FOREIGN KEY (FacultyIDs) REFERENCES Users(UserID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Admins
                (AdminID INTEGER PRIMARY KEY, 
                FOREIGN KEY (AdminID) REFERENCES Users(UserID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Faculty
                (FacultyID INTEGER PRIMARY KEY, Phone TEXT, Email TEXT, Name TEXT, Qualifications TEXT,
                FOREIGN KEY (FacultyID) REFERENCES Users(UserID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Students
                (StudentID INTEGER PRIMARY KEY, Phone TEXT, Email TEXT, Name TEXT, 
                FOREIGN KEY (StudentID) REFERENCES Users(UserID)
                )''')
    
    conn.commit()
    conn.close()

###

# ROLE GUIS

###

def open_admin_UI() -> None:
    admin_win = tk.Tk()
    admin_win.title("Welcome Admin")
    admin_win.state("zoomed")

def open_faculty_UI() -> None:
    faculty_win = tk.Tk()
    faculty_win.title("Welcome Faculty")
    faculty_win.state("zoomed")

def open_student_UI() -> None:
    student_win = tk.Tk()
    student_win.title("Welcome Student")
    student_win.state("zoomed")
###


# DATABASE FUNCTIONS

###
    
def registercredentials() -> None:
    username = username_entry.get()
    password = password_entry.get()
    role = role_dd.get()

    if username == '' or password == '' or role == '':
        messagebox.showerror("Username, password and/or role can not be empty. Please input a username and/or password.")
        return

    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM Users WHERE Username = ?",
                 (username, ))
    if curs.fetchone():
        messagebox.showerror("Error", "Username already exists. Please try again.")
    else:
        curs.execute("INSERT INTO Users(Username, Password, Role) VALUES (?, ?, ?)",
                 (username, password, role))
        conn.commit()
        messagebox.showinfo("Welcome", "Registration successful")

    conn.close()

def UserLogin() -> None:
    username = username_entry2.get()
    password = password_entry2.get()

    if username == '' or password == '':
        messagebox.showerror("Username and/or password can not be empty. Please input a username and/or password.")
        return
    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()
    curs.execute("SELECT Password, Role FROM Users WHERE Username = ?",
                 (username, ))
    result = curs.fetchone()
    if result and result[0] == password:
        messagebox.showinfo("Welcome", "Successful login.")
        if result[1] == 'Admin':
            open_admin_UI()
        elif result[1] == 'Faculty':
            open_faculty_UI()
        elif result[1] == 'Student':
            open_student_UI()
    else:
        messagebox.showerror("Error", "Invalid username and/or password.")

###

# MAIN GUI

###

main_win = tk.Tk()
main_win.title("User Login")
main_win.state("zoomed")

username_label = tk.Label(main_win, text= "Username: ")
username_label.grid(row= 1, column= 0, padx= 5, pady= 5)

password_label = tk.Label(main_win, text= "Password: ")
password_label.grid(row= 2, column= 0, padx= 5, pady= 5)

role_label = tk.Label(main_win, text= "Role: ")
role_label.grid(row= 3, column= 0, padx= 5, pady= 5)

username_entry = tk.Entry(main_win)
username_entry.grid(row= 1, column= 1, padx= 5, pady= 5)

password_entry = tk.Entry(main_win, show="*")
password_entry.grid(row= 2, column= 1, padx= 5, pady= 5)

roles = ["Admin", "Student", "Faculty"]
role_dd = ttk.Combobox(main_win, values=roles, state="readonly")
role_dd.grid(row= 3, column= 1, padx= 5, pady= 5)

username_label2 = tk.Label(main_win, text= "Username: ")
username_label2.grid(row= 1, column= 2, padx= 5, pady= 5)

password_label2 = tk.Label(main_win, text= "Password: ")
password_label2.grid(row= 2, column= 2, padx= 5, pady= 5)

username_entry2 = tk.Entry(main_win)
username_entry2.grid(row= 1, column= 3, padx= 10, pady= 5)

password_entry2 = tk.Entry(main_win, show="*")
password_entry2.grid(row= 2, column= 3, padx= 5, pady= 5)
        
register_button = tk.Button(main_win, text= "Register", command= registercredentials)
register_button.grid(row= 4, column= 0, padx= 5, pady= 5)
    
login_button = tk.Button(main_win, text= "Login", command= UserLogin)
login_button.grid(row= 3, column= 2, padx= 5, pady= 5)

main_win.mainloop()


#if __name__ == "__main__":
