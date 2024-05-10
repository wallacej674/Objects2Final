import tkinter as tk
import sqlite3
import threading
from tkinter import Tk, messagebox, ttk, filedialog
import socket
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3





class CollegeDatabase:


    #to initialize a college database
    def __init__(self, db_name='Users.db'):
        self.db_name = db_name
        self.conn = None
        self.curs = None
        self.lock = threading.Lock()


    #to enter a cursor safely into a database
    def __enter__(self) -> 'Database':
        self.conn =sqlite3.connect(self.db_name, check_same_thread=False)
        self.curs = self.conn.cursor()
        return self

    #to safely exit the database connection
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.conn:
            self.conn.close()


    def execute_query(self, query: str, params: tuple = ()) -> None:
        with self.lock:
            #check if a database connection does not exist and establish one if needed.
            if not self.conn:
                self.conn = sqlite3.connect(self.db_name)
            #Execute thr SQL query using the connection. Automatically manage transaction commit/rollback
            with self.conn:
                self.curs.execute(query, params)


    def fetch_query(self, query: str, params: tuple = ()) -> list[tuple]:
        #fetch results from a SQL query with optional parameters.
        with self.lock:
            self.curs.execute(query,params)
            return self.curs.fetchall()


    def create_tables(self):
        self.curs.execute("DROP TABLE IF EXISTS Users")
        self.curs.execute("DROP TABLE IF EXISTS Admins")
        self.curs.execute("DROP TABLE IF EXISTS Faculty")
        self.curs.execute("DROP TABLE IF EXISTS Students")
        self.curs.execute("DROP TABLE IF EXISTS Courses")
        self.curs.execute("DROP TABLE IF EXISTS Enrollment")
        self.curs.execute("DROP TABLE IF EXISTS CourseStaff")
        self.curs.execute("DROP TABLE IF EXISTS Grades")
        self.curs.execute("DROP TABLE IF EXISTS Exams")

        self.curs.execute('''CREATE TABLE IF NOT EXISTS Users
                    (UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, Role TEXT)''')

        self.curs.execute('''CREATE TABLE IF NOT EXISTS Courses
                    (CourseID INTEGER PRIMARY KEY AUTOINCREMENT, CourseName TEXT, Schedule TEXT
                    )''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS Admins
                    (AdminID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT,
                    FOREIGN KEY (AdminID) REFERENCES Users(UserID)
                    )''')

        self.curs.execute('''CREATE TABLE IF NOT EXISTS Faculty
                    (FacultyID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT, Qualifications TEXT,
                    FOREIGN KEY (FacultyID) REFERENCES Users(UserID)
                    )''')

        self.curs.execute('''CREATE TABLE IF NOT EXISTS Students
                    (StudentID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT, Grade TEXT, Graduation TEXT,
                    FOREIGN KEY (StudentID) REFERENCES Users(UserID)
                    )''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS Enrollment
                    (CourseID INTEGER, StudentID INTEGER,
                    PRIMARY KEY (CourseID, StudentID),
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
                    )''')
        self.curs.execute('''CREATE TABLE IF NOT EXISTS CourseStaff
                    (CourseID INTEGER, FacultyID INTEGER,
                    PRIMARY KEY (CourseID, FacultyID),
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                    FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID)
                    )''')
        self.curs.execute(''' CREATE TABLE IF NOT EXISTS Grades(
                    CourseID INTEGER, 
                    StudentID INTEGER,
                    student_grade FLOAT,
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                    FOREIGN KEY (StudentID) REFERENCES Students(StudentID))''')
        self.curs.execute(''' CREATE TABLE IF NOT EXISTS Exams
                    (ExamID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Date TEXT, CourseID INTEGER,
                    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                    )''')

        self.curs.execute(''' CREATE TABLE IF NOT EXISTS Assignments(
                    AssignmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                    StudentID INTEGER,
                    CourseID INTEGER,
                    AssignmentName TEXT,
                    SubmissionDate TEXT,
                    File TEXT,
                    Score REAL DEFAULT -1,
                    Submitted BOOLEAN,
        FOREIGN KEY(StudentID) REFERENCES Users(UserID),
        FOREIGN KEY(CourseID) REFERENCES Courses(CourseID))
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()










class FacultyUI:
    def __init__(self):
        self.faculty_win = tk.Toplevel()
        self.faculty_win.title("Faculty Dashboard")
        self.conn = sqlite3.connect('Users.db')
        self.curs = self.conn.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS CourseMaterials (
                            id INTEGER PRIMARY KEY,
                            file_name TEXT,
                            file_path TEXT
                            )''')
        self.conn.commit()

        self.create_buttons()

    #contract: self -> None
    #purpose: creates the different buttons that would be used in the Faculty UI
    def create_buttons(self):
        add_materials_button = tk.Button(self.faculty_win, text="Add Course Materials", command=self.add_course_materials)
        add_materials_button.pack()

        view_materials_button = tk.Button(self.faculty_win, text="View Course Materials", command=self.view_course_materials)
        view_materials_button.pack()

        delete_materials_button = tk.Button(self.faculty_win, text="Delete Course Materials", command=self.delete_course_materials)
        delete_materials_button.pack()

        view_progress_button = tk.Button(self.faculty_win, text="View Student Progress", command=self.view_student_progress)
        view_progress_button.pack()

        manage_assignments_button = tk.Button(self.faculty_win, text="Manage Assignments", command=self.manage_assignments)
        manage_assignments_button.pack()


    #Contract: -> None
    #Purpose: To provide a UI for adding course materials to the database
    def add_course_materials(self) -> None:
        file_path = filedialog.askopenfilename()
        if file_path:
            name_window = tk.Toplevel()
            name_window.title("Enter File Name")

            name_label = tk.Label(name_window, text="Enter the name for the file:")
            name_label.pack()
            name_entry = tk.Entry(name_window)
            name_entry.pack()

            #Contract: -> None
            #Purpose: To save the provided file name and path to the database
            def save_file_name() -> None:
                file_name = name_entry.get()
                if file_name:
                    self.curs.execute('INSERT INTO CourseMaterials (file_name, file_path) VALUES (?, ?)', (file_name, file_path))
                    self.conn.commit()
                    messagebox.showinfo("Success", "Material added successfully!")
                    name_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter a file name.")

            save_button = tk.Button(name_window, text="Save", command=save_file_name)
            save_button.pack()

        else:
            messagebox.showinfo("Failure", "No file selected.")



    #Contract: -> None
    #Purpose: To display a list of course materials and allow opening them
    def view_course_materials(self) -> None:
        self.curs.execute('SELECT file_name, file_path FROM CourseMaterials')
        materials = self.curs.fetchall()

        materials_win = tk.Toplevel()
        materials_win.title("Course Materials")

        for material in materials:
            file_name, file_path = material
            tk.Label(materials_win, text=file_name).pack()

            #Contract: -> None
            #Purpose: To open the selected course material file
            def open_file(path=file_path) -> None:
                # Implement the logic to open the file here
                with open(path, 'r') as file:
                    #Reads the entire content of the file
                    content = file.read()

                # Create a new window to display the file content
                file_win = tk.Toplevel()
                file_win.title("File Content")

                # Create a text box and insert the file content
                text_box = tk.Text(file_win)
                text_box.insert('1.0', content)
                text_box.pack()

            open_button = tk.Button(materials_win, text="Open", command=open_file)
            open_button.pack()


    #Contract: -> None
    #Purpose: To provide a UI for deleting course materials from the database
    def delete_course_materials(self):
        delete_materials_win = tk.Toplevel(self.faculty_win)
        delete_materials_win.title("Delete Course Materials")

        #Contract: -> None
        #Purpose: To delete the selected material from the database
        def delete_selected_material(material_id):
            self.curs.execute('DELETE FROM CourseMaterials WHERE id = ?', (material_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Material deleted successfully!")
            delete_materials_win.destroy()

        self.curs.execute('SELECT id, file_name FROM CourseMaterials')
        materials = self.curs.fetchall()

        selected_material_id = tk.IntVar()

        for material in materials:
            material_id, file_name = material
            tk.Radiobutton(delete_materials_win, text=file_name, variable=selected_material_id, value=material_id).pack()

        delete_button = tk.Button(delete_materials_win, text="Delete Selected Material",
                                  command=lambda: delete_selected_material(selected_material_id.get()))
        delete_button.pack()


    #Contract: -> None
    #Purpose: To display student progress and grades
    def view_student_progress(self):
        self.curs.execute('SELECT StudentID, CourseID, student_grade FROM Grades')
        grades = self.curs.fetchall()

        progress_win = tk.Toplevel(self.faculty_win)
        progress_win.title("Student Progress")

        for grade in grades:
            student_id, course_id, student_grade = grade
            grade_label = tk.Label(progress_win, text=f"Student ID: {student_id}, Course ID: {course_id}, Grade: {student_grade}")
            grade_label.pack()


    #Contract: -> None
    #Purpose: To manage assignments including adding, updating, and deleting them
    def manage_assignments(self):
        assignments_win = tk.Toplevel(self.faculty_win)
        assignments_win.title("Manage Assignments")

        #Contract: -> None
        #Purpose: To add a new assignment to the database
        def add_assignment():
            course_id = course_id_entry.get()
            assignment_name = assignment_name_entry.get()
            submission_date = submission_date_entry.get()

            self.curs.execute('SELECT StudentID FROM Students')
            student_ids = self.curs.fetchall()

            for student_id_tuple in student_ids:
                student_id = student_id_tuple[0]
                self.curs.execute('INSERT INTO Assignments (CourseID, AssignmentName, SubmissionDate, Submitted, StudentID) VALUES (?, ?, ?, ?, ?)',
                             (course_id, assignment_name, submission_date, False, student_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Assignment added successfully!")

        #Contract: -> None
        #Purpose: To update an existing assignment in the database
        def update_assignment(assignment_id):
            updated_name = assignment_name_entry.get()
            updated_date = submission_date_entry.get()
            self.curs.execute('UPDATE Assignments SET AssignmentName = ?, SubmissionDate = ? WHERE AssignmentID = ?',
                         (updated_name, updated_date, assignment_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Assignment updated successfully!")

        #Contract: -> None
        #Purpose: To delete an existing assignment from the database
        def delete_assignment(assignment_id):
            self.curs.execute('DELETE FROM Assignments WHERE AssignmentID = ?', (assignment_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Assignment deleted successfully!")

        #Contract: -> None
        #Purpose: To grade a student's assignment
        def grade_assignment() -> None:
            # Create a new window for grading assignments
            grade_win = tk.Toplevel()
            grade_win.title("Grade Assignment")

            # Create an entry field for the student ID
            student_id_label = tk.Label(grade_win, text="Student ID:")
            student_id_label.pack()
            student_id_entry = tk.Entry(grade_win)
            student_id_entry.pack()

            # Create an entry field for the grade
            grade_label = tk.Label(grade_win, text="Grade:")
            grade_label.pack()
            grade_entry = tk.Entry(grade_win)
            grade_entry.pack()

            #Contract: -> None
            #Purpose: To save the grade for the student
            def save_grade() -> None:
                course_id = course_id_entry.get()
                student_id = student_id_entry.get()
                grade = grade_entry.get()
                self.curs.execute('UPDATE Grades SET student_grade = ? WHERE StudentID = ? AND CourseID = ?', (grade, student_id, course_id))
                self.conn.commit()
                messagebox.showinfo("Success", f"Grade updated successfully for student {student_id}!")
                grade_win.destroy()

            # Create a button to save the grade
            save_button = tk.Button(grade_win, text="Save Grade", command=save_grade)
            save_button.pack()

        #Widgets for assignment details
        course_id_label = tk.Label(assignments_win, text="Course ID:")
        course_id_label.pack()
        course_id_entry = tk.Entry(assignments_win)
        course_id_entry.pack()

        assignment_name_label = tk.Label(assignments_win, text="Assignment Name:")
        assignment_name_label.pack()
        assignment_name_entry = tk.Entry(assignments_win)
        assignment_name_entry.pack()

        submission_date_label = tk.Label(assignments_win, text="Submission Date:")
        submission_date_label.pack()
        submission_date_entry = tk.Entry(assignments_win)
        submission_date_entry.pack()

        # Buttons for adding, updating, and deleting assignments
        add_button = tk.Button(assignments_win, text="Add Assignment", command=add_assignment)
        add_button.pack()

        assignment_id = 1  # Placeholder for the selected assignment ID
        update_button = tk.Button(assignments_win, text="Update Selected Assignment", command=lambda: update_assignment(assignment_id))
        update_button.pack()

        delete_button = tk.Button(assignments_win, text="Delete Selected Assignment", command=lambda: delete_assignment(assignment_id))
        delete_button.pack()

        grade_button = tk.Button(assignments_win, text="Grade Assignment", command= grade_assignment)
        grade_button.pack()

    def run(self):
        self.faculty_win.mainloop()






class StudentUI:
    #contract: self, str -> None
    #to initialize student
    def __init__(self, username: str) -> None:
        self.username = username
        self.student_win = tk.Tk()
        self.student_win.title("Welcome Student")
        self.student_win.state("zoomed")

        self.create_widgets()

    #contract: self -> None
    #purpose: to create the visuals for the initial gui
    def create_widgets(self) -> None:
        view_courses_btn = tk.Button(self.student_win, text="View Courses", command=self.view_courses)
        view_courses_btn.pack(pady=10)

        register_class_btn = tk.Button(self.student_win, text="Register for a Class", command=self.register_class)
        register_class_btn.pack(pady=10)

        submit_assignments_btn = tk.Button(self.student_win, text="Submit Assignments", command=self.submit_assignment)
        submit_assignments_btn.pack(pady=10)

        view_grades_btn = tk.Button(self.student_win, text="View Grades", command=self.view_grades)
        view_grades_btn.pack(pady=10)

    #contract: self -> None
    #purpose: to add courses to a window
    def view_courses(self) -> None:
        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()

        # Get the student's ID based on their username
        curs.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
        student_id = curs.fetchone()[0]

        # Get the courses the student is enrolled in
        curs.execute("SELECT Courses.CourseName, Courses.Schedule FROM Enrollment "
                     "INNER JOIN Courses ON Enrollment.CourseID = Courses.CourseID "
                     "WHERE Enrollment.StudentID = ?", (student_id,))
        courses = curs.fetchall()

        conn.close()

        # Display the courses in a new window
        courses_win = tk.Toplevel(self.student_win)
        courses_win.title("Enrolled Courses")

        for i, (course_name, schedule) in enumerate(courses):
            tk.Label(courses_win, text=f"Course {i + 1}: {course_name} - {schedule}").pack()


    #contract -> None
    #to register a student to a course that exist
    def register_class(self) -> None:
        course_win = tk.Tk()
        course_win.title("Add Student to Course")
        course_win.state("zoomed")

        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()
        coursenamelabel = tk.Label(course_win, text= "Course Name: ")
        coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        coursenameentry = tk.Entry(course_win)
        coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        courseschedulelabel = tk.Label(course_win, text= "Course Schedule: ")
        courseschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        coursescheduleentry = tk.Entry(course_win)
        coursescheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        coursescheduleinfolabel = tk.Label(course_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
        coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

        #to save the change made to the course
        def save_changes() -> None:

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            # Get the student's ID based on their username
            curs.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
            studentID = curs.fetchone()[0]

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
                curs.execute("INSERT INTO Grades(CourseID, StudentID, student_grade) VALUES(?,?,?)",
                             (courseID, studentID, 100.0))
                conn.commit()
                messagebox.showinfo("Successful", "Added to Course!")

                conn.close()
                self.student_win.destroy()
            else:
                messagebox.showerror("Failure", "Course does not exist")

        addbutton = tk.Button(course_win, text= "Add Course", command= save_changes)
        addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    #contract: self -> None
    #purpose: allows a user to submit assignments and
    def submit_assignment(self) -> None:
        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()

        # Get the student's ID based on their username
        curs.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
        student_id = curs.fetchone()[0]

        # Get the assignments for the student
        curs.execute("SELECT AssignmentID, AssignmentName FROM Assignments WHERE StudentID = ?", (student_id,))
        assignments = curs.fetchall()

        conn.close()

        #checks to see if there are assignments
        if not assignments:
            messagebox.showinfo("No Assignments", "You have no assignments to submit.")
            return

        # Display the assignments in a new window
        submit_win = tk.Toplevel(self.student_win)
        submit_win.title("Submit Assignment")

        assignment_var = tk.StringVar()
        assignment_var.set(assignments[0][0])  # Default to the first assignment

        for assignment_id, assignment_name in assignments:
            tk.Radiobutton(submit_win, text=assignment_name, variable=assignment_var, value=assignment_id).pack()

        #contract: self -> None
        #purpose: to upload a file to the db
        def upload_file() -> None:
            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            file_path = filedialog.askopenfilename()
            if file_path:
                # Logic to handle the file upload
                # For example, you might copy the file to a specific directory
                # and store the path in the database

                # Update the database with the file path
                selected_assignment_id = assignment_var.get()
                curs.execute("UPDATE Assignments SET Submitted = ?, FilePath = ? WHERE AssignmentID = ?",
                             (1, file_path, selected_assignment_id))
                conn.commit()
                messagebox.showinfo("Success", "File uploaded successfully!")
                submit_win.destroy()

        upload_button = tk.Button(submit_win, text="Upload File", command=upload_file)
        upload_button.pack(pady=10)

    #contract: self -> None
    #this allows students to view the grades that exist for the classes that a student is registered for
    def view_grades(self) -> None:
        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()

        # Get the student's ID based on their username
        curs.execute("SELECT UserID FROM Users WHERE Username = ?", (self.username,))
        student_id = curs.fetchone()[0]

        # Get the grades for the student
        curs.execute("SELECT CourseName, student_grade FROM Grades "
                     "INNER JOIN Courses ON Grades.CourseID = Courses.CourseID "
                     "WHERE StudentID = ?", (student_id,))
        grades = curs.fetchall()
        conn.close()

        grades_win = tk.Toplevel(self.student_win)
        grades_win.title("Grades")
        for i, (course_name, grade) in enumerate(grades):
            tk.Label(grades_win, text=f"Course: {course_name} - Grade: {grade}").pack()

    #runs the student gui
    def run(self):
        self.student_win.mainloop()






class UserAuthenticationSystem:
    def __init__(self):
        self.main_win = tk.Tk()
        self.main_win.title("User Login")
        self.main_win.state("zoomed")

        self.create_tables()

        self.create_register_side()
        self.create_login_side()

        self.main_win.mainloop()

    def create_tables(self):
        try:
            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            curs.execute('''CREATE TABLE IF NOT EXISTS Users
                        (UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                         Username TEXT NOT NULL,
                         Password TEXT NOT NULL,
                         Role TEXT NOT NULL)''')

            curs.execute('''CREATE TABLE IF NOT EXISTS Admins
                        (AdminID INTEGER PRIMARY KEY,
                         FOREIGN KEY (AdminID) REFERENCES Users(UserID))''')

            curs.execute('''CREATE TABLE IF NOT EXISTS Faculty
                        (FacultyID INTEGER PRIMARY KEY,
                         FOREIGN KEY (FacultyID) REFERENCES Users(UserID))''')

            curs.execute('''CREATE TABLE IF NOT EXISTS Students
                        (StudentID INTEGER PRIMARY KEY,
                         FOREIGN KEY (StudentID) REFERENCES Users(UserID))''')

            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            if conn:
                conn.close()

    def register_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_dd.get()

        if username == '' or password == '' or role == '':
            messagebox.showerror("Registration Failed", "Username, password and/or role cannot be empty. Please input a username and/or password.")
            return

        try:
            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            curs.execute("SELECT * FROM Users WHERE Username = ?", (username, ))
            if curs.fetchone():
                messagebox.showerror("Error", "Username already exists. Please try again.")
            else:
                curs.execute("INSERT INTO Users(Username, Password, Role) VALUES (?, ?, ?)", (username, password, role))
                userid = curs.lastrowid
                if role == 'Admin':
                    curs.execute("INSERT INTO Admins (AdminID) VALUES (?)", (userid, ))
                elif role == 'Faculty':
                    curs.execute("INSERT INTO Faculty (FacultyID) VALUES (?)", (userid, ))
                elif role == 'Student':
                    curs.execute("INSERT INTO Students (StudentID) VALUES (?)", (userid, ))

                conn.commit()
                conn.close()
                messagebox.showinfo("Welcome", "Registration successful")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            if conn:
                conn.close()

    def user_login(self):
        username = self.username_entry2.get()
        password = self.password_entry2.get()

        if username == '' or password == '':
            messagebox.showerror("Login Failed", "Username and/or password cannot be empty. Please input a username and/or password.")
            return

        try:
            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            curs.execute("SELECT Password, Role FROM Users WHERE Username = ?", (username, ))
            result = curs.fetchone()
            if result and result[0] == password:
                messagebox.showinfo("Welcome", "Successful login.")
                if result[1] == 'Admin':
                    self.open_admin_UI()
                elif result[1] == 'Faculty':
                    self.open_faculty_UI()
                elif result[1] == 'Student':
                    self.open_student_UI(username)
            else:
                messagebox.showerror("Error", "Invalid username and/or password.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            if conn:
                conn.close()

    def create_register_side(self):
        register_frame = tk.Frame(self.main_win)
        register_frame.grid(row=0, column=0, padx=20, pady=20)

        username_label = tk.Label(register_frame, text="Username: ")
        username_label.grid(row=0, column=0, padx=5, pady=5)

        self.username_entry = tk.Entry(register_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        password_label = tk.Label(register_frame, text="Password: ")
        password_label.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(register_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        role_label = tk.Label(register_frame, text="Role: ")
        role_label.grid(row=2, column=0, padx=5, pady=5)

        roles = ["Admin", "Student", "Faculty"]
        self.role_dd = ttk.Combobox(register_frame, values=roles, state="readonly")
        self.role_dd.grid(row=2, column=1, padx=5, pady=5)

        register_button = tk.Button(register_frame, text="Register", command=self.register_credentials)
        register_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def create_login_side(self):
        login_frame = tk.Frame(self.main_win)
        login_frame.grid(row=0, column=1, padx=20, pady=20)

        username_label = tk.Label(login_frame, text="Username: ")
        username_label.grid(row=0, column=0, padx=5, pady=5)

        self.username_entry2 = tk.Entry(login_frame)
        self.username_entry2.grid(row=0, column=1, padx=5, pady=5)

        password_label = tk.Label(login_frame, text="Password: ")
        password_label.grid(row=1, column=0, padx=5, pady=5)

        self.password_entry2 = tk.Entry(login_frame, show="*")
        self.password_entry2.grid(row=1, column=1, padx=5, pady=5)

        login_button = tk.Button(login_frame, text="Login", command=self.user_login)
        login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    #opens the respective ui's in the system
    def open_admin_UI(self):
        pass


    def open_faculty_UI(self):
        FacultyUI().run()

    #contract: self, str -> None
    #purpose: opens the student UI
    def open_student_UI(self, username):
        StudentUI(username).run()


UserAuthenticationSystem()