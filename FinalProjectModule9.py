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

course_popularity()
