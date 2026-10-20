from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str
    age: int

    def get_info(self):
        pass


@dataclass
class Task:
    title: str
    duration: int
    priority: str
    pet: Pet

    def get_details(self):
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

class PawPalSystem:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        pass

    def sort_tasks(self):
        pass

    def generate_plan(self):
        pass