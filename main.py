
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
