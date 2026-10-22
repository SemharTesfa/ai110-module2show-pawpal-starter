
from pawpal_system import Owner, Pet, Task, PawPalSystem

# Create an owner
owner = Owner("John", 60)
 
# Create two pets
buddy = Pet("Buddy", "Dog", 3)
luna = Pet("Luna", "Cat", 2)

# Add pets to the owner
owner.add_pet(buddy)
owner.add_pet(luna)

# Create the scheduler
system = PawPalSystem(owner)

# Add care tasks
system.add_task(Task("Walk", 30, "High", buddy))
system.add_task(Task("Feed", 15, "High", luna))
system.add_task(Task("Groom", 25, "Low", buddy))

# Generate today's schedule
schedule = system.generate_plan()

print("=== Today's Schedule ===")

for task in schedule:
    print(
        f"{task.pet.name}: {task.title} "
        f"- {task.duration} minutes "
        f"({task.priority} priority)"
    )

print(f"\nTotal scheduled tasks: {len(schedule)}")
print(f"Total scheduled time: {sum(task.duration for task in schedule)} minutes")


print("\n=== Tasks Sorted by Time ===")

# Add tasks in a different order from their scheduled times
time_owner = Owner("Alex", 90)
time_pet = Pet("Max", "Dog", 4)
time_owner.add_pet(time_pet)

time_system = PawPalSystem(time_owner)

time_system.add_task(Task(
    "Evening walk", 20, "Medium", time_pet, time="18:00"
))

time_system.add_task(Task(
    "Breakfast", 15, "High", time_pet, time="08:00"
))

time_system.add_task(Task(
    "Medication", 5, "High", time_pet, time="12:00"
))

for task in time_system.sort_by_time():
    print(f"{task.time} - {task.pet.name}: {task.title}")

print("\n=== Filter Tasks by Pet ===")

for task in system.filter_tasks(pet_name="Buddy"):
    print(f"{task.pet.name}: {task.title}")

print("\n=== Filter Incomplete Tasks ===")

for task in system.filter_tasks(completed=False):
    print(f"{task.pet.name}: {task.title}")

print("\n=== Filter Completed Tasks ===")

# Mark Buddy's Walk task as completed
buddy.tasks[0].mark_complete()

for task in system.filter_tasks(completed=True):
    print(f"{task.pet.name}: {task.title}")

print("\n=== Filter Tasks by Pet ===")

for task in system.filter_tasks(pet_name="Buddy"):
    print(f"{task.pet.name}: {task.title}")

print("\n=== Filter Incomplete Tasks ===")

for task in system.filter_tasks(completed=False):
    print(f"{task.pet.name}: {task.title}")

print("\n=== Filter Completed Tasks ===")

buddy.tasks[0].mark_complete()

for task in system.filter_tasks(completed=True):
    print(f"{task.pet.name}: {task.title}")


print("\n=== Conflict Detection ===")

conflict_owner = Owner("Alex", 90)

buddy2 = Pet("Buddy", "Dog", 3)
luna2 = Pet("Luna", "Cat", 2)

conflict_owner.add_pet(buddy2)
conflict_owner.add_pet(luna2)

conflict_system = PawPalSystem(conflict_owner)

conflict_system.add_task(Task(
    "Walk", 30, "High", buddy2,
    time="08:00", due_date="2026-10-20"
))

conflict_system.add_task(Task(
    "Feed", 15, "High", luna2,
    time="08:15", due_date="2026-10-20"
))

conflict_system.add_task(Task(
    "Groom", 20, "Low", buddy2,
    time="09:00", due_date="2026-10-20"
))

conflicts = conflict_system.find_conflicts()

if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No scheduling conflicts found.")
    