
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


def test_recurring_tasks():
    buddy = Pet("Buddy", "Dog", 3)

    # Daily recurring task
    daily_task = Task(
        "Walk", 30, "High", buddy,
        frequency="Daily",
        due_date="2026-10-20"
    )
    buddy.add_task(daily_task)

    next_daily = daily_task.mark_complete()

    assert daily_task.completed is True
    assert next_daily is not None
    assert next_daily.due_date == "2026-10-21"
    assert next_daily.completed is False
    assert len(buddy.tasks) == 2

    # Completing the same task again must not create duplicates
    assert daily_task.mark_complete() is None
    assert len(buddy.tasks) == 2

    # Weekly recurring task
    weekly_task = Task(
        "Groom", 20, "Medium", buddy,
        frequency="Weekly",
        due_date="2026-10-20"
    )
    buddy.add_task(weekly_task)

    next_weekly = weekly_task.mark_complete()

    assert next_weekly is not None
    assert next_weekly.due_date == "2026-10-27"
    assert next_weekly.completed is False


def test_conflict_detection():
    owner = Owner("Alex", 90)

    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(luna)

    system = PawPalSystem(owner)

    system.add_task(Task(
        "Walk", 30, "High", buddy,
        time="08:00", due_date="2026-10-20"
    ))

    system.add_task(Task(
        "Feed", 15, "High", luna,
        time="08:15", due_date="2026-10-20"
    ))

    system.add_task(Task(
        "Groom", 20, "Low", buddy,
        time="09:00", due_date="2026-10-20"
    ))

    conflicts = system.find_conflicts()

    assert len(conflicts) == 1
    assert "Buddy's Walk" in conflicts[0]
    assert "Luna's Feed" in conflicts[0]

def test_sort_tasks_by_time():
    owner = Owner("Alex", 90)
    buddy = Pet("Buddy", "Dog", 3)

    owner.add_pet(buddy)

    system = PawPalSystem(owner)

    system.add_task(Task(
        "Evening Walk", 30, "Medium", buddy,
        time="18:00"
    ))

    system.add_task(Task(
        "Breakfast", 15, "High", buddy,
        time="08:00"
    ))

    system.add_task(Task(
        "Medication", 10, "High", buddy,
        time="12:00"
    ))

    sorted_tasks = system.sort_by_time()

    assert [task.title for task in sorted_tasks] == [
        "Breakfast",
        "Medication",
        "Evening Walk"
    ]

def test_conflict_same_start_time():
    owner = Owner("Alex", 60)

    buddy = Pet("Buddy", "Dog", 3)
    luna = Pet("Luna", "Cat", 2)

    owner.add_pet(buddy)
    owner.add_pet(luna)

    system = PawPalSystem(owner)

    system.add_task(Task(
        "Walk", 30, "High", buddy,
        time="08:00", due_date="2026-10-20"
    ))

    system.add_task(Task(
        "Feed", 15, "High", luna,
        time="08:00", due_date="2026-10-20"
    ))

    conflicts = system.find_conflicts()

    assert len(conflicts) == 1
    assert "Buddy's Walk" in conflicts[0]
    assert "Luna's Feed" in conflicts[0]

def test_filter_no_matching_tasks():
    owner = Owner("Alex", 60)
    buddy = Pet("Buddy", "Dog", 3)

    owner.add_pet(buddy)

    system = PawPalSystem(owner)

    system.add_task(Task(
        "Walk", 30, "High", buddy
    ))

    system.add_task(Task(
        "Feed", 15, "Medium", buddy
    ))

    # Search for a pet that does not exist
    results = system.filter_tasks(pet_name="Luna")

    assert results == []

    # Search for completed tasks when none are completed
    completed_tasks = system.filter_tasks(completed=True)

    assert completed_tasks == []

def test_zero_available_time():
    owner = Owner("Alex", 0)
    buddy = Pet("Buddy", "Dog", 3)

    owner.add_pet(buddy)

    system = PawPalSystem(owner)

    system.add_task(Task(
        "Walk", 30, "High", buddy
    ))

    system.add_task(Task(
        "Feed", 15, "High", buddy
    ))

    schedule = system.generate_plan()

    assert schedule == []
    