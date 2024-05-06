import tkinter as tk
import sqlite3
from tkinter import Tk, messagebox, ttk

### Current Problems ###
# UNCUSTOMIZED GUI
# Role GUIs incomplete




# Purpose: Create the user database
def createTables() -> None:
    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()

    curs.execute("DROP TABLE IF EXISTS Users")
    curs.execute("DROP TABLE IF EXISTS Admins")
    curs.execute("DROP TABLE IF EXISTS Faculty")
    curs.execute("DROP TABLE IF EXISTS Students")
    curs.execute("DROP TABLE IF EXISTS Courses")
    curs.execute("DROP TABLE IF EXISTS Enrollment")
    curs.execute("DROP TABLE IF EXISTS CourseStaff")

    curs.execute('''CREATE TABLE IF NOT EXISTS Users
                (UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, Role TEXT)''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Courses
                (CourseID INTEGER PRIMARY KEY AUTOINCREMENT, CourseName TEXT, Schedule TEXT
                )''')
    curs.execute('''CREATE TABLE IF NOT EXISTS Admins
                (AdminID INTEGER PRIMARY KEY, Phone TEXT, Email TEXT, Name TEXT,
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
    curs.execute('''CREATE TABLE IF NOT EXISTS Enrollment
                (CourseID INTEGER, StudentID INTEGER,
                PRIMARY KEY (CourseID, StudentID),
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
                )''')
    curs.execute('''CREATE TABLE IF NOT EXISTS CourseStaff
                (CourseID INTEGER, FacultyID INTEGER,
                PRIMARY KEY (CourseID, FacultyID),
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
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

    def addStudentCourse() -> None:
        add_win = tk.Tk()
        add_win.title("Add Student to Course")
        add_win.state("zoomed")

        studentIDlabel = tk.Label(add_win, text= "Student ID: ")
        studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        studentIDentry = tk.Entry(add_win)
        studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        coursenamelabel = tk.Label(add_win, text= "Course Name: ")
        coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        coursenameentry = tk.Entry(add_win)
        coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        courseschedulelabel = tk.Label(add_win, text= "Course Schedule: ")
        courseschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        coursescheduleentry = tk.Entry(add_win)
        coursescheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        coursescheduleinfolabel = tk.Label(add_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
        coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

        def save_changes() -> None:
            studentID = studentIDentry.get()
            coursename = coursenameentry.get()
            courseschedule = coursescheduleentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT CourseID FROM Courses WHERE CourseName= ? and Schedule= ?",
                         (coursename, courseschedule))
            courseID = curs.fetchone()
            if courseID:
                courseID = courseID[0]
                curs.execute("INSERT INTO Enrollment(CourseID, StudentID) VALUES (?, ?)",
                             (courseID, studentID))
                conn.commit()
                messagebox.showinfo("Successful", "Student added to Course")

                conn.close()
                add_win.destroy()
            else:
                messagebox.showerror("Failure", "Course does not exist")

        addbutton = tk.Button(add_win, text= "Add Student", command= save_changes)
        addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    def createCourses() -> None:
        course_win = tk.Tk()
        course_win.title("Create Courses")
        course_win.state("zoomed")

        coursenamelabel = tk.Label(course_win, text= "Name: ")
        coursenamelabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        coursenameentry = tk.Entry(course_win)
        coursenameentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        courseschedulelabel = tk.Label(course_win, text= "Schedule: ")
        courseschedulelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        coursescheduleentry = tk.Entry(course_win)
        coursescheduleentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        coursescheduleinfolabel = tk.Label(course_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
        coursescheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

        def save_changes() -> None:
            newname = coursenameentry.get()
            newschedule = coursescheduleentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Courses WHERE CourseName=? AND Schedule=?",
                         (newname, newschedule))
            course = curs.fetchone()
            if course:
                messagebox.showerror("Error", "Course already exists.")
            else:
                curs.execute("INSERT INTO Courses(CourseName, Schedule) VALUES (?, ?)",
                             (newname, newschedule))
                conn.commit()
                messagebox.showinfo("Successful", "Course added successfully.")

            conn.close()
            course_win.destroy()

        savebutton = tk.Button(course_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)

    def update_profile() -> None:
        update_win = tk.Tk()
        update_win.title("Update Profile")
        update_win.state("zoomed")

        studentIDlabel = tk.Label(update_win, text= "Student ID: ")
        studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        studentIDentry = tk.Entry(update_win)
        studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        phonelabel = tk.Label(update_win, text= "Student Phone:")
        phonelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        phoneentry = tk.Entry(update_win)
        phoneentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        emaillabel = tk.Label(update_win, text= "Student Email:")
        emaillabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        emailentry = tk.Entry(update_win)
        emailentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        namelabel = tk.Label(update_win, text= "Student Name:")
        namelabel.grid(row= 3, column= 0, padx= 5, pady= 5)
        nameentry = tk.Entry(update_win)
        nameentry.grid(row= 3, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            studentID = studentIDentry.get()
            newphone = phoneentry.get()
            newemail = emailentry.get()
            newname = nameentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Students WHERE StudentID = ?", (studentID,))
            student = curs.fetchone()
            if student:
                curs.execute("Update Students SET Phone= ?, Email= ?, Name= ? WHERE StudentID= ?",
                             (newphone, newemail, newname, studentID))
                conn.commit()
                conn.close()

                messagebox.showinfo("Successful Update", "Student's Personal Information has been updated")

                update_win.destroy()
            else:
                messagebox.showerror("Failure", "Student was not found.")

        savebutton = tk.Button(update_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 4, column= 0, columnspan= 2, padx= 5, pady= 5)

    create_courses_button = tk.Button(admin_win, text= "Create Courses", command= createCourses)
    create_courses_button.pack(pady= 10)

    add_student_to_course_button = tk.Button(admin_win, text= "Add Student to Course", command= addStudentCourse)
    add_student_to_course_button.pack(pady= 10)

    update_profile_button = tk.Button(admin_win, text= "Update Student Profile", command= update_profile)
    update_profile_button.pack(pady= 10)

    admin_win.mainloop()

def open_faculty_UI() -> None:
    faculty_win = tk.Tk()
    faculty_win.title("Welcome Faculty")
    faculty_win.state("zoomed")

def open_student_UI(username: str) -> None:
    student_win = tk.Tk()
    student_win.title("Welcome Student")
    student_win.state("zoomed")


    def view_courses():
        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()

        # Get the student's ID based on their username
        curs.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        student_id = curs.fetchone()[0]

        # Get the courses the student is enrolled in
        curs.execute("SELECT Courses.CourseName, Courses.Schedule FROM Enrollment "
                     "INNER JOIN Courses ON Enrollment.CourseID = Courses.CourseID "
                     "WHERE Enrollment.StudentID = ?", (student_id,))
        courses = curs.fetchall()

        conn.close()

        # Display the courses in a new window
        courses_win = tk.Toplevel(student_win)
        courses_win.title("Enrolled Courses")

        for i, (course_name, schedule) in enumerate(courses):
            tk.Label(courses_win, text=f"Course {i + 1}: {course_name} - {schedule}").pack()


    def register_class():
        pass

    def submit_assignment():
        pass

    def view_grades():
        pass

    def communicate_with_faculty():
        pass

    view_courses = tk.Button(student_win, text= "View Courses", command= view_courses)
    view_courses.pack(pady= 10)

    register_class = tk.Button(student_win, text= "Register for a Class", command= register_class)
    register_class.pack(pady= 10)


    submit_assignments = tk.Button(student_win, text= "submit assignments", command= submit_assignment)
    submit_assignments.pack(pady= 10)

    view_grades = tk.Button(student_win, text= "view grades", command= view_grades)
    view_grades.pack(pady= 10)

    communicate_with_fac = tk.Button(student_win, text= "communicate with faculty", command= communicate_with_faculty)
    communicate_with_fac.pack(pady= 10)


    student_win.mainloop()




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
        userid = curs.lastrowid
        if role == 'Admin':
            curs.execute("INSERT INTO Admins (AdminID) VALUES (?)",
                         (userid, ))
        elif role == 'Faculty':
            curs.execute("INSERT INTO Faculty (FacultyID) VALUES (?)",
                         (userid, ))
        elif role == 'Student':
            curs.execute("INSERT INTO Students (StudentID) VALUES (?)",
                         (userid, ))

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
            open_student_UI(username)
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

createTables()

main_win.mainloop()


#if __name__ == "__main__":
