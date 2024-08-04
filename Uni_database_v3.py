import mysql.connector
import random

# اطلاعات اتصال به دیتابیس
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'student_db',
}

# اتصال به دیتابیس
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# ایجاد دیتابیس و جداول
cursor.execute("CREATE DATABASE IF NOT EXISTS student_db")
cursor.execute("USE student_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    math FLOAT,
    physics FLOAT,
    chemistry FLOAT,
    biology FLOAT,
    history FLOAT,
    geography FLOAT,
    english FLOAT,
    average FLOAT,
    rank INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(50),
    units INT
)
""")

# چک کردن جدول courses خالی است یا نه
cursor.execute("SELECT COUNT(*) AS count FROM courses")
row = cursor.fetchone()

if row[0] == 0:
    # وارد کردن واحدهای تصادفی برای 7 درس
    course_names = ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "English"]
    for course_name in course_names:
        units = random.randint(2, 4)
        cursor.execute("INSERT INTO courses (course_name, units) VALUES (%s, %s)", (course_name, units))
    conn.commit()

# گرفتن واحدهای درسی از جدول courses
cursor.execute("SELECT units FROM courses")
units = [row[0] for row in cursor.fetchall()]

# گرفتن اطلاعات دانشجویان از کاربر
students = []
num_students = int(input("Enter the number of students: "))

for _ in range(num_students):
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    grades = []
    for course_name in ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "English"]:
        grade = float(input(f"Enter grade for {course_name}: "))
        grades.append(grade)
    students.append({"first_name": first_name, "last_name": last_name, "grades": grades})

# محاسبه معدل و ذخیره اطلاعات در دیتابیس
for student in students:
    grades = student['grades']
    total_units = sum(units)
    total_points = sum(grades[i] * units[i] for i in range(7))
    average = total_points / total_units

    cursor.execute("""
        INSERT INTO students (first_name, last_name, math, physics, chemistry, biology, history, geography, english, average)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (student['first_name'], student['last_name'], *grades, average))
    conn.commit()

# به‌روزرسانی رتبه‌ها
cursor.execute("SELECT id, average FROM students ORDER BY average DESC")
rank = 1
for row in cursor.fetchall():
    cursor.execute("UPDATE students SET rank = %s WHERE id = %s", (rank, row[0]))
    rank += 1
    conn.commit()

# قطع اتصال به دیتابیس
cursor.close()
conn.close()
