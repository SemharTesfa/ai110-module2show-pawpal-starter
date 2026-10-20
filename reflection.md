PawPal+ Project Reflection

1. System Design

a. Initial design

My PawPal+ project focuses on three main requirements:

Manage pets: Allow users to enter owner and pet information, including the pet's name, species, and age.

Manage care tasks: Allow users to add pet care tasks such as feeding, walking, medication, and grooming, with duration and priority.

Generate a daily schedule: Organize tasks based on priority and available time, with support for owner preferences as a future improvement.

My initial UML design includes four classes:

Owner: Stores the owner's name, available time, preferences, and pets.

Pet: Stores each pet's name, species, age, and care tasks.

Task: Represents a care activity, including its title, duration, priority, and associated pet.

PawPalSystem: Manages tasks, sorts them by priority, and generates daily schedules.

The classes use association relationships rather than inheritance. An owner has pets, pets have tasks, and PawPalSystem manages scheduling. Each class has a separate responsibility, making the system easier to understand and maintain.

b. Design changes

During the design review, I identified two improvements. First, I added a preferences attribute to the Owner class to support future preference-based scheduling. Second, I added a pet reference to the Task class to connect each care task to a specific pet.

During implementation, I also added a task list to each Pet and a get_all_tasks() method to Owner. This allows the scheduler to collect tasks from multiple pets.

In Phase 4, I expanded the Task class with scheduled time and due-date attributes to support time sorting, recurring tasks, and conflict detection.

2. Scheduling Logic and Tradeoffs

a. Constraints and priorities

My scheduler considers task priority, available time, and completion status. High-priority tasks are considered first, followed by medium- and low-priority tasks. Completed tasks are excluded from the daily schedule.

I prioritized these constraints because important pet care activities should be scheduled first without exceeding the owner's available time.

I also implemented additional algorithms to sort tasks by scheduled time, filter tasks by pet or completion status, create daily and weekly recurring tasks, and detect overlapping tasks.

Owner preferences are stored but are not yet used in the scheduling algorithm.

b. Tradeoffs

One tradeoff is that my scheduler uses a greedy approach, selecting higher-priority tasks first when they fit within the available time.

For example, with 60 available minutes, the scheduler may select a 30-minute walk and a 15-minute feeding task while skipping a 25-minute grooming task.

This approach is simple and prioritizes important care activities, but it does not always maximize the number of tasks completed or the total time used.

Another tradeoff involves my filtering algorithm. I compared two implementations: one using separate filtering steps and another combining the conditions into a single list comprehension. Although the combined version was shorter and avoided an intermediate list, I kept the original version because it was easier to read, understand, and maintain. Both approaches have O(n) time complexity.

For conflict detection, I chose to compare task start and end times and return warning messages. This makes conflicts visible without crashing the application. However, the current implementation assumes tasks do not extend past midnight.

3. AI Collaboration

a. How you used AI

I used ChatGPT to help design my UML diagram, implement Python classes, and debug errors. AI helped me understand class relationships, implement task management methods, and build a scheduler that retrieves tasks from multiple pets.

I also used AI to connect my Python backend to Streamlit using st.session_state, create automated tests, and understand code coverage.

During Phase 4, I used AI to develop sorting, filtering, recurring-task, and conflict-detection algorithms.

Step-by-step explanations, debugging questions, and comparisons between different implementations were especially helpful.

b. Judgment and verification

During implementation, I encountered a TypeError because my original PawPalSystem constructor did not accept an Owner argument. Instead of assuming the suggested code was correct, I compared it with my existing implementation and corrected the constructor.

I also encountered an AttributeError when testing filter_tasks(). I reviewed the class structure, added the missing method, and reran my demonstration.

When evaluating the filtering algorithm, I decided to keep the more readable implementation rather than replacing it with a shorter version.

I verified changes by running my CLI demonstration, testing the Streamlit interface, and executing automated pytest tests.

4. Testing and Verification

a. What you tested

I initially created three automated tests:

Task Completion: Verified that mark_complete() changes a task's completion status.

Task Addition: Verified that adding a task to a pet updates the pet's task list.

Multi-Pet Scheduling: Verified that the scheduler retrieves tasks from multiple pets and respects the owner's available time.

These initial tests passed and achieved 96% statement coverage at that stage.

During Phase 4, I added tests for:

Recurring Tasks: Checking that daily tasks create a new occurrence one day later, weekly tasks create one seven days later, and completing the same task twice does not create duplicates.

Conflict Detection: Checking that overlapping tasks generate a warning while non-overlapping tasks do not.

I also used main.py to demonstrate chronological sorting, filtering by pet and completion status, and conflict detection.

b. Confidence

I am confident in the basic scheduling, filtering, and recurrence behavior for the scenarios I tested.

However, I would like to test additional edge cases, including empty task lists, invalid time formats, tasks with equal priorities, overlapping tasks across midnight, and recurring tasks at month or year boundaries.

I would also improve how the scheduler handles owner preferences and tasks that have already passed their due dates.

5. Reflection

a. What went well

I am most satisfied with successfully connecting my Python backend to the Streamlit interface. I can add pets, assign tasks, and generate schedules through the browser.

I also improved my understanding of object-oriented programming by using separate classes with clear responsibilities.

Implementing sorting, filtering, recurrence, and conflict detection helped me see how small algorithms can make an application more useful.

b. What you would improve

If I had another iteration, I would improve the scheduling algorithm to consider owner preferences, due dates, and overlapping tasks when generating the final schedule.

I would also add stronger input validation, improve the Streamlit interface, and provide controls for marking tasks complete and viewing upcoming recurring tasks.

Another improvement would be saving data to a file or database so pets and tasks remain available after the Streamlit session ends.

c. Key takeaway

One important lesson I learned is that good software design involves more than writing code that works. Separating responsibilities between classes, testing behavior, and evaluating algorithmic tradeoffs makes the system easier to maintain and extend.

I also learned that AI is most useful when I review its suggestions, understand the reasoning, and verify the results through testing rather than accepting generated code without checking it.