"""
Base Entity class
"""


class Entity:
    def __init__(self, entity_id: int, name: str):
        self.entity_id = entity_id
        self.name = name

    def get_info(self):
        return f"ID: {self.entity_id}, Name: {self.name}"
