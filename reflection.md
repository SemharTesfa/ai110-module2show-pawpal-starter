# PawPal+ Project Reflection

## 1. System Design

### a. Initial Design

My PawPal+ project focuses on three main requirements:

1. **Manage pets:** Allow users to enter owner and pet information, including the pet's name, species, and age.
2. **Manage care tasks:** Allow users to add pet care tasks such as feeding, walking, medication, and grooming, with duration and priority.
3. **Generate a daily schedule:** Organize tasks based on priority and available time, with support for owner preferences as a future improvement.

My initial UML design included four classes:

- **Owner:** Stores the owner's name, available time, preferences, and pets.
- **Pet:** Stores each pet's name, species, age, and care tasks.
- **Task:** Represents a care activity, including its title, duration, priority, and associated pet.
- **PawPalSystem:** Manages tasks, sorts them by priority, and generates daily schedules.

The classes use association relationships rather than inheritance. An owner has pets, pets have tasks, and `PawPalSystem` manages scheduling.

Each class has a separate responsibility, making the system easier to understand, test, and maintain.

### b. Design Changes

During the design review, I identified two improvements.

First, I added a `preferences` attribute to the `Owner` class to support future preference-based scheduling.

Second, I added a pet reference to the `Task` class to connect each care task to a specific pet.

During implementation, I also added a task list to each `Pet` and a `get_all_tasks()` method to `Owner`. This allows the scheduler to collect tasks from multiple pets.

In Phase 4, I expanded the `Task` class with scheduled time, due date, frequency, and completion status.

I also expanded `PawPalSystem` to support chronological sorting, task filtering, and scheduling conflict detection.

These changes improved the functionality while preserving the original four-class architecture.

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and Priorities

My scheduler considers task priority, available time, and completion status.

High-priority tasks are considered first, followed by medium- and low-priority tasks. Completed tasks are excluded from the daily schedule.

I prioritized these constraints because important pet-care activities should be scheduled first without exceeding the owner's available time.

I also implemented additional algorithms to:

- Sort tasks by scheduled time.
- Filter tasks by pet or completion status.
- Create daily and weekly recurring tasks.
- Detect overlapping tasks scheduled for the same date.

Owner preferences are stored but are not yet used in the scheduling algorithm.

### b. Tradeoffs

One tradeoff is that my scheduler uses a greedy approach, selecting higher-priority tasks first when they fit within the available time.

For example, with 60 available minutes, the scheduler may select a 30-minute walk and a 15-minute feeding task while skipping a 25-minute grooming task.

This approach is simple and prioritizes important care activities, but it does not always maximize the number of tasks completed or the total available time used.

Another tradeoff involves filtering. I compared two implementations: one using separate filtering steps and another combining conditions into a single list comprehension.

Although the combined implementation was shorter, I initially preferred the separate filtering steps because they were easier for me to read and debug. Both approaches have O(n) time complexity.

For conflict detection, I chose to compare task start and end times and return warning messages.

This makes conflicts visible without crashing the application. However, the current implementation assumes tasks do not extend past midnight and does not automatically resolve conflicts.

## 3. AI Collaboration and Strategy

### a. How I Used AI

I used ChatGPT as an AI coding assistant throughout the PawPal+ development process.

AI helped me:

- Design and revise my UML class diagram.
- Understand relationships between the `Owner`, `Pet`, `Task`, and `PawPalSystem` classes.
- Implement Python classes and methods.
- Debug errors involving constructors and missing methods.
- Connect backend functionality to Streamlit.
- Implement sorting, filtering, recurrence, and conflict detection.
- Write automated tests using pytest.
- Understand code coverage and algorithmic tradeoffs.
- Improve project documentation.

The most effective AI assistance involved step-by-step explanations, debugging support, and comparisons between different implementations.

For example, when I encountered errors, I could share the relevant code and error message, ask for an explanation, and make a targeted correction instead of rewriting the entire application.

This approach helped me understand why changes were necessary.

### b. AI Suggestions I Rejected or Modified

One important example involved the task-filtering algorithm.

AI presented a shorter implementation that combined filtering conditions into one list comprehension.

Although that approach was valid, I preferred the version with separate filtering steps because it was easier for me to understand, debug, and maintain.

I therefore chose readability over reducing the number of lines of code.

Another example occurred when I encountered a `TypeError` because my original `PawPalSystem` constructor did not accept an `Owner` argument.

Rather than assuming the suggested code matched my existing architecture, I reviewed my class definition and updated the constructor to work with the owner-based design.

These experiences taught me that AI-generated suggestions must be evaluated against the actual project requirements and existing code.

### c. Using Separate Chat Sessions for Different Phases

Organizing AI-assisted development by project phase helped me focus on specific engineering problems.

During the design phase, I concentrated on requirements, UML diagrams, and class responsibilities.

During implementation, I focused on Python methods and connecting the classes.

During the scheduling phase, I worked on sorting, filtering, recurrence, and conflict detection.

During testing, I concentrated on pytest, edge cases, and code coverage.

Finally, during the packaging phase, I focused on the Streamlit interface, final UML diagram, README, and reflection.

Separating these discussions made it easier to ask focused questions and review changes incrementally.

However, I also learned that AI suggestions from different conversations must be checked against the latest project files because the implementation may have changed between phases.

### d. My Role as the Lead Architect

The most important lesson from using AI is that the developer must remain responsible for the system design.

AI can suggest algorithms, generate code, explain errors, and identify possible improvements, but it does not automatically know whether a suggestion fits the existing architecture.

As the lead architect, my responsibilities included:

- Defining the requirements.
- Deciding how classes should interact.
- Evaluating suggested implementations.
- Choosing between alternative algorithms.
- Testing whether changes worked.
- Keeping the UML diagram consistent with the Python code.
- Ensuring the documentation accurately describes the project.

I learned that successful AI-assisted engineering requires understanding and verifying the code rather than simply copying generated solutions.

## 4. Testing and Verification

### a. What I Tested

I initially created three automated tests:

1. **Task Completion:** Verified that `mark_complete()` changes a task's completion status.
2. **Task Addition:** Verified that adding a task to a pet updates the pet's task list.
3. **Multi-Pet Scheduling:** Verified that the scheduler retrieves tasks from multiple pets and respects the owner's available time.

These initial tests passed and achieved 96% statement coverage at that stage.

During Phase 4, I added tests for recurring tasks and scheduling conflict detection.

I also used `main.py` to demonstrate chronological sorting, filtering, and conflict detection.

By Phase 5, the automated test suite included nine tests:

| Test | Purpose |
|---|---|
| Task completion | Verify that tasks can be marked complete. |
| Task addition | Verify that tasks are added to a pet. |
| Multi-pet scheduling | Verify scheduling across multiple pets. |
| Recurring tasks | Verify daily and weekly recurrence and prevent duplicates. |
| Conflict detection | Detect overlapping tasks. |
| Sorting by time | Verify chronological task ordering. |
| Identical start times | Detect conflicts between tasks starting at the same time. |
| Filtering edge cases | Verify behavior when no tasks match the filter. |
| Zero available time | Verify that no tasks are scheduled when the time budget is zero. |

I ran:

```bash
python -m pytest tests/test_pawpal.py -v
```

The results were:

```text
9 passed in 0.18s
```

All nine tests passed.

The Phase 4 suite achieved 93% statement coverage. Because additional tests were added afterward, the current coverage percentage should be measured again before submission.

### b. Confidence

I rate my confidence in PawPal+ as **4 out of 5 stars**.

I am confident in the core scheduling, filtering, conflict detection, and recurrence behavior for the scenarios tested.

However, I would like to test additional edge cases, including:

- Empty task lists.
- Invalid time formats.
- Tasks with equal priorities.
- Tasks crossing midnight.
- Recurring tasks at month or year boundaries.
- Tasks with different due dates.
- Streamlit user interactions.

I would also improve how the scheduler handles owner preferences, overdue tasks, and conflicting activities when generating the final schedule.

## 5. Final Reflection

### a. What Went Well

I am most satisfied with connecting my Python backend to the Streamlit interface.

I can add pets, assign tasks, and generate schedules through the browser.

I also improved my understanding of object-oriented programming by using separate classes with clear responsibilities.

Implementing sorting, filtering, recurrence, and conflict detection helped me understand how algorithms can make an application more useful.

Automated testing also gave me greater confidence when making changes.

### b. What I Would Improve

If I had another iteration, I would improve the scheduling algorithm to consider owner preferences, due dates, and overlapping tasks when generating the final schedule.

I would also add stronger input validation, improve the Streamlit interface, and provide more complete controls for marking tasks complete and viewing upcoming recurring tasks.

Another important improvement would be saving data to a file or database so pets and tasks remain available after the application restarts.

I would also add more integration tests to verify that the Streamlit interface correctly uses the backend algorithms.

### c. Key Takeaway

One important lesson I learned is that good software design involves more than writing code that works.

Separating responsibilities between classes, testing behavior, and evaluating algorithmic tradeoffs makes a system easier to maintain and extend.

I also learned that AI is most effective when used as a collaborator rather than as a replacement for engineering judgment.

By reviewing suggestions, comparing alternatives, testing results, and making final design decisions myself, I developed a better understanding of what it means to be the lead architect of an AI-assisted software project.