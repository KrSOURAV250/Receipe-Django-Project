from faker import Faker
from .models import *
import random
fake = Faker()


def seed_db(n=10) -> None:
    try:
        for _ in range(n):
            department_obj = Department.objects.all()
            r_index = random.randint(0, len(department_obj) - 1)
            department = department_obj[r_index]
            student_id = f"STU-0{random.randint(100, 999)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = fake.random.randint(18, 30)
            student_address = fake.address()
            stu_id = StudentID.objects.create(student_id=student_id)
            Student.objects.create(department=department, student_id=stu_id, student_name=student_name,
                                   student_email=student_email, student_age=student_age, student_address=student_address)
    except Exception as e:
        print(e)


def subject_marks():
    try:
        students = Student.objects.all()
        for student in students:
            subjects = Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    student=student, subject=subject, marks=random.randint(0, 100))
    except Exception as e:
        print(e)
