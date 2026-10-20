
from dataclasses import dataclass, field


# Pet class
@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list["Task"] = field(default_factory=list)

    def get_info(self):
        """Return basic information about the pet."""
        return f"{self.name} is a {self.age}-year-old {self.species}."

    def add_task(self, task: "Task"):
        """Add a care task to this pet."""
        self.tasks.append(task)


# Task class
@dataclass
class Task:
    title: str
    duration: int
    priority: str
    pet: Pet
    frequency: str = "Daily"
    completed: bool = False

    def get_details(self):
        """Return a readable description of the task."""
        return f"{self.title} for {self.pet.name} ({self.duration} minutes)"

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True


# Owner class
@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Collect tasks from all pets."""
        all_tasks = []

        for pet in self.pets:
            all_tasks.extend(pet.tasks)

        return all_tasks

# PawPalSystem class

# PawPalSystem class
class PawPalSystem:
    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def add_task(self, task: Task):
        """Add a task to its assigned pet."""
        task.pet.add_task(task)

    def sort_tasks(self):
        """Sort incomplete tasks from all pets by priority."""
        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        tasks = self.owner.get_all_tasks()

        incomplete_tasks = [
            task for task in tasks
            if not task.completed
        ]

        return sorted(
            incomplete_tasks,
            key=lambda task: priority_order.get(task.priority, 4)
        )

    def generate_plan(self):
        """Create a daily schedule within the available time."""
        available_time = self.owner.available_minutes
        schedule = []

        for task in self.sort_tasks():
            if task.duration <= available_time:
                schedule.append(task)
                available_time -= task.duration

        return schedule

