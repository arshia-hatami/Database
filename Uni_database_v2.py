import mysql.connector
import random

# تنظیمات اتصال به دیتابیس
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
    course1 FLOAT,
    course2 FLOAT,
    course3 FLOAT,
    course4 FLOAT,
    course5 FLOAT,
    course6 FLOAT,
    course7 FLOAT,
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

# چک کردن آیا جدول courses خالی است یا نه
cursor.execute("SELECT COUNT(*) AS count FROM courses")
row = cursor.fetchone()

if row[0] == 0:
    # وارد کردن واحدهای تصادفی برای 7 درس
    course_names = ["Course1", "Course2", "Course3", "Course4", "Course5", "Course6", "Course7"]
    for course_name in course_names:
        units = random.randint(2, 4)
        cursor.execute("INSERT INTO courses (course_name, units) VALUES (%s, %s)", (course_name, units))
    conn.commit()

# گرفتن واحدهای درسی از جدول courses
cursor.execute("SELECT units FROM courses")
units = [row[0] for row in cursor.fetchall()]

# گرفتن اطلاعات دانشجویان
students = [
    {"first_name": "Ali", "last_name": "Ahmadi", "grades": [15, 17, 16, 14, 18, 19, 20]},
    {"first_name": "Sara", "last_name": "Mohammadi", "grades": [13, 14, 15, 16, 17, 18, 19]},
    {"first_name": "Reza", "last_name": "Hosseini", "grades": [12, 13, 14, 15, 16, 17, 18]},
    {"first_name": "Mina", "last_name": "Karimi", "grades": [11, 12, 13, 14, 15, 16, 17]},
    {"first_name": "Hassan", "last_name": "Rahimi", "grades": [10, 11, 12, 13, 14, 15, 16]},
]

# محاسبه معدل و ذخیره اطلاعات در دیتابیس
for student in students:
    grades = student['grades']
    total_units = sum(units)
    total_points = sum(grades[i] * units[i] for i in range(7))
    average = total_points / total_units

    cursor.execute("""
        INSERT INTO students (first_name, last_name, course1, course2, course3, course4, course5, course6, course7, average)
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

# بستن اتصال به دیتابیس
cursor.close()
conn.close()
