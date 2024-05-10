#Contract: -> None
#Purpose: To create the faculty user interface window
def open_faculty_UI() -> None:
    faculty_win = tk.Toplevel()
    faculty_win.title("Faculty Dashboard")
    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()
    curs.execute(''' CREATE TABLE IF NOT EXISTS CourseMaterials (
                id INTEGER PRIMARY KEY,
                file_name TEXT,
                file_path TEXT
                )''')
    conn.commit()

    #Contract: -> None
    #Purpose: To provide a UI for adding course materials to the database
    def add_course_materials() -> None:
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
                    curs.execute('INSERT INTO CourseMaterials (file_name, file_path) VALUES (?, ?)', (file_name, file_path))
                    conn.commit()
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
    def view_course_materials() -> None:
        curs.execute('SELECT file_name, file_path FROM CourseMaterials')
        materials = curs.fetchall()
        
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
    def delete_course_materials():
        delete_materials_win = tk.Toplevel(faculty_win)
        delete_materials_win.title("Delete Course Materials")

        #Contract: -> None
        #Purpose: To delete the selected material from the database
        def delete_selected_material(material_id):
            curs.execute('DELETE FROM CourseMaterials WHERE id = ?', (material_id,))
            conn.commit()
            messagebox.showinfo("Success", "Material deleted successfully!")
            delete_materials_win.destroy()

        curs.execute('SELECT id, file_name FROM CourseMaterials')
        materials = curs.fetchall()

        selected_material_id = tk.IntVar()

        for material in materials:
            material_id, file_name = material
            tk.Radiobutton(delete_materials_win, text=file_name, variable=selected_material_id, value=material_id).pack()

        delete_button = tk.Button(delete_materials_win, text="Delete Selected Material",
                                  command=lambda: delete_selected_material(selected_material_id.get()))
        delete_button.pack()

    #Contract: -> None
    #Purpose: To display student progress and grades
    def view_student_progress():
        curs.execute('SELECT StudentID, CourseID, student_grade FROM Grades')
        grades = curs.fetchall()
        
        progress_win = tk.Toplevel(faculty_win)
        progress_win.title("Student Progress")

        for grade in grades:
            student_id, course_id, student_grade = grade
            grade_label = tk.Label(progress_win, text=f"Student ID: {student_id}, Course ID: {course_id}, Grade: {student_grade}")
            grade_label.pack()

    #Contract: -> None
    #Purpose: To manage assignments including adding, updating, and deleting them
    def manage_assignments():
        assignments_win = tk.Toplevel(faculty_win)
        assignments_win.title("Manage Assignments")

        #Contract: -> None
        #Purpose: To add a new assignment to the database
        def add_assignment():
            course_id = course_id_entry.get()
            assignment_name = assignment_name_entry.get()
            submission_date = submission_date_entry.get()
            curs.execute('INSERT INTO Assignments (CourseID, AssignmentName, SubmissionDate, Submitted) VALUES (?, ?, ?, ?)', 
                         (course_id, assignment_name, submission_date, False))
            conn.commit()
            messagebox.showinfo("Success", "Assignment added successfully!")

        #Contract: -> None
        #Purpose: To update an existing assignment in the database
        def update_assignment(assignment_id):
            updated_name = assignment_name_entry.get()
            updated_date = submission_date_entry.get()
            curs.execute('UPDATE Assignments SET AssignmentName = ?, SubmissionDate = ? WHERE AssignmentID = ?', 
                         (updated_name, updated_date, assignment_id))
            conn.commit()
            messagebox.showinfo("Success", "Assignment updated successfully!")

        #Contract: -> None
        #Purpose: To delete an existing assignment from the database
        def delete_assignment(assignment_id):
            curs.execute('DELETE FROM Assignments WHERE AssignmentID = ?', (assignment_id,))
            conn.commit()
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
                curs.execute('UPDATE Grades SET student_grade = ? WHERE StudentID = ? AND CourseID = ?', (grade, student_id, course_id))
                conn.commit()
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

    #Buttons for faculty UI functions
    add_materials_button = tk.Button(faculty_win, text="Add Course Materials", command=add_course_materials)
    add_materials_button.pack()

    view_materials_button = tk.Button(faculty_win, text="View Course Materials", command=view_course_materials)
    view_materials_button.pack()

    delete_materials_button = tk.Button(faculty_win, text="Delete Course Materials", command=delete_course_materials)
    delete_materials_button.pack()
    
    view_progress_button = tk.Button(faculty_win, text="View Student Progress", command=view_student_progress)
    view_progress_button.pack()

    manage_assignments_button = tk.Button(faculty_win, text="Manage Assignments", command=manage_assignments)
    manage_assignments_button.pack()

    main_win.mainloop()
