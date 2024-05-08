import tkinter as tk
import sqlite3
from tkinter import Tk, messagebox, ttk

### Current Problems ###
# UNCUSTOMIZED GUI
# Role GUIs incomplete
# Multithreading
# Network Server and Client
# Handle empty user inputs for updates to represent "do not update"
# Use information from piratenet records to aid in creating the database.
# Error Handling
# Window Duplication (can't have multiple of the same window)


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
    curs.execute("DROP TABLE IF EXISTS Grades")
    curs.execute("DROP TABLE IF EXISTS Exams")
    
    curs.execute('''CREATE TABLE IF NOT EXISTS Users
                (UserID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, Role TEXT)''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Courses
                (CourseID INTEGER PRIMARY KEY AUTOINCREMENT, CourseName TEXT, Schedule TEXT
                )''')
    curs.execute('''CREATE TABLE IF NOT EXISTS Admins
                (AdminID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT,
                FOREIGN KEY (AdminID) REFERENCES Users(UserID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Faculty
                (FacultyID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT, Qualifications TEXT,
                FOREIGN KEY (FacultyID) REFERENCES Users(UserID)
                )''')

    curs.execute('''CREATE TABLE IF NOT EXISTS Students
                (StudentID INTEGER PRIMARY KEY AUTOINCREMENT, Phone TEXT, Email TEXT, Name TEXT, Grade TEXT, Graduation TEXT,
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
    curs.execute(''' CREATE TABLE IF NOT EXISTS Grades(
                CourseID INTEGER, 
                FacultyID INTEGER,
                StudentID INTEGER,
                student_grade FLOAT,
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                FOREIGN KEY (FacultyID) REFERENCES Faculty(FacultyID))''')
    curs.execute(''' CREATE TABLE IF NOT EXISTS Exams
                (ExamID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Date TEXT, CourseID INTEGER,
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                )''')
    conn.commit()
    conn.close()

###

# ROLE GUIS

###

def open_admin_UI() -> None:
    main_win.destroy()
    
    admin_win = tk.Tk()
    admin_win.title("Welcome Admin")
    admin_win.state("zoomed")

    # Purpose: Delete a student
    def deleteStudent() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Student")
        delete_win.state("zoomed")

        studentIDlabel = tk.Label(delete_win, text= "Student ID: ")
        studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        studentIDentry = tk.Entry(delete_win)
        studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            studentID = studentIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            
            curs.execute("SELECT * FROM Students WHERE StudentID= ?",
                         (studentID,))
            student = curs.fetchone()
            if student:
                curs.execute("DELETE FROM Enrollment WHERE StudentID = ?", (studentID, ))
                curs.execute("DELETE FROM Students WHERE StudentID = ?", (studentID, ))
                curs.execute("DELETE FROM Grades WHERE StudentID = ?", (studentID, ))

                conn.commit()

                messagebox.showinfo("Success", "Student deleted successfully")
                delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Student not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Student", command= save_changes)
        savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
            
    # Purpose: Delete Faculty
    def deleteFaculty() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Faculty")
        delete_win.state("zoomed")

        facultyIDlabel = tk.Label(delete_win, text= "Faculty ID: ")
        facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        facultyIDentry = tk.Entry(delete_win)
        facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            facultyID = facultyIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            
            curs.execute("SELECT * FROM Faculty WHERE FacultyID= ?",
                         (facultyID,))
            faculty = curs.fetchone()
            if faculty:
                curs.execute("DELETE FROM CourseStaff WHERE FacultyID = ?", (facultyID, ))
                curs.execute("DELETE FROM Faculty WHERE FacultyID = ?", (facultyID, ))
                curs.execute("DELETE FROM Grades WHERE FacultyID = ?", (facultyID, ))

                conn.commit()

                messagebox.showinfo("Success", "Faculty deleted successfully")
                delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Faculty not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Faculty", command= save_changes)
        savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        
    # Purpose: Enrolls a student to a course
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
                curs.execute("SELECT * FROM Students WHERE StudentID= ?",
                             (studentID, ))
                student = curs.fetchone()
                if student:
                    courseID = courseID[0]
                    curs.execute("INSERT INTO Enrollment(CourseID, StudentID) VALUES (?, ?)",
                                 (courseID, studentID))
                    conn.commit()
                    messagebox.showinfo("Successful", "Student added to Course")

                    conn.close()
                    add_win.destroy()
                else:
                    messagebox.showerror("Failure", "Student does not exist")
                    add_win.destroy()
            else:
                messagebox.showerror("Failure", "Course does not exist")

                add_win.destroy()

        addbutton = tk.Button(add_win, text= "Add Student", command= save_changes)
        addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Purpose: Delete an enrollment
    def deleteEnrollment() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Enrollment")
        delete_win.state("zoomed")

        courseIDlabel = tk.Label(delete_win, text= "Course ID: ")
        courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(delete_win)
        courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        studentIDlabel = tk.Label(delete_win, text= "Student ID: ")
        studentIDlabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        studentIDentry = tk.Entry(delete_win)
        studentIDentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            courseID = courseIDentry.get()
            studentID = studentIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Enrollment WHERE CourseID = ? AND StudentID = ?", (courseID, studentID))
            enrollment = curs.fetchone()
            
            if enrollment:
                curs.execute("DELETE FROM Enrollment WHERE CourseID= ? AND StudentID = ?", (courseID, studentID))

                conn.commit()
                conn.close()

                messagebox.showinfo("Successful", "Enrollment deleted successfully.")
                delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Enrollment not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Enrollment", command= save_changes)
        savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Purpose: Creates a course
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

    # update a given course's information
    def updateCourse() -> None:
        update_win = tk.Tk()
        update_win.title("Update Course")
        update_win.state("zoomed")

        courseIDlabel = tk.Label(update_win, text= "Course ID: ")
        courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(update_win)
        courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        coursenamelabel = tk.Label(update_win, text= "New Course Name: ")
        coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        coursenameentry = tk.Entry(update_win)
        coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        schedulelabel = tk.Label(update_win, text= "New Schedule: ")
        schedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        scheduleentry = tk.Entry(update_win)
        scheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        coursescheduleinfolabel = tk.Label(update_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
        coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

        def save_changes() -> None:
            CourseID = courseIDentry.get()
            newname = coursenameentry.get()
            newschedule = scheduleentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Courses WHERE CourseID= ?",
                         (CourseID))
            course = curs.fetchone()
            if course:
                curs.execute("UPDATE Courses SET CourseName = ?, Schedule= ? WHERE CourseID= ?",
                             (newname, newschedule, CourseID))
                conn.commit()
                messagebox.showinfo("Successful", "Course updated successfully.")
            else:
                messagebox.showerror("Failure", "Course does not exist.")
                
            conn.close()
            update_win.destroy()

        savebutton = tk.Button(update_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Delete a course from the system
    def deleteCourse() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Course")
        delete_win.state("zoomed")

        courseIDlabel = tk.Label(delete_win, text= "Course ID: ")
        courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(delete_win)
        courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            courseID = courseIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Courses WHERE CourseID = ?", (courseID,))
            course = curs.fetchone()
            
            if course:
                curs.execute("DELETE FROM Courses WHERE CourseID = ?", (courseID,))
                curs.execute("DELETE FROM Enrollment WHERE CourseID = ?", (courseID,))
                curs.execute("DELETE FROM CourseStaff WHERE CourseID = ?", (courseID,))

                conn.commit()
                conn.close()

                messagebox.showinfo("Successful", "Course deleted successfully.")
                delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Course not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Course", command= save_changes)
        savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # View a student's profile information
    def view_student_profile() -> None:
        view_win = tk.Tk()
        view_win.title("View Profile")
        view_win.state("zoomed")

        studentIDlabel = tk.Label(view_win, text= "Student ID: ")
        studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        studentIDentry = tk.Entry(view_win)
        studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        def view_information() -> None:
            studentID = studentIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Students WHERE StudentID = ?", (studentID,))
            student = curs.fetchone()

            if student:
                info_win = tk.Toplevel(view_win)
                info_win.title("Student Profile")
                
                infolabel = tk.Label(info_win, text=f"Phone: {student[1]} \n Email: {student[2]} \n Name: {student[3]}")
                infolabel.grid(row= 0, column= 0, padx= 5, pady= 5)

                academiclabel = tk.Label(info_win, text=f"Grade: {student[4]} \n Graduation Year: {student[5]}")
                academiclabel.grid(row= 0, column= 1,  padx= 5, pady= 5)

                conn.close()
            else:
                messagebox.showerror("Failure", "Student was not found.")
                
        viewbutton = tk.Button(view_win, text= "View Profile", command= view_information)
        viewbutton.grid(row= 1, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Updates the personal information of a student
    def update_student_profile() -> None:
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

        gradelabel = tk.Label(update_win, text= "Grade: ")
        gradelabel.grid(row= 4, column= 0, padx= 5, pady= 5)
        gradeentry = tk.Entry(update_win)
        gradeentry.grid(row= 4, column= 1, padx= 5, pady= 5)

        yearlabel = tk.Label(update_win, text= "Graduation Year: ")
        yearlabel.grid(row= 5, column= 0, padx= 5, pady= 5)
        yearentry = tk.Entry(update_win)
        yearentry.grid(row= 5, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            studentID = studentIDentry.get()
            newphone = phoneentry.get()
            newemail = emailentry.get()
            newname = nameentry.get()
            newgrade = gradeentry.get()
            newyear = yearentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Students WHERE StudentID = ?", (studentID,))
            student = curs.fetchone()
            if student:
                curs.execute("Update Students SET Phone= ?, Email= ?, Name= ?, Grade= ?, Graduation= ? WHERE StudentID= ?",
                             (newphone, newemail, newname, newgrade, newyear, studentID))
                conn.commit()
                conn.close()

                messagebox.showinfo("Successful Update", "Student's Personal Information has been updated")

                update_win.destroy()
            else:
                messagebox.showerror("Failure", "Student was not found.")
                update_win.destroy()

        savebutton = tk.Button(update_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 6, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Add a Faculty Member to a Course
    def addFacultyCourse() -> None:
        add_win = tk.Tk()
        add_win.title("Add Faculty to Course")
        add_win.state("zoomed")

        facultyIDlabel = tk.Label(add_win, text= "Faculty ID: ")
        facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        facultyIDentry = tk.Entry(add_win)
        facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

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
            facultyID = facultyIDentry.get()
            coursename = coursenameentry.get()
            courseschedule = coursescheduleentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            
            curs.execute("SELECT CourseID FROM Courses WHERE CourseName= ? and Schedule= ?",
                         (coursename, courseschedule))
            courseID = curs.fetchone()
            if courseID:
                curs.execute("SELECT * FROM Faculty WHERE FacultyID= ?", (facultyID, ))
                faculty = curs.fetchone()
                if faculty:
                    courseID = courseID[0]
                    curs.execute("INSERT INTO CourseStaff(CourseID, FacultyID) VALUES (?, ?)",
                             (courseID, facultyID))

                    conn.commit()
                    messagebox.showinfo("Successful", "Faculty added to Course")

                else:
                    messagebox.showerror("Failure", "Faculty does not exist")

                conn.close()
                add_win.destroy()
            else:
                messagebox.showerror("Failure", "Course does not exist")
                add_win.destroy()

        addbutton = tk.Button(add_win, text= "Add Student", command= save_changes)
        addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Delete a faculty from a course
    def deleteCourseStaff() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Staff from Course")
        delete_win.state("zoomed")

        courseIDlabel = tk.Label(delete_win, text= "Course ID: ")
        courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(delete_win)
        courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        facultyIDlabel = tk.Label(delete_win, text= "Faculty ID: ")
        facultyIDlabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        facultyIDentry = tk.Entry(delete_win)
        facultyIDentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            courseID = courseIDentry.get()
            facultyID = facultyIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Courses WHERE CourseID = ?", (courseID,))
            course = curs.fetchone()
            
            if course:
                curs.execute("SELECT * FROM Faculty WHERE FacultyID= ?", (facultyID, ))
                faculty = curs.fetchone()
                if faculty:
                    curs.execute("DELETE FROM CourseStaff WHERE CourseID= ? AND FacultyID= ?", (courseID, facultyID))

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Successful", "Faculty has been deleted successfully from course.")
                    delete_win.destroy()
                else:
                    messagebox.showerror("Failure", "Faculty not found.")
                    delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Course not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Course", command= save_changes)
        savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Update a faculty member's profile
    def update_faculty_profile() -> None:
        update_win = tk.Tk()
        update_win.title("Update Profile")
        update_win.state("zoomed")

        facultyIDlabel = tk.Label(update_win, text= "Faculty ID: ")
        facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        facultyIDentry = tk.Entry(update_win)
        facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        phonelabel = tk.Label(update_win, text= "Faculty Phone:")
        phonelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        phoneentry = tk.Entry(update_win)
        phoneentry.grid(row= 1, column= 1, padx= 5, pady= 5)
    
        emaillabel = tk.Label(update_win, text= "Faculty Email:")
        emaillabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        emailentry = tk.Entry(update_win)
        emailentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        namelabel = tk.Label(update_win, text= "Faculty Name:")
        namelabel.grid(row= 3, column= 0, padx= 5, pady= 5)
        nameentry = tk.Entry(update_win)
        nameentry.grid(row= 3, column= 1, padx= 5, pady= 5)

        quallabel = tk.Label(update_win, text= "Qualifications: ")
        quallabel.grid(row= 4, column= 0, padx= 5, pady= 5)
        qualentry = tk.Entry(update_win)
        qualentry.grid(row= 4, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            facultyID = facultyIDentry.get()
            newphone = phoneentry.get()
            newemail = emailentry.get()
            newname = nameentry.get()
            newqual = qualentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Faculty WHERE FacultyID = ?", (facultyID,))
            staff = curs.fetchone()
            if staff:
                curs.execute("Update Faculty SET Phone= ?, Email= ?, Name= ?, Qualifications= ? WHERE FacultyID= ?",
                             (newphone, newemail, newname, newqual, facultyID))
                conn.commit()
                conn.close()

                messagebox.showinfo("Successful Update", "Faculty's Personal Information has been updated")

                update_win.destroy()
            else:
                messagebox.showerror("Failure", "Faculty was not found.")
                update_win.destroy()

        savebutton = tk.Button(update_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 5, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Create an Exam
    def createExam() -> None:
        exam_win = tk.Tk()
        exam_win.title("Create Exams")
        exam_win.state("zoomed")

        examnamelabel = tk.Label(exam_win, text= "Name: ")
        examnamelabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        examnameentry = tk.Entry(exam_win)
        examnameentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        examschedulelabel = tk.Label(exam_win, text= "Schedule: ")
        examschedulelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        examscheduleentry = tk.Entry(exam_win)
        examscheduleentry.grid(row= 1, column= 1, padx= 5, pady= 5)

        examscheduleinfolabel = tk.Label(exam_win, text= "Format Dates: MM/DD/YYY \nExample: '09/20/2024'")
        examscheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

        courseIDlabel = tk.Label(exam_win, text= "CourseID: ")
        courseIDlabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(exam_win)
        courseIDentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            examname = examnameentry.get()
            examschedule = examscheduleentry.get()
            courseID = courseIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Exams WHERE CourseID=? AND Name=? AND Date=?",
                         (courseID, examname, examschedule))
            exam = curs.fetchone()
            if exam:
                messagebox.showerror("Error", "Exam already exists.")
            else:
                curs.execute("SELECT * FROM Courses WHERE CourseID=?",
                             (courseID))
                course = curs.fetchone()
                if course:
                    curs.execute("INSERT INTO Exams(CourseID, Name, Date) VALUES (?, ?, ?)",
                             (courseID, examname, examschedule))
                    conn.commit()
                    messagebox.showinfo("Successful", "Exam added successfully.")
                else:
                    messagebox.showerror("Error", "Course does not exist")
            
            conn.close()
            exam_win.destroy()
            
        savebutton = tk.Button(exam_win, text= "Save Changes", command= save_changes)
        savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Update an exam's information
    def updateExam() -> None:
        exam_win = tk.Tk()
        exam_win.title("Update Exam")
        exam_win.state("zoomed")

        examIDlabel = tk.Label(exam_win, text= "Exam ID: ")
        examIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        examIDentry = tk.Entry(exam_win)
        examIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        examnamelabel = tk.Label(exam_win, text= "Exam Name: ")
        examnamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
        examnameentry = tk.Entry(exam_win)
        examnameentry.grid(row= 1, column= 1, padx = 5, pady= 5)

        examschedulelabel = tk.Label(exam_win, text= "Schedule: ")
        examschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
        examscheduleentry = tk.Entry(exam_win)
        examscheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

        examscheduleinfolabel = tk.Label(exam_win, text= "Format Dates: MM/DD/YYY \nExample: '09/20/2024'")
        examscheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

        courseIDlabel = tk.Label(exam_win, text= "CourseID: ")
        courseIDlabel.grid(row= 3, column= 0, padx= 5, pady= 5)
        courseIDentry = tk.Entry(exam_win)
        courseIDentry.grid(row= 3, column= 1, padx= 5, pady= 5)

        def enter_info() -> None:
            examID = examIDentry.get()
            examname = examnameentry.get()
            examschedule = examscheduleentry.get()
            courseID = courseIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Exams WHERE ExamID = ?", (examID,))
            exam = curs.fetchone()
            if exam:
                curs.execute("SELECT * FROM Courses WHERE CourseID=?",
                             (courseID))
                course = curs.fetchone()
                if course:
                    curs.execute("Update Exams SET Name= ?, Date= ?, CourseID= ? WHERE ExamID= ?",
                             (examname, examschedule, courseID, examID))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Successful Update", "Exam has been updated")

                    exam_win.destroy()
                else:
                    messagebox.showerror("Failure", "Course was not found")

                    exam_win.destroy()
            else:
                messagebox.showerror("Failure", "Exam was not found.")
                exam_win.destroy()

        exambutton = tk.Button(exam_win, text= "Choose Exam", command= enter_info)
        exambutton.grid(row= 4, column= 0, columnspan= 2, padx= 5, pady= 5)

    # Delete an Exam
    def deleteExam() -> None:
        delete_win = tk.Tk()
        delete_win.title("Delete Exam")
        delete_win.state("zoomed")

        examIDlabel = tk.Label(delete_win, text= "Exam ID: ")
        examIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
        examIDentry = tk.Entry(delete_win)
        examIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

        def save_changes() -> None:
            examID = examIDentry.get()

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()

            curs.execute("SELECT * FROM Exams WHERE ExamID = ?", (examID,))
            exam = curs.fetchone()
            
            if exam:
                curs.execute("DELETE FROM Exams WHERE ExamID = ?", (examID,))

                conn.commit()
                conn.close()

                messagebox.showinfo("Successful", "Exam deleted successfully.")
                delete_win.destroy()
            else:
                messagebox.showerror("Failure", "Exam not found.")
                delete_win.destroy()

        savebutton = tk.Button(delete_win, text= "Delete Exam", command= save_changes)
        savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    # FRAMES
    faculty_frame = tk.Frame(admin_win, bd=2, relief=tk.GROOVE)
    faculty_frame.grid(row= 0, column= 0, padx= 2, pady= 2, sticky= "nsew")
    faculty_title = tk.Label(faculty_frame, text= "Faculty")
    faculty_title.pack()
    
    student_frame = tk.Frame(admin_win, bd=2, relief=tk.GROOVE)
    student_frame.grid(row= 0, column= 1, padx= 2, pady= 2, sticky= "nsew")
    student_title = tk.Label(student_frame, text= "Student")
    student_title.pack()
    
    course_frame = tk.Frame(admin_win, bd=2, relief=tk.GROOVE)
    course_frame.grid(row= 1, column= 0, padx= 2, pady= 2, sticky= "nsew")
    course_title = tk.Label(course_frame, text= "Course")
    course_title.pack()
    
    other_frame = tk.Frame(admin_win, bd=2, relief=tk.GROOVE)
    other_frame.grid(row= 1, column= 1, padx= 2, pady= 2, sticky= "nsew")
    other_title = tk.Label(other_frame, text= "Other")
    other_title.pack()

    admin_win.rowconfigure(0, weight=1)
    admin_win.rowconfigure(1, weight=1)
    admin_win.columnconfigure(0, weight=1)
    admin_win.columnconfigure(1, weight=1)

    # BUTTONS 
    delete_student_button = tk.Button(student_frame, text= "Delete Student", command = deleteStudent)
    delete_student_button.pack(pady= 10)
    
    create_courses_button = tk.Button(course_frame, text= "Create Courses", command= createCourses)
    create_courses_button.pack(pady= 10)

    update_course_button = tk.Button(course_frame, text= "Update Course", command= updateCourse)
    update_course_button.pack(pady= 10)

    delete_course_button = tk.Button(course_frame, text= "Delete Course", command= deleteCourse)
    delete_course_button.pack(pady= 10)
    
    add_student_to_course_button = tk.Button(student_frame, text= "Add Student to Course", command= addStudentCourse)
    add_student_to_course_button.pack(pady= 10)

    delete_enrollment_button = tk.Button(other_frame, text= "Delete Enrollment", command= deleteEnrollment)
    delete_enrollment_button.pack(pady= 10)

    view_profile_button = tk.Button(student_frame, text= "View Student Information", command= view_student_profile)
    view_profile_button.pack(pady= 10)

    update_Sprofile_button = tk.Button(student_frame, text= "Update Student Profile", command= update_student_profile)
    update_Sprofile_button.pack(pady= 10)

    delete_faculty_button = tk.Button(faculty_frame, text= "Delete Faculty", command= deleteFaculty)
    delete_faculty_button.pack(pady= 10)

    add_faculty_to_course_button = tk.Button(faculty_frame, text= "Add Faculty to Course", command= addFacultyCourse)
    add_faculty_to_course_button.pack(pady= 10)

    delete_faculty_course_button = tk.Button(other_frame, text= "Delete Faculty from Course", command= deleteCourseStaff)
    delete_faculty_course_button.pack(pady= 10)

    update_Fprofile_button = tk.Button(faculty_frame, text= "Update Faculty Profile", command= update_faculty_profile)
    update_Fprofile_button.pack(pady= 10)

    create_exam_button = tk.Button(other_frame, text= "Create Exams", command= createExam)
    create_exam_button.pack(pady= 10)

    update_exam_button = tk.Button(other_frame, text= "Update Exams", command= updateExam)
    update_exam_button.pack(pady= 10)

    delete_exam_button = tk.Button(other_frame, text= "Delete Exams", command= deleteExam)
    delete_exam_button.pack(pady= 10)

    admin_win.update()
    admin_win.mainloop()
    
def open_faculty_UI() -> None:
    main_win.destroy()
    
    faculty_win = tk.Tk()
    faculty_win.title("Welcome Faculty")
    faculty_win.state("zoomed")

def open_student_UI(username: str) -> None:
    main_win.destroy()
    
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

        def save_changes() -> None:

            conn = sqlite3.connect('Users.db')
            curs = conn.cursor()
            # Get the student's ID based on their username
            curs.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
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
                conn.commit()
                messagebox.showinfo("Successful", "Added to Course!")

                conn.close()
                student_win.destroy()
            else:
                messagebox.showerror("Failure", "Course does not exist")

        addbutton = tk.Button(course_win, text= "Add Course", command= save_changes)
        addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)

    def submit_assignment():
        pass

    def view_grades():
        conn = sqlite3.connect('Users.db')
        curs = conn.cursor()

        # Get the student's ID based on their username
        curs.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
        student_id = curs.fetchone()[0]

         # Get the grades for the student
        curs.execute("SELECT CourseName, student_grade FROM Grades "
                    "INNER JOIN Courses ON Grades.CourseID = Courses.CourseID "
                    "WHERE StudentID = ?", (student_id,))
        grades = curs.fetchall()
        conn.close()

        grades_win = tk.Toplevel(student_win)
        grades_win.title("Grades")
        for i, (course_name, grade) in enumerate(grades):
            tk.Label(grades_win, text=f"Course: {course_name} - Grade: {grade}").pack()

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


# USER FUNCTIONS


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

main_win.mainloop()


#if __name__ == "__main__":
