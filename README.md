# 🐾 PawPal+ — Module 2 Project

PawPal+ is a Python and Streamlit pet-care scheduling application that helps owners organize daily care tasks based on priority, available time, and scheduled activities.

The project demonstrates object-oriented programming, scheduling algorithms, automated testing, UML system design, and AI-assisted software development.

## Scenario

A busy pet owner needs help managing responsibilities such as walking, feeding, medication, grooming, and enrichment.

PawPal+ helps the owner:

- Manage multiple pets and their care tasks.
- Assign task priorities and scheduled times.
- Generate a daily care plan within an available time budget.
- Identify overlapping tasks.
- Track completed and incomplete activities.
- Automatically create future occurrences of recurring tasks.

## Features

### Pet Management

- Add pets with a name, species, and age.
- Associate care tasks with individual pets.
- View all registered pets in the Streamlit interface.

### Task Management

- Create tasks with a title, duration, priority, and scheduled time.
- Assign tasks to a specific pet.
- Track task completion status.
- Support daily and weekly recurrence in the backend.

### Smart Scheduling

PawPal+ includes the following algorithms:

| Feature | Method | Description |
|---|---|---|
| Priority sorting | `PawPalSystem.sort_tasks()` | Orders incomplete tasks by High, Medium, and Low priority. |
| Time sorting | `PawPalSystem.sort_by_time()` | Sorts tasks chronologically by scheduled start time. |
| Task filtering | `PawPalSystem.filter_tasks()` | Filters tasks by pet name or completion status. |
| Daily scheduling | `PawPalSystem.generate_plan()` | Selects priority-based tasks within the owner's available time. |
| Conflict detection | `PawPalSystem.find_conflicts()` | Detects overlapping incomplete tasks scheduled for the same date. |
| Task recurrence | `Task.mark_complete()` | Marks a task complete and creates the next daily or weekly occurrence when applicable. |

The scheduling algorithm prioritizes important tasks while respecting the owner's available time.

Conflict detection reports overlapping activities but does not automatically reschedule them. The daily plan also does not currently enforce conflict-free scheduling.

### Streamlit User Interface

The interactive application supports:

- Adding and viewing pets.
- Creating care tasks.
- Displaying tasks in a table.
- Sorting tasks by scheduled time.
- Filtering tasks by pet and by completion status (All, Incomplete, or Completed).
- Displaying scheduling conflict warnings.
- Marking a task complete with the **Mark Task Complete** button.
- Generating a daily care schedule.
- Displaying success and warning messages.

These UI behaviors were verified by driving the running app with Streamlit's `AppTest` framework: adding pets and tasks, conflict warnings, completing a task, and each filter combination.

Not yet available in the UI: choosing a recurrence frequency (tasks created in the interface always use the backend default of daily recurrence), and editing or deleting tasks.

## Project Architecture

PawPal+ uses four main Python classes.

| Class | Responsibility |
|---|---|
| `Owner` | Stores owner information, available time, pets, and preferences. |
| `Pet` | Stores pet information and associated care tasks. |
| `Task` | Represents a care activity, its scheduling information, completion status, and recurrence. |
| `PawPalSystem` | Coordinates task management, sorting, filtering, conflict detection, and schedule generation. |

The final UML diagram is stored in:

`diagrams/uml_final.mmd`

The diagram illustrates class attributes, methods, and relationships based on the final Python implementation.

## Getting Started

### Requirements

- Python 3
- Streamlit
- pytest
- Dependencies listed in `requirements.txt`

### Installation

Clone or download the project repository and open the project folder in a terminal.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

### Run the Streamlit Application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open it in your browser to use PawPal+.

### Run the Command-Line Demonstration

```bash
python main.py
```

This demonstrates the scheduling behavior using example pets and care tasks.

## 📸 Demo Walkthrough

### 1. Launch the Application

Run:

```bash
python -m streamlit run app.py
```

The main screen displays the application title, owner information, available time, and pet-management controls.

For example:

```text
PawPal+

Current owner: Jordan
Available time: 60 minutes
```

### 2. Add a Pet

Enter the following information:

| Field | Example |
|---|---|
| Pet name | Buddy |
| Species | Dog |
| Age | 3 |

Click **Add Pet**.

The application displays a success message and adds Buddy to the pet list.

### 3. Create Care Tasks

Select Buddy and add the following activities:

| Task | Time | Duration | Priority |
|---|---|---|---|
| Morning Walk | 08:00 | 30 minutes | High |
| Breakfast | 09:00 | 15 minutes | High |
| Grooming | 18:00 | 25 minutes | Low |

Each task is associated with the selected pet.

### 4. View Tasks Sorted by Time

The application displays scheduled tasks in chronological order.

Example:

```text
08:00  Buddy  Morning Walk  30 minutes  High
09:00  Buddy  Breakfast     15 minutes  High
18:00  Buddy  Grooming      25 minutes  Low
```

The `sort_by_time()` algorithm orders tasks by their scheduled start time.

### 5. Filter Tasks

The **Filter by pet** and **Filter by status** dropdowns above the task table use `filter_tasks()` and can be combined.

For example, selecting **Incomplete Tasks** displays tasks that have not been marked complete.

Selecting **Completed Tasks** displays only completed activities.

### 6. Detect Scheduling Conflicts

Suppose the owner creates two tasks:

| Task | Start Time | Duration |
|---|---|---|
| Morning Walk | 08:00 | 30 minutes |
| Breakfast | 08:15 | 15 minutes |

These activities overlap.

PawPal+ detects the conflict and can display the following Streamlit warning:

```text
Conflict: Buddy's Morning Walk overlaps with Buddy's Breakfast
```

The warning helps the owner identify overlapping responsibilities and manually adjust the schedule.

The system detects conflicts between incomplete tasks that share the same due date.

### 7. Generate a Daily Schedule

Click **Generate schedule**.

PawPal+ uses `generate_plan()` to select incomplete tasks according to priority and available time.

For an owner with 60 available minutes, the system can select:

- Morning Walk: 30 minutes
- Breakfast: 15 minutes

The remaining 15 minutes are insufficient for the 25-minute grooming task.

The schedule therefore contains two tasks totaling 45 minutes.

### 8. Complete Recurring Tasks

In the app, choose a task under **Complete a Task** and click **Mark Task Complete**. The task's status changes to Completed in the table.

This calls `Task.mark_complete()`. Tasks created in the UI are daily, so completing one creates a new pending occurrence for the following day.

The backend also supports weekly tasks, where the next occurrence is scheduled seven days later. The UI does not yet offer a way to choose weekly recurrence.

The system also prevents repeated completion of the same task from generating duplicate occurrences.

### 9. Sample CLI Output

The following sample output was generated using:

```bash
python main.py
```

```text
=== Today's Schedule ===
Buddy: Walk - 30 minutes (High priority)
Luna: Feed - 15 minutes (High priority)

Total scheduled tasks: 2
Total scheduled time: 45 minutes
```

The owner has 60 minutes available. The scheduler selects high-priority tasks from both pets.

A lower-priority grooming task requiring 25 minutes is skipped because only 15 minutes remain.

This example demonstrates multi-pet scheduling, priority sorting, and time-budget constraints.

## 🧪 Testing PawPal+

PawPal+ uses pytest to verify its core functionality, scheduling algorithms, and edge cases.

### Running the Tests

Run all automated tests:

```bash
python -m pytest
```

Run the PawPal+ test file with detailed output:

```bash
python -m pytest tests/test_pawpal.py -v
```

Generate a coverage report:

```bash
python -m pytest tests/test_pawpal.py -v --cov=pawpal_system --cov-report=term-missing
```

### Test Coverage

The automated test suite verifies nine important behaviors:

| Test | Description | Result |
|---|---|---|
| Task completion | Confirms that tasks can be marked complete. | PASSED |
| Task addition | Verifies that tasks are added to a pet. | PASSED |
| Multi-pet scheduling | Checks scheduling across multiple pets within available time. | PASSED |
| Recurring tasks | Verifies recurrence and prevents duplicate generation. | PASSED |
| Conflict detection | Identifies overlapping tasks. | PASSED |
| Sorting correctness | Verifies chronological task ordering. | PASSED |
| Identical start times | Detects tasks scheduled at the same time. | PASSED |
| Filtering edge cases | Returns an empty list when no tasks match. | PASSED |
| Zero available time | Returns an empty schedule when no time is available. | PASSED |

### Successful Test Output

```text
collected 9 items

tests/test_pawpal.py::test_task_completion PASSED
tests/test_pawpal.py::test_task_addition PASSED
tests/test_pawpal.py::test_multi_pet_scheduler PASSED
tests/test_pawpal.py::test_recurring_tasks PASSED
tests/test_pawpal.py::test_conflict_detection PASSED
tests/test_pawpal.py::test_sort_tasks_by_time PASSED
tests/test_pawpal.py::test_conflict_same_start_time PASSED
tests/test_pawpal.py::test_filter_no_matching_tasks PASSED
tests/test_pawpal.py::test_zero_available_time PASSED

9 passed in 0.18s
```

All nine tests passed during Phase 5.

### Code Coverage

The Phase 4 test suite achieved 93% statement coverage.

Additional tests were added during Phase 5. The updated coverage percentage should be measured using pytest-cov before final submission.

### Confidence Level: ★★★★☆ (4/5)

I am confident that PawPal+ handles its core pet management and scheduling functions correctly.

All nine automated tests passed, including tests for sorting, recurrence, overlapping schedules, filtering, and zero available time.

I rated the system four out of five stars because additional testing is still needed for invalid inputs, tasks crossing midnight, complex scheduling conflicts, and data persistence.

## Algorithm Design and Tradeoffs

I selected straightforward algorithms that are easy to understand, test, and maintain.

**Sorting:** Python's built-in `sorted()` function organizes tasks by priority or start time. Its typical time complexity is O(n log n).

**Filtering:** List comprehensions select tasks based on pet name or completion status. Filtering has O(n) time complexity.

**Recurrence:** Python's `datetime.timedelta` calculates the next due date for daily or weekly tasks.

**Conflict detection:** The scheduler compares pairs of incomplete tasks to identify overlapping time intervals on the same date. This approach has O(n²) time complexity.

**Daily schedule generation:** The scheduler processes priority-sorted tasks and includes those that fit within the remaining time budget.

These approaches are appropriate for a small pet-care application, where readability and correctness are more important than advanced optimization.

## Limitations and Future Improvements

PawPal+ could be improved by adding:

- Persistent storage so pets and tasks remain available after restarting the application.
- Validation for invalid task durations and time formats.
- Better handling of tasks spanning midnight.
- Date-aware scheduling and conflict-free plan generation.
- More advanced support for owner preferences.
- Improved task editing and rescheduling controls.
- Additional Streamlit integration tests.
- More efficient conflict detection for large task collections.

## Project Reflection

The project reflection is documented in:

`reflection.md`

It discusses system design, scheduling tradeoffs, automated testing, AI-assisted development, and lessons learned from acting as the lead architect.

## Project Files

```text
app.py
main.py
pawpal_system.py
README.md
reflection.md
requirements.txt
diagrams/
    uml_final.mmd
tests/
    test_pawpal.py
```

PawPal+ demonstrates how Python object-oriented design, scheduling algorithms, testing, and Streamlit can be combined into a practical pet-care planning application.