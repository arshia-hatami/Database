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
    subjects = ["subject1", "subject2", "subject3", "subject4", "subject5", "subject6", "subject7"]
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


def database_maker():
    pass
