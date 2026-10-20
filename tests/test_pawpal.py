
from pawpal_system import Owner, Pet, Task, PawPalSystem


def test_task_completion():
    """Test that a task can be marked complete."""
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Walk", 30, "High", buddy)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition():
    """Test that adding a task increases a pet's task count."""
    buddy = Pet("Buddy", "Dog", 3)
    task = Task("Walk", 30, "High", buddy)

    assert len(buddy.tasks) == 0

    buddy.add_task(task)

    assert len(buddy.tasks) == 1
    assert buddy.tasks[0] == task



def test_multi_pet_scheduler():
    """Verify the scheduler includes tasks from multiple pets."""
    owner = Owner("John", 60)

    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(luna)

    system = PawPalSystem(owner)

    system.add_task(Task("Walk", 30, "High", buddy))
    system.add_task(Task("Feed", 15, "High", luna))
    system.add_task(Task("Groom", 25, "Low", buddy))

    schedule = system.generate_plan()

    assert len(schedule) == 2
    assert [task.title for task in schedule] == ["Walk", "Feed"]
    assert {task.pet.name for task in schedule} == {"Buddy", "Luna"}
    assert sum(task.duration for task in schedule) <= owner.available_minutes
