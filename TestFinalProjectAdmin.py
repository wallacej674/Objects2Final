from FinalProject import *

# ASSUMPTIONS FOR DATABASE INITIALIZATION
# Students: ID: 1 and 4, (info starts as blank)
# Faculty: ID: 3 and 5, (info starts as blank)
# Admin: ID: 2
# Course: ID = 1; Name = Math; Schedule = MW
# ID = 2 ; Name = Science ; Schedule = TR
# ID = 3 ; Name = History ; Schedule = F
# Exam: ExamID = 1; Name = MathFinal ; Date = MW ; CourseID = 1
# ExamID = 2; Name = ScienceFinal ; Date = TR ; CourseID = 2
# ExamID = 3; Name = HistoryFinal ; Date = F ; CourseID = 3


def testAdmin():
    conn = sqlite3.connect('Users.db')
    curs = conn.cursor()
    curs.execute('''SELECT * FROM Courses WHERE CourseID = ?''', (2,))
    course = curs.fetchone()

    # TEST COURSE CREATION
    assert course != None
    assert course[1] == 'Science'

    # TEST UPDATE COURSE
    # CHANGE NAME TO MATHEMATICS
    curs.execute('''SELECT * FROM Courses WHERE CourseID = ?''', (1,))
    course = curs.fetchone()

    assert course[1] == 'Mathematics'

    # TEST DELETE COURSE
    curs.execute('''SELECT * FROM Courses WHERE CourseID = ?''', (3,))
    course = curs.fetchone()

    assert course == None

    # TEST EXAM CREATION
    curs.execute('''SELECT * FROM Exams WHERE ExamID = ?''', (1,))
    exam = curs.fetchone()

    assert exam != None
    assert exam[1] == 'MathFinal'

    # TEST UPDATE EXAM
    # CHANGE NAME TO ScienceFinalExam
    curs.execute('''SELECT * FROM Exams WHERE ExamID = ?''', (2,))
    exam = curs.fetchone()

    assert exam[1] == 'ScienceFinalExam'

    # TEST DELETE EXAM
    curs.execute('''SELECT * FROM Exams WHERE ExamID = ?''', (3,))
    exam = curs.fetchone()

    assert exam == None

    # TEST UPDATE FACULTY PROFILE
    # SET Phone: 911, Email: faculty@shu.edu, Name: Professor, Qualifications: PHD
    curs.execute('''SELECT * FROM Faculty WHERE FacultyID = ?''', (3,))
    faculty = curs.fetchone()

    assert faculty != None
    assert faculty[1] == '911'
    assert faculty[4] == 'PHD'
    assert faculty[3] == 'Professor'

    # TEST UPDATE STUDENT PROFILE
    # SET Phone: 908, Email: student@shu.edu, Name: Student, Grade: Junior, GradYear: 2026
    curs.execute('''SELECT * FROM Students WHERE StudentID = ?''', (1,))
    student = curs.fetchone()

    assert student != None
    assert student[1] == '908'
    assert student[2] == 'student@shu.edu'
    assert student[3] == 'Student'
    assert student[4] == 'Junior'
    assert student[5] == '2026'

    # TEST Enrollment Creation (Student 1 to Course 1)
    curs.execute('''SELECT * FROM Enrollment WHERE StudentID = ?''', (1,))
    enrollment = curs.fetchone()

    assert enrollment != None
    assert enrollment[1] == 1

    # TEST CourseStaff Creation (Faculty 3 to Course 1)
    curs.execute('''SELECT * FROM CourseStaff WHERE FacultyID = ?''', (3,))
    coursestaff = curs.fetchone()

    assert coursestaff != None
    assert coursestaff[0] == 1

    # TEST Enrollment Deletion (Student 1 to Course 2)
    # ASSUMPTION: Enrollment was created and then deleted.
    curs.execute('''SELECT * FROM Enrollment WHERE CourseID = ?''', (2,))
    enrollment = curs.fetchone()

    assert enrollment == None

    # TEST CourseStaff Deletion (Faculty 3 to Course 2)
    # ASSUMPTION: CourseStaff was created then deleted.
    curs.execute('''SELECT * FROM CourseStaff WHERE CourseID = ?''', (2,))
    coursestaff = curs.fetchone()

    assert coursestaff == None

    # TEST Faculty Deletion
    curs.execute('''SELECT * FROM Faculty WHERE FacultyID = ?''', (5,))
    faculty = curs.fetchone()

    assert faculty == None

    # TEST Student Deletion
    curs.execute('''SELECT * FROM Students WHERE StudentID = ?''', (4,))
    student = curs.fetchone()

    assert student == None

testAdmin()

    
