"""
Department class - aggregates users
"""


class Department:
    def __init__(self, dept_name: str):
        self.dept_name = dept_name
        self.members = []  # List of User objects (Association)

    def add_member(self, user):
        self.members.append(user)
