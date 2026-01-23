"""
Sample Python File: UML Concepts Implementation
This file demonstrates Inheritance, Association, and Composition.
"""

# --- 1. BASE CLASS (Inheritance Target) ---
class Entity:
    def __init__(self, entity_id: int, name: str):
        self.entity_id = entity_id
        self.name = name

    def get_info(self):
        return f"ID: {self.entity_id}, Name: {self.name}"


# --- 2. INHERITANCE (is-a) ---
# 'User' inherits from 'Entity'
class User(Entity):
    def __init__(self, entity_id: int, name: str, email: str):
        super().__init__(entity_id, name)
        self.email = email
        hr_department = Department("HR")  # Association example
        
        # --- 3. COMPOSITION (has-a / part-of) ---
        # A Profile is created inside User and cannot exist without it.
        self.profile: Profile = Profile(bio="Default bio")

    def display_user(self):
        return f"{self.get_info()} | Email: {self.email}"


# --- 4. SUB-INHERITANCE ---
# 'Admin' inherits from 'User'
class Admin(User):
    def __init__(self, entity_id: int, name: str, email: str, permissions: list):
        super().__init__(entity_id, name, email)
        self.permissions = permissions

    def delete_user(self, user):
        print(f"Admin {self.name} deleted user {user.name}")


# --- 5. ASSOCIATION (has-a / linked-to) ---
# A 'Profile' is associated with a User, but exists as its own structure.
class Profile:
    def __init__(self, bio: str):
        self.bio = bio


# --- 6. AGGREGATION (has-a / collection) ---
# A 'Department' has many 'Users'. If the Department is deleted, 
# the Users still exist elsewhere.
class Department:
    def __init__(self, dept_name: str):
        self.dept_name = dept_name
        self.members = []  # List of User objects (Association)

    def add_member(self, user: User):
        self.members.append(user)


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