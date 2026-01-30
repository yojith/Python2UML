"""
Admin class - inherits from User
"""

from user import User


class Admin(User):
    def __init__(self, entity_id: int, name: str, email: str, permissions: list):
        super().__init__(entity_id, name, email)
        self.permissions = permissions

    def delete_user(self, user):
        print(f"Admin {self.name} deleted user {user.name}")
