#!/usr/bin/env python3

from __init__ import CONN, CURSOR
from department import Department
from employee import Employee
from review import Review
import ipdb


def reset_database():
    try:
        Review.drop_table()
        Employee.drop_table()
        Department.drop_table()
        print("Dropped existing tables.")
    except Exception as e:
        print(f"Error dropping tables: {e}")

    try:
        Department.create_table()
        Employee.create_table()
        Review.create_table()
        print("Created new tables.")
    except Exception as e:
        print(f"Error creating tables: {e}")

    # Create seed data
    try:
        payroll = Department.create("Payroll", "Building A, 5th Floor")
        human_resources = Department.create("Human Resources", "Building C, East Wing")
        print("Created departments.")

        employee1 = Employee.create("Lee", "Manager", payroll.id)
        employee2 = Employee.create("Sasha", "Manager", human_resources.id)
        print("Created employees.")

        Review.create(2023, "Efficient worker", employee1.id)
        Review.create(2022, "Good work ethic", employee1.id)
        Review.create(2023, "Excellent communication skills", employee2.id)
        print("Created reviews.")
    except Exception as e:
        print(f"Error creating seed data: {e}")

if __name__ == "__main__":
    reset_database()
    ipdb.set_trace()
