
from dataclasses import dataclass, field
from datetime import date, timedelta


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
    time: str = "08:00"
    due_date: str = ""

    def get_details(self):
        """Return a readable description of the task."""
        return f"{self.title} for {self.pet.name} ({self.duration} minutes)"

    def mark_complete(self):
        """Complete a task and create its next occurrence if recurring."""
        if self.completed:
            return None

        self.completed = True

        frequency = self.frequency.lower()

        if frequency == "daily":
            days = 1
        elif frequency == "weekly":
            days = 7
        else:
            return None

        current_date = (
            date.fromisoformat(self.due_date)
            if self.due_date
            else date.today()
        )

        next_date = current_date + timedelta(days=days)

        next_task = Task(
            title=self.title,
            duration=self.duration,
            priority=self.priority,
            pet=self.pet,
            frequency=self.frequency,
            time=self.time,
            due_date=next_date.isoformat()
        )

        self.pet.add_task(next_task)
        return next_task


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
    
    def find_conflicts(self):
        """Return warnings for overlapping incomplete tasks."""
        tasks = self.owner.get_all_tasks()
        conflicts = []

        active_tasks = [task for task in tasks if not task.completed]

        for i in range(len(active_tasks)):
            task1 = active_tasks[i]

            hour1, minute1 = map(int, task1.time.split(":"))
            start1 = hour1 * 60 + minute1
            end1 = start1 + task1.duration

            for j in range(i + 1, len(active_tasks)):
                task2 = active_tasks[j]

                if task1.due_date != task2.due_date:
                    continue

                hour2, minute2 = map(int, task2.time.split(":"))
                start2 = hour2 * 60 + minute2
                end2 = start2 + task2.duration

                if start1 < end2 and start2 < end1:
                    conflicts.append(
                        f"Conflict: {task1.pet.name}'s {task1.title} "
                        f"overlaps with {task2.pet.name}'s {task2.title}"
                    )

        return conflicts
    
    def sort_by_time(self):
        """Return all pet tasks sorted by scheduled time."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter tasks by pet name and completion status."""
        return [
            task for task in self.owner.get_all_tasks()
            if (pet_name is None or task.pet.name.lower() == pet_name.lower())
            and (completed is None or task.completed == completed)
        ]

    def generate_plan(self):
        """Create a daily schedule within the available time."""
        available_time = self.owner.available_minutes
        schedule = []

        for task in self.sort_tasks():
            if task.duration <= available_time:
                schedule.append(task)
                available_time -= task.duration

        return schedule

