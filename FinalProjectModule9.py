import sqlite3
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

def course_popularity():
    conn = sqlite3.connect("Users.db")
    curs = conn.cursor()
    
    curs.execute("SELECT CourseID, CourseName FROM Courses")
    courses = curs.fetchall()
    
    course_names = []
    enrollment_counts = []
    
    for course_id, course_name in courses:
        curs.execute("SELECT * FROM Enrollment WHERE CourseID = ?", (course_id,))
        enrollments = curs.fetchall()
        count = len(enrollments)
        
        course_names.append(course_name)
        enrollment_counts.append(count)
    
    curs.close()
    conn.close()

    plt.figure(figsize=(10, 8))
    plt.bar(course_names, enrollment_counts, color='blue')
    plt.xlabel('Course Name')
    plt.ylabel('Number of Students Enrolled')
    plt.title('Popularity of Courses Based on Enrollment')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    plt.show()

def student_performance(student_id: int):
    conn = sqlite3.connect("Users.db")
    curs = conn.cursor()

    curs.execute("SELECT Courses.CourseName, Grades.student_grade FROM Courses "
                 "INNER JOIN Grades ON Courses.CourseID = Grades.CourseID "
                 "WHERE Grades.StudentID = ?", (student_id,))
    data = curs.fetchall()

    conn.close()

    course_names = [row[0] for row in data]
    grades = [row[1] for row in data]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(course_names, grades, color='skyblue')
    plt.xlabel('Courses')
    plt.ylabel('Grades')
    plt.title('Student Performance')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout() 

    plt.show()

def faculty_workload(faculty_id: int):
    conn = sqlite3.connect("Users.db")
    curs = conn.cursor()

    curs.execute("SELECT COUNT(CourseID) FROM CourseStaff WHERE FacultyID = ?", (faculty_id,))
    course_count = curs.fetchone()[0]

    curs.execute("SELECT COUNT(StudentID) FROM Enrollment WHERE CourseID IN "
                 "(SELECT CourseID FROM CourseStaff WHERE FacultyID = ?)", (faculty_id,))
    student_count = curs.fetchone()[0]

    conn.close()

    categories = ['Courses', 'Students']
    counts = [course_count, student_count]

    plt.bar(categories, counts, color=['blue', 'orange'])
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Faculty Stats')
    plt.show()

faculty_workload(3)
    
