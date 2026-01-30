"""
Sample Python File: UML Concepts Implementation with Multi-folder Structure
This file demonstrates Inheritance, Association, and Composition with classes spread across different modules.
"""

from entity import Entity
from profile import Profile
from department import Department
from user import User
from admin import Admin


# --- EXECUTION / TESTING ---
if __name__ == "__main__":
    # Create instances
    standard_user = User(101, "Alice", "alice@example.com")
    super_user = Admin(1, "Bob", "admin@corp.com", ["all"])

    # Demonstrate Association/Aggregation
    engineering = Department("Engineering")
    engineering.add_member(standard_user)
    engineering.add_member(super_user)

    print(f"Department: {engineering.dept_name}")
    for member in engineering.members:
        print(f" - {member.display_user()}")
