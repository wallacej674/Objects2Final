def open_admin_UI() -> None:
    main_win.destroy()
    
    admin_win = tk.Tk()
    admin_win.title("Welcome Admin")
    admin_win.state("zoomed")

    # Purpose: Delete a student
    def deleteStudent() -> None:
        global delete_student_win
    
        if delete_student_win is None or not delete_student_win.winfo_exists():
            delete_student_win = tk.Toplevel()
            delete_student_win.title("Delete Student")
            delete_student_win.state("zoomed")

            studentIDlabel = tk.Label(delete_student_win, text= "Student ID: ")
            studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            studentIDentry = tk.Entry(delete_student_win)
            studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                studentID = studentIDentry.get()

                deletion_thread = threading.Thread(target=perform_deletion, args=(studentID,))
                deletion_thread.start()
                delete_student_win.destroy()
                    
            def perform_deletion(studentID: str) -> None:
                try:
                    with file_lock:
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
                            conn.close()

                            messagebox.showinfo("Success", "Student deleted successfully")
                        else:
                            messagebox.showerror("Failure", "Student not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_student_win, text= "Delete Student", command= save_changes)
            savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_student_win.lift()
    # Purpose: Delete Faculty
    def deleteFaculty() -> None:
        global delete_faculty_win
    
        if delete_faculty_win is None or not delete_faculty_win.winfo_exists():
            delete_faculty_win = tk.Toplevel()
            delete_faculty_win.title("Delete Faculty")
            delete_faculty_win.state("zoomed")

            facultyIDlabel = tk.Label(delete_faculty_win, text= "Faculty ID: ")
            facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            facultyIDentry = tk.Entry(delete_faculty_win)
            facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                facultyID = facultyIDentry.get()

                deletion_thread = threading.Thread(target=perform_deletion, args=(facultyID,))
                deletion_thread.start()
                delete_faculty_win.destroy()
                
            def perform_deletion(facultyID: str) -> None:
                try:
                    with file_lock:
                        conn = sqlite3.connect('Users.db')
                        curs = conn.cursor()
                        
                        curs.execute("SELECT * FROM Faculty WHERE FacultyID= ?",
                                     (facultyID,))
                        faculty = curs.fetchone()
                        if faculty:
                            curs.execute("DELETE FROM CourseStaff WHERE FacultyID = ?", (facultyID, ))
                            curs.execute("DELETE FROM Faculty WHERE FacultyID = ?", (facultyID, ))

                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Success", "Faculty deleted successfully")
                        else:
                            messagebox.showerror("Failure", "Faculty not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_faculty_win, text= "Delete Faculty", command= save_changes)
            savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_faculty_win.lift()
    # Purpose: Enrolls a student to a course
    def addStudentCourse() -> None:
        global add_enrollment_win

        if add_enrollment_win is None or not add_enrollment_win.winfo_exists():
            add_enrollment_win = tk.Toplevel()
            add_enrollment_win.title("Add Student to Course")
            add_enrollment_win.state("zoomed")

            studentIDlabel = tk.Label(add_enrollment_win, text= "Student ID: ")
            studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            studentIDentry = tk.Entry(add_enrollment_win)
            studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            coursenamelabel = tk.Label(add_enrollment_win, text= "Course Name: ")
            coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            coursenameentry = tk.Entry(add_enrollment_win)
            coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            courseschedulelabel = tk.Label(add_enrollment_win, text= "Course Schedule: ")
            courseschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            coursescheduleentry = tk.Entry(add_enrollment_win)
            coursescheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            coursescheduleinfolabel = tk.Label(add_enrollment_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
            coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

            def save_changes() -> None:
                studentID = studentIDentry.get()
                coursename = coursenameentry.get()
                courseschedule = coursescheduleentry.get()

                add_thread = threading.Thread(target=perform_add, args=(studentID, coursename, courseschedule))
                add_thread.start()
                add_enrollment_win.destroy()

            def perform_add(studentID: str, coursename: str, courseschedule: str) -> None:
                try:
                    with file_lock:
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
                                curs.execute("INSERT INTO Grades(CourseID, StudentID, student_grade) VALUES(?,?,?)",
                                             (courseID, studentID, 100.0))
                                conn.commit()
                                conn.close()
                                messagebox.showinfo("Successful", "Student added to Course")
                            else:
                                messagebox.showerror("Failure", "Student does not exist")
                        else:
                            messagebox.showerror("Failure", "Course does not exist")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            addbutton = tk.Button(add_enrollment_win, text= "Add Student", command= save_changes)
            addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            add_enrollment_win.lift()

    # Purpose: Delete an enrollment
    def deleteEnrollment() -> None:
        global delete_enrollment_win

        if delete_enrollment_win is None or not delete_enrollment_win.winfo_exists():
            delete_enrollment_win = tk.Toplevel()
            delete_enrollment_win.title("Delete Enrollment")
            delete_enrollment_win.state("zoomed")

            courseIDlabel = tk.Label(delete_enrollment_win, text= "Course ID: ")
            courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(delete_enrollment_win)
            courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            studentIDlabel = tk.Label(delete_enrollment_win, text= "Student ID: ")
            studentIDlabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            studentIDentry = tk.Entry(delete_enrollment_win)
            studentIDentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                courseID = courseIDentry.get()
                studentID = studentIDentry.get()

                deletion_thread = threading.Thread(target=perform_deletion, args=(studentID, courseID))
                deletion_thread.start()
                delete_enrollment_win.destroy()

            def perform_deletion(studentID: str, courseID: str) -> None:
                try:
                    with file_lock:
                        conn = sqlite3.connect('Users.db')
                        curs = conn.cursor()

                        curs.execute("SELECT * FROM Enrollment WHERE CourseID = ? AND StudentID = ?", (courseID, studentID))
                        enrollment = curs.fetchone()
                        
                        if enrollment:
                            curs.execute("DELETE FROM Enrollment WHERE CourseID= ? AND StudentID = ?", (courseID, studentID))

                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Successful", "Enrollment deleted successfully.")
                        else:
                            messagebox.showerror("Failure", "Enrollment not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_enrollment_win, text= "Delete Enrollment", command= save_changes)
            savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_enrollment_win.lift()

    # Purpose: Creates a course
    def createCourses() -> None:
        global course_creation_win

        if course_creation_win is None or not course_creation_win.winfo_exists():
            course_creation_win = tk.Toplevel()
            course_creation_win.title("Create Courses")
            course_creation_win.state("zoomed")

            coursenamelabel = tk.Label(course_creation_win, text= "Name: ")
            coursenamelabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            coursenameentry = tk.Entry(course_creation_win)
            coursenameentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            courseschedulelabel = tk.Label(course_creation_win, text= "Schedule: ")
            courseschedulelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            coursescheduleentry = tk.Entry(course_creation_win)
            coursescheduleentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            coursescheduleinfolabel = tk.Label(course_creation_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
            coursescheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

            def save_changes() -> None:
                newname = coursenameentry.get()
                newschedule = coursescheduleentry.get()

                create_thread = threading.Thread(target=perform_creation, args= (newname, newschedule))
                create_thread.start()
                course_creation_win.destroy()

            def perform_creation(newname: str, newschedule: str) -> None:
                try:
                    with file_lock:
                        conn = sqlite3.connect('Users.db')
                        curs = conn.cursor()

                        curs.execute("SELECT * FROM Courses WHERE CourseName=? AND Schedule=?",
                                     (newname, newschedule))
                        course = curs.fetchone()
                        if course:
                            messagebox.showerror("Error", "Course already exists.")
                            conn.close()
                        else:
                            curs.execute("INSERT INTO Courses(CourseName, Schedule) VALUES (?, ?)",
                                         (newname, newschedule))
                            conn.commit()
                            conn.close()
                            messagebox.showinfo("Successful", "Course added successfully.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()
                
            savebutton = tk.Button(course_creation_win, text= "Save Changes", command= save_changes)
            savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            course_creation_win.lift()

    # update a given course's information
    def updateCourse() -> None:
        global update_course_win

        if update_course_win is None or not update_course_win.winfo_exists():
            update_course_win = tk.Toplevel()
            update_course_win.title("Update Course")
            update_course_win.state("zoomed")

            courseIDlabel = tk.Label(update_course_win, text= "Course ID: ")
            courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(update_course_win)
            courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            coursenamelabel = tk.Label(update_course_win, text= "New Course Name: ")
            coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            coursenameentry = tk.Entry(update_course_win)
            coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            schedulelabel = tk.Label(update_course_win, text= "New Schedule: ")
            schedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            scheduleentry = tk.Entry(update_course_win)
            scheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            coursescheduleinfolabel = tk.Label(update_course_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
            coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

            def save_changes() -> None:
                CourseID = courseIDentry.get()
                newname = coursenameentry.get()
                newschedule = scheduleentry.get()

                update_thread = threading.Thread(target=perform_update, args= (CourseID, newname, newschedule))
                update_thread.start()
                update_course_win.destroy()
                
            def perform_update(CourseID: str, newname: str, newschedule: str) -> None:
                try:
                    with file_lock:
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
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(update_course_win, text= "Save Changes", command= save_changes)
            savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            update_course_win.lift()

    # Delete a course from the system
    def deleteCourse() -> None:
        global delete_course_win

        if delete_course_win is None or not delete_course_win.winfo_exists():
            delete_course_win = tk.Toplevel()
            delete_course_win.title("Delete Course")
            delete_course_win.state("zoomed")

            courseIDlabel = tk.Label(delete_course_win, text= "Course ID: ")
            courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(delete_course_win)
            courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                courseID = courseIDentry.get()
                deletion_thread = threading.Thread(target=perform_deletion, args=(courseID, ))
                deletion_thread.start()
                delete_course_win.destroy()

            def perform_deletion(courseID: str) -> None:
                try:
                    with file_lock:
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
                        else:
                            messagebox.showerror("Failure", "Course not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_course_win, text= "Delete Course", command= save_changes)
            savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_course_win.lift()

    # View a student's profile information
    def view_student_profile() -> None:
        global view_student_win

        if view_student_win is None or not view_student_win.winfo_exists():
            view_student_win = tk.Toplevel()
            view_student_win.title("View Profile")
            view_student_win.state("zoomed")

            studentIDlabel = tk.Label(view_student_win, text= "Student ID: ")
            studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            studentIDentry = tk.Entry(view_student_win)
            studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            def view_information() -> None:
                studentID = studentIDentry.get()

                view_thread = threading.Thread(target=perform_view, args=(studentID,))
                view_thread.start()
                
            def perform_view(studentID: str) -> None:
                try:
                    with file_lock:
                        conn = sqlite3.connect('Users.db')
                        curs = conn.cursor()

                        curs.execute("SELECT * FROM Students WHERE StudentID = ?", (studentID,))
                        student = curs.fetchone()

                        if student:
                            show_info(student)
                        else:
                            messagebox.showerror("Failure", "Student was not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            def show_info(student):
                info_win = tk.Toplevel()
                info_win.title("Student Profile")
                            
                infolabel = tk.Label(info_win, text=f"Phone: {student[1]} \n Email: {student[2]} \n Name: {student[3]}")
                infolabel.grid(row= 0, column= 0, padx= 5, pady= 5)

                academiclabel = tk.Label(info_win, text=f"Grade: {student[4]} \n Graduation Year: {student[5]}")
                academiclabel.grid(row= 0, column= 1,  padx= 5, pady= 5)
                
                    
            viewbutton = tk.Button(view_student_win, text= "View Profile", command= view_information)
            viewbutton.grid(row= 1, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            view_student_win.lift()

    # Updates the personal information of a student
    def update_student_profile() -> None:
        global update_student_win

        if update_student_win is None or not update_student_win.winfo_exists():
            update_student_win = tk.Toplevel()
            update_student_win.title("Update Profile")
            update_student_win.state("zoomed")

            studentIDlabel = tk.Label(update_student_win, text= "Student ID: ")
            studentIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            studentIDentry = tk.Entry(update_student_win)
            studentIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            phonelabel = tk.Label(update_student_win, text= "Student Phone:")
            phonelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            phoneentry = tk.Entry(update_student_win)
            phoneentry.grid(row= 1, column= 1, padx= 5, pady= 5)
        
            emaillabel = tk.Label(update_student_win, text= "Student Email:")
            emaillabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            emailentry = tk.Entry(update_student_win)
            emailentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            namelabel = tk.Label(update_student_win, text= "Student Name:")
            namelabel.grid(row= 3, column= 0, padx= 5, pady= 5)
            nameentry = tk.Entry(update_student_win)
            nameentry.grid(row= 3, column= 1, padx= 5, pady= 5)

            gradelabel = tk.Label(update_student_win, text= "Grade: ")
            gradelabel.grid(row= 4, column= 0, padx= 5, pady= 5)
            gradeentry = tk.Entry(update_student_win)
            gradeentry.grid(row= 4, column= 1, padx= 5, pady= 5)

            yearlabel = tk.Label(update_student_win, text= "Graduation Year: ")
            yearlabel.grid(row= 5, column= 0, padx= 5, pady= 5)
            yearentry = tk.Entry(update_student_win)
            yearentry.grid(row= 5, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                studentID = studentIDentry.get()
                newphone = phoneentry.get()
                newemail = emailentry.get()
                newname = nameentry.get()
                newgrade = gradeentry.get()
                newyear = yearentry.get()

                update_thread = threading.Thread(target=perform_update, args=(studentID, newphone, newemail, newname, newgrade, newyear))
                update_thread.start()
                update_student_win.destroy()

            def perform_update(studentID: str, newphone: str, newemail: str, newname: str, newgrade: str, newyear: str) -> None:
                try:
                    with file_lock:
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
                        else:
                            messagebox.showerror("Failure", "Student was not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(update_student_win, text= "Save Changes", command= save_changes)
            savebutton.grid(row= 6, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            update_student_win.lift()

    # Add a Faculty Member to a Course
    def addFacultyCourse() -> None:
        global add_courseStaff_win

        if add_courseStaff_win is None or not add_courseStaff_win.winfo_exists():
            add_courseStaff_win = tk.Toplevel()
            add_courseStaff_win.title("Add Faculty to Course")
            add_courseStaff_win.state("zoomed")

            facultyIDlabel = tk.Label(add_courseStaff_win, text= "Faculty ID: ")
            facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            facultyIDentry = tk.Entry(add_courseStaff_win)
            facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            coursenamelabel = tk.Label(add_courseStaff_win, text= "Course Name: ")
            coursenamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            coursenameentry = tk.Entry(add_courseStaff_win)
            coursenameentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            courseschedulelabel = tk.Label(add_courseStaff_win, text= "Course Schedule: ")
            courseschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            coursescheduleentry = tk.Entry(add_courseStaff_win)
            coursescheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            coursescheduleinfolabel = tk.Label(add_courseStaff_win, text= "Format Dates with Lettered Days (SuMTWRFSa): ##:## AM/PM - ##:## AM/PM \nExample: 'MW: 08:00 AM - 09:15 AM'")
            coursescheduleinfolabel.grid(row= 2, column= 2, padx= 5, pady= 5)

            def save_changes() -> None:
                facultyID = facultyIDentry.get()
                coursename = coursenameentry.get()
                courseschedule = coursescheduleentry.get()

                add_thread = threading.Thread(target=perform_add, args=(facultyID, coursename, courseschedule))
                add_thread.start()
                add_courseStaff_win.destroy()

            def perform_add(facultyID: str, coursename: str, courseschedule: str) -> None:
                try:
                    with file_lock:
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
                                curs.execute("INSERT INTO CourseStaff(CourseID, FacultyID) VALUES (?, ?)", (courseID, facultyID))
                                conn.commit()
                                messagebox.showinfo("Successful", "Faculty added to Course")

                                conn.close()
                            else:
                                messagebox.showerror("Failure", "Faculty does not exist")
                        else:
                            messagebox.showerror("Failure", "Course does not exist")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            addbutton = tk.Button(add_courseStaff_win, text= "Add Student", command= save_changes)
            addbutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            add_courseStaff_win.lift()

    # Delete a faculty from a course
    def deleteCourseStaff() -> None:
        global delete_CourseStaff_win

        if delete_CourseStaff_win is None or not delete_CourseStaff_win.winfo_exists():
            delete_CourseStaff_win = tk.Toplevel()
            delete_CourseStaff_win.title("Delete Staff from Course")
            delete_CourseStaff_win.state("zoomed")

            courseIDlabel = tk.Label(delete_CourseStaff_win, text= "Course ID: ")
            courseIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(delete_CourseStaff_win)
            courseIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            facultyIDlabel = tk.Label(delete_CourseStaff_win, text= "Faculty ID: ")
            facultyIDlabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            facultyIDentry = tk.Entry(delete_CourseStaff_win)
            facultyIDentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                courseID = courseIDentry.get()
                facultyID = facultyIDentry.get()

                deletion_thread = threading.Thread(target=perform_deletion, args=(courseID, facultyID))
                deletion_thread.start()
                delete_CourseStaff_win.destroy()

            def perform_deletion(courseID: str, facultyID: str) -> None:
                try:
                    with file_lock:
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
                            else:
                                messagebox.showerror("Failure", "Faculty not found.")
                        else:
                            messagebox.showerror("Failure", "Course not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_CourseStaff_win, text= "Delete Course", command= save_changes)
            savebutton.grid(row= 2, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_CourseStaff_win.lift()

    # Update a faculty member's profile
    def update_faculty_profile() -> None:
        global update_faculty_win

        if update_faculty_win is None or not update_faculty_win.winfo_exists():
            update_faculty_win = tk.Toplevel()
            update_faculty_win.title("Update Profile")
            update_faculty_win.state("zoomed")

            facultyIDlabel = tk.Label(update_faculty_win, text= "Faculty ID: ")
            facultyIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            facultyIDentry = tk.Entry(update_faculty_win)
            facultyIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            phonelabel = tk.Label(update_faculty_win, text= "Faculty Phone:")
            phonelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            phoneentry = tk.Entry(update_faculty_win)
            phoneentry.grid(row= 1, column= 1, padx= 5, pady= 5)
        
            emaillabel = tk.Label(update_faculty_win, text= "Faculty Email:")
            emaillabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            emailentry = tk.Entry(update_faculty_win)
            emailentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            namelabel = tk.Label(update_faculty_win, text= "Faculty Name:")
            namelabel.grid(row= 3, column= 0, padx= 5, pady= 5)
            nameentry = tk.Entry(update_faculty_win)
            nameentry.grid(row= 3, column= 1, padx= 5, pady= 5)

            quallabel = tk.Label(update_faculty_win, text= "Qualifications: ")
            quallabel.grid(row= 4, column= 0, padx= 5, pady= 5)
            qualentry = tk.Entry(update_faculty_win)
            qualentry.grid(row= 4, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                facultyID = facultyIDentry.get()
                newphone = phoneentry.get()
                newemail = emailentry.get()
                newname = nameentry.get()
                newqual = qualentry.get()

                update_thread = threading.Thread(target=perform_update, args=(facultyID, newphone, newemail, newname, newqual))
                update_thread.start()
                update_faculty_win.destroy()

            def perform_update(facultyID: str, newphone: str, newemail: str, newname: str, newqual: str) -> None:
                try:
                    with file_lock:
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
                        else:
                            messagebox.showerror("Failure", "Faculty was not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(update_faculty_win, text= "Save Changes", command= save_changes)
            savebutton.grid(row= 5, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            update_faculty_win.lift()

    # Create an Exam
    def createExam() -> None:
        global exam_creation_win

        if exam_creation_win is None or not exam_creation_win.winfo_exists():
            exam_creation_win = tk.Toplevel()
            exam_creation_win.title("Create Exams")
            exam_creation_win.state("zoomed")

            examnamelabel = tk.Label(exam_creation_win, text= "Name: ")
            examnamelabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            examnameentry = tk.Entry(exam_creation_win)
            examnameentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            examschedulelabel = tk.Label(exam_creation_win, text= "Schedule: ")
            examschedulelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            examscheduleentry = tk.Entry(exam_creation_win)
            examscheduleentry.grid(row= 1, column= 1, padx= 5, pady= 5)

            examscheduleinfolabel = tk.Label(exam_creation_win, text= "Format Dates: MM/DD/YYY \nExample: '09/20/2024'")
            examscheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

            courseIDlabel = tk.Label(exam_creation_win, text= "CourseID: ")
            courseIDlabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(exam_creation_win)
            courseIDentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                examname = examnameentry.get()
                examschedule = examscheduleentry.get()
                courseID = courseIDentry.get()

                create_thread = threading.Thread(target=perform_creation, args=(examname, examschedule, courseID))
                create_thread.start()
                exam_creation_win.destroy()

            def perform_creation(examname: str, examschedule: str, courseID: str) -> None:
                try:
                    with file_lock:
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
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()
                
            savebutton = tk.Button(exam_creation_win, text= "Save Changes", command= save_changes)
            savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            exam_creation_win.lift()

    # Update an exam's information
    def updateExam() -> None:
        global exam_update_win

        if exam_update_win is None or not exam_update_win.winfo_exists():
            exam_update_win = tk.Toplevel()
            exam_update_win.title("Update Exam")
            exam_update_win.state("zoomed")

            examIDlabel = tk.Label(exam_update_win, text= "Exam ID: ")
            examIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            examIDentry = tk.Entry(exam_update_win)
            examIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            examnamelabel = tk.Label(exam_update_win, text= "Exam Name: ")
            examnamelabel.grid(row= 1, column= 0, padx= 5, pady= 5)
            examnameentry = tk.Entry(exam_update_win)
            examnameentry.grid(row= 1, column= 1, padx = 5, pady= 5)

            examschedulelabel = tk.Label(exam_update_win, text= "Schedule: ")
            examschedulelabel.grid(row= 2, column= 0, padx= 5, pady= 5)
            examscheduleentry = tk.Entry(exam_update_win)
            examscheduleentry.grid(row= 2, column= 1, padx= 5, pady= 5)

            examscheduleinfolabel = tk.Label(exam_update_win, text= "Format Dates: MM/DD/YYY \nExample: '09/20/2024'")
            examscheduleinfolabel.grid(row= 1, column= 2, padx= 5, pady= 5)

            courseIDlabel = tk.Label(exam_update_win, text= "CourseID: ")
            courseIDlabel.grid(row= 3, column= 0, padx= 5, pady= 5)
            courseIDentry = tk.Entry(exam_update_win)
            courseIDentry.grid(row= 3, column= 1, padx= 5, pady= 5)

            def enter_info() -> None:
                examID = examIDentry.get()
                examname = examnameentry.get()
                examschedule = examscheduleentry.get()
                courseID = courseIDentry.get()

                update_thread = threading.Thread(target=perform_update, args=(examID, examname, examschedule, courseID))
                update_thread.start()
                exam_update_win.destroy()

            def perform_update(examID: str, examname: str, examschedule: str, courseID: str) -> None:
                try:
                    with file_lock:
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
                            else:
                                messagebox.showerror("Failure", "Course was not found")
                        else:
                            messagebox.showerror("Failure", "Exam was not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            exambutton = tk.Button(exam_update_win, text= "Update Exam", command= enter_info)
            exambutton.grid(row= 4, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            exam_update_win.lift()

    # Delete an Exam
    def deleteExam() -> None:
        global delete_exam_win

        if delete_exam_win is None or not delete_exam_win.winfo_exists():
            delete_exam_win = tk.Toplevel()
            delete_exam_win.title("Delete Exam")
            delete_exam_win.state("zoomed")

            examIDlabel = tk.Label(delete_exam_win, text= "Exam ID: ")
            examIDlabel.grid(row= 0, column= 0, padx= 5, pady= 5)
            examIDentry = tk.Entry(delete_exam_win)
            examIDentry.grid(row= 0, column= 1, padx= 5, pady= 5)

            def save_changes() -> None:
                examID = examIDentry.get()

                deletion_thread = threading.Thread(target=perform_deletion, args=(examID, ))
                deletion_thread.start()
                delete_exam_win.destroy()

            def perform_deletion(examID: str) -> None:
                try:
                    with file_lock:
                        conn = sqlite3.connect('Users.db')
                        curs = conn.cursor()

                        curs.execute("SELECT * FROM Exams WHERE ExamID = ?", (examID,))
                        exam = curs.fetchone()

                        if exam:
                            curs.execute("DELETE FROM Exams WHERE ExamID = ?", (examID,))
                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Successful", "Exam deleted successfully.")
                        else:
                            messagebox.showerror("Failure", "Exam not found.")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
                finally:
                    if conn:
                        conn.close()

            savebutton = tk.Button(delete_exam_win, text= "Delete Exam", command= save_changes)
            savebutton.grid(row= 3, column= 0, columnspan= 2, padx= 5, pady= 5)
        else:
            delete_exam_win.lift()

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

    delete_enrollment_button = tk.Button(student_frame, text= "Delete Enrollment", command= deleteEnrollment)
    delete_enrollment_button.pack(pady= 10)

    view_profile_button = tk.Button(student_frame, text= "View Student Information", command= view_student_profile)
    view_profile_button.pack(pady= 10)

    update_Sprofile_button = tk.Button(student_frame, text= "Update Student Profile", command= update_student_profile)
    update_Sprofile_button.pack(pady= 10)

    delete_faculty_button = tk.Button(faculty_frame, text= "Delete Faculty", command= deleteFaculty)
    delete_faculty_button.pack(pady= 10)

    add_faculty_to_course_button = tk.Button(faculty_frame, text= "Add Faculty to Course", command= addFacultyCourse)
    add_faculty_to_course_button.pack(pady= 10)

    delete_faculty_course_button = tk.Button(faculty_frame, text= "Delete Faculty from Course", command= deleteCourseStaff)
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
