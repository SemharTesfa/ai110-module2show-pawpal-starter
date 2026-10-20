# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

1. Manage pets: The user should be able to enter basic owner and pet information, including the pet's name, species, and age.

2. Manage care tasks: The user should be able to add and edit daily pet care tasks, such as feeding, walking, medication, and grooming. Each task should include a duration and priority.

3. Generate a daily schedule: The system should organize tasks based on priority, available time, and owner preferences. It should generate a daily plan and explain why certain tasks were selected.

My initial UML design includes four classes:

Owner: Stores the owner's name, available time, and list of pets. It also includes a method to add pets.

Pet: Stores each pet's name, species, and age. It includes a method to display pet information.

Task: Represents a pet care activity, including its title, duration, priority, and associated pet.

PawPalSystem: Manages care tasks, sorts tasks by priority, and generates a daily schedule.

The classes use association relationships rather than inheritance. An owner has pets, pets have care tasks, and PawPalSystem manages those tasks. Each class has a separate responsibility, making the design easier to understand and maintain.

**b. Design changes**

During the design review, I identified two improvements. First, I decided to add a preferences attribute to the Owner class so the system can consider the owner's preferences when generating a daily schedule. Second, I added a pet reference to the Task class to connect each care task to a specific pet.

These changes help organize the information and make the scheduler more flexible. I also reviewed the UML relationships to make sure they matched the Python class design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler currently considers two main constraints: task priority and the owner's available time. High-priority tasks are considered first, followed by medium- and low-priority tasks. The scheduler also excludes completed tasks.

I prioritized these constraints because important pet care activities should be scheduled first without exceeding the owner's available time. Owner preferences are stored in the design but are not yet used in the scheduling algorithm.

**b. Tradeoffs**

One tradeoff is that the scheduler may skip a lower-priority task if it does not fit within the remaining available time.

For example, if the owner has 60 minutes available, the scheduler may select a 30-minute walk and a 15-minute feeding task but skip a 25-minute grooming task.

This is reasonable because it prioritizes important tasks while respecting the time limit. However, the current greedy algorithm does not always maximize the number of tasks completed or total time used.

---

## 3. AI Collaboration

**a. How you used AI**
I used ChatGPT to help design my UML diagram, implement Python classes, and debug errors. AI helped me understand class relationships, implement task management methods, and build a scheduler that retrieves tasks from multiple pets.

I also used AI to create pytest tests and understand code coverage. Step-by-step explanations and debugging questions were especially helpful.

b. Judgment and verification

During implementation, I encountered a TypeError because my original PawPalSystem constructor did not accept an Owner argument. Instead of assuming the suggested code was working, I compared it with my existing implementation and corrected the constructor.

I verified the changes by running the CLI demonstration and testing the scheduler with two pets. I also ran three automated tests using pytest. All three passed, and the code achieved 96% statement coverage.

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

---

## 4. Testing and Verification

**a. What you tested**

I created three automated tests using pytest:

Task Completion: Verified that mark_complete() changes a task's completed status from False to True.

Task Addition: Verified that adding a task to a pet increases the pet's task count.

Multi-Pet Scheduling: Verified that the scheduler retrieves tasks from multiple pets and generates a schedule within the owner's available time.

These tests were important because they checked the main functionality of my backend system.

All three tests passed, and the tests achieved 96% code coverage.

**b. Confidence**

I am confident that the basic task management and scheduling functions work for the scenarios I tested.

However, I would like to add more tests for edge cases, including zero available time, empty task lists, invalid task durations, and tasks with equal priorities. I would also test how the scheduler handles owner preferences and recurring tasks once those features are implemented.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
