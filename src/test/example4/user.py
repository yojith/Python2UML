"""
User class - inherits from Entity, has Profile, associated with Department
"""

from entity import Entity
from userprofile import UserProfile
from department import Department


class User(Entity):
    def __init__(self, entity_id: int, name: str, email: str):
        super().__init__(entity_id, name)
        self.email = email
        hr_department = Department("HR")  # Association example

        # --- COMPOSITION (has-a / part-of) ---
        # A Profile is created inside User and cannot exist without it.
        self.profile: UserProfile = UserProfile(bio="Default bio")

    def display_user(self):
        return f"{self.get_info()} | Email: {self.email}"
