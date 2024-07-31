import mysql.connector
import random
import numpy


class Student:
    def __init__(self, first_name, last_name, grades):
        self.first_name = first_name
        self.last_name = last_name
        self.grades = grades
        self.moaddel = 0
        self.rank = 0


def random_units():
    subjects = ["Subject1", "Subject2", "Subject3", "Subject4", "Subject5", "Subject6", "Subject7"]
    units = [random.choice([2, 3, 4]) for _ in subjects]
    return dict(zip(subjects, units))


def calculate_moaddel(student, units):
    total_grade = sum(student.grades[i] * units[f"Subject{i + 1}"] for i in range(7))
    total_units = sum(units.values())
    return total_grade / total_units


def calculate_rank(students):
    moaddels = numpy.array([Student.moaddel for student in students])
    ranks = moaddels.argsort()[::-1].argsort() + 1
    for i, student in enumerate(students):
        student.rank = ranks[i]


def database_maker(cursor):
    students = [

        Student("mohammad", "khani", [90, 85, 73, 78, 97, 95, 89]),
        Student("ali", "moosavi", [86, 84, 92, 91, 92, 79, 94]),
        Student("reza", "razi", [86, 84, 92, 91, 92, 79, 94]),
        Student("arshia", "hatami", [86, 84, 90, 89, 93, 78, 97]),
        Student("ilia", "shahi", [68, 84, 90, 89, 93, 78, 74])
    ]

    units = random_units()

    for student in students:
        student.grades = calculate_moaddel(student, units)

    calculate_rank(students)

    connect = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="arshia"
    )
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS students
                      (id int AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), moaddel FLOAT, rank INT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS grades
                          (id int AUTO_INCREMENT PRIMARY KEY, students_id INT, subject VARCHAR(50), grade FLOAT, units INT,
                          FOREIGN KEY(students_id) REFERENCES students(id))""")

    for student in students:
        cursor.execute("INSERT INTO students (first_name, last_name, moaddel,rank) VALUES (%s, %s, %s, %s)",
                       (student.first_name, student.last_name, student.moaddel, student.rank))
    student_id = cursor.lastrowid
    for i in range(7):
        subject = f"Subject{i + 1}"
        cursor.execute("INSERT INTO grades (student_id, subject, grade, units) VALUES (%s, %s, %s, %s)",
                       (student_id, subject, student.grades[i], units[f"subject{i + 1}"]))

    connect.commit()
    cursor.close()
    connect.close()


database_maker()
