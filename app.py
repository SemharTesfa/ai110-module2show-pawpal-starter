
import streamlit as st
from pawpal_system import Owner, Pet, Task, PawPalSystem


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", 60)

system = PawPalSystem(st.session_state.owner)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🐾 PawPal+")

st.markdown(
    """
    Welcome to PawPal+!

    Manage your pets, organize care tasks, and generate
    daily schedules based on priority and available time.

    PawPal+ also supports task filtering, conflict detection,
    and recurring care activities.
    """
)

st.write("Current owner:", st.session_state.owner.name)
st.write(
    "Available time:",
    st.session_state.owner.available_minutes,
    "minutes"
)

st.divider()


# --------------------------------------------------
# Owner Information
# --------------------------------------------------

st.subheader("Owner Information")

owner_name = st.text_input(
    "Owner name",
    value=st.session_state.owner.name
)

available_time = st.number_input(
    "Available time (minutes)",
    min_value=0,
    max_value=1440,
    value=st.session_state.owner.available_minutes
)

if st.button("Update Owner"):
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_minutes = int(available_time)

    st.success("Owner information updated!")
    st.rerun()


st.divider()


# --------------------------------------------------
# Add Pet
# --------------------------------------------------

st.subheader("Add a Pet")

pet_name = st.text_input(
    "Pet name",
    value="Mochi"
)

species = st.selectbox(
    "Species",
    ["dog", "cat", "other"]
)

pet_age = st.number_input(
    "Pet age",
    min_value=0,
    max_value=30,
    value=2
)

if st.button("Add Pet"):
    if not pet_name.strip():
        st.warning("Please enter a pet name.")
    else:
        new_pet = Pet(
            name=pet_name.strip(),
            species=species,
            age=int(pet_age)
        )

        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} added successfully!")


# --------------------------------------------------
# Display Pets
# --------------------------------------------------

st.subheader("My Pets")

if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(
            f"🐾 {pet.name} - "
            f"{pet.species}, {pet.age} years old"
        )
else:
    st.info("No pets added yet.")


st.divider()


# --------------------------------------------------
# Task Management
# --------------------------------------------------

st.subheader("Task Management")
st.caption("Add and manage care tasks for your pets.")

if st.session_state.owner.pets:

    selected_pet_index = st.selectbox(
        "Select pet",
        range(len(st.session_state.owner.pets)),
        format_func=lambda i: st.session_state.owner.pets[i].name
    )

    selected_pet = st.session_state.owner.pets[selected_pet_index]

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input(
            "Task title",
            value="Morning walk"
        )

    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20
        )

    with col3:
        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

    task_date = st.date_input("Due Date")

    task_time = st.time_input("Scheduled Time")

    frequency = st.selectbox(
        "Frequency",
        ["Once", "Daily", "Weekly"]
    )

    if st.button("Add Task"):

        if not task_title.strip():
            st.warning("Please enter a task title.")

        else:
            new_task = Task(
                title=task_title.strip(),
                duration=int(duration),
                priority=priority,
                pet=selected_pet,
                frequency=frequency,
                time=task_time.strftime("%H:%M"),
                due_date=task_date.isoformat()
            )

            system.add_task(new_task)

            st.success(
                f"{task_title} added for {selected_pet.name}!"
            )

    st.divider()


    # --------------------------------------------------
    # Mark Task Complete
    # --------------------------------------------------

    st.subheader("Complete a Task")

    pending_tasks = [
        task
        for task in st.session_state.owner.get_all_tasks()
        if not task.completed
    ]

    if pending_tasks:

        selected_task_index = st.selectbox(
            "Select task to complete",
            range(len(pending_tasks)),
            format_func=lambda i: (
                f"{pending_tasks[i].pet.name} - "
                f"{pending_tasks[i].title} "
                f"({pending_tasks[i].due_date} "
                f"{pending_tasks[i].time})"
            )
        )

        if st.button("Mark Task Complete"):

            selected_task = pending_tasks[selected_task_index]

            next_task = selected_task.mark_complete()

            if next_task:
                st.session_state.completion_message = (
                    f"{selected_task.title} completed! "
                    f"Next occurrence: {next_task.due_date}"
                )
            else:
                st.session_state.completion_message = (
                    f"{selected_task.title} marked as completed!"
                )

            st.rerun()

    else:
        st.info("No incomplete tasks.")

    if "completion_message" in st.session_state:
        st.success(st.session_state.completion_message)
        del st.session_state.completion_message


    st.divider()


    # --------------------------------------------------
    # Filter and Sort Tasks
    # --------------------------------------------------

    st.subheader("Current Tasks")

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        pet_filter = st.selectbox(
            "Filter by pet",
            ["All pets"] + [
                pet.name
                for pet in st.session_state.owner.pets
            ]
        )

    with filter_col2:
        status_filter = st.selectbox(
            "Filter by status",
            [
                "All tasks",
                "Incomplete Tasks",
                "Completed Tasks"
            ]
        )

    status_options = {
        "All tasks": None,
        "Incomplete Tasks": False,
        "Completed Tasks": True
    }

    filtered_tasks = system.filter_tasks(
        pet_name=(
            None if pet_filter == "All pets"
            else pet_filter
        ),
        completed=status_options[status_filter]
    )

    all_tasks = sorted(
        filtered_tasks,
        key=lambda task: (task.due_date, task.time)
    )

    if all_tasks:

        st.table([
            {
                "Pet": task.pet.name,
                "Task": task.title,
                "Date": task.due_date,
                "Time": task.time,
                "Duration": task.duration,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": (
                    "Completed"
                    if task.completed
                    else "Pending"
                )
            }
            for task in all_tasks
        ])

    else:
        st.info("No tasks match the selected filters.")

else:
    st.info("Please add a pet before adding tasks.")


st.divider()


# --------------------------------------------------
# Scheduling Conflict Detection
# --------------------------------------------------

st.subheader("⚠️ Scheduling Conflicts")

conflicts = system.find_conflicts()

if conflicts:

    for conflict in conflicts:
        st.warning(conflict)

    st.info(
        "Please review overlapping tasks and adjust "
        "their scheduled times."
    )

else:
    st.success("No scheduling conflicts detected!")


st.divider()


# --------------------------------------------------
# Generate Daily Schedule
# --------------------------------------------------

st.subheader("Build Schedule")

st.caption(
    "Generate a care plan based on priority "
    "and available time."
)

if st.button("Generate Schedule"):

    schedule = system.generate_plan()

    if schedule:

        st.success("Schedule generated successfully!")

        schedule_table = [
            {
                "Pet": task.pet.name,
                "Task": task.title,
                "Date": task.due_date,
                "Time": task.time,
                "Duration": task.duration,
                "Priority": task.priority
            }
            for task in schedule
        ]

        st.table(schedule_table)

        total_time = sum(
            task.duration
            for task in schedule
        )

        st.write(
            f"Total scheduled tasks: {len(schedule)}"
        )

        st.write(
            f"Total scheduled time: {total_time} minutes"
        )

        st.write(
            "Remaining available time:",
            st.session_state.owner.available_minutes - total_time,
            "minutes"
        )

        st.caption(
            "Tasks are selected by priority and available time. "
            "The plan does not automatically resolve scheduling "
            "conflicts or restrict tasks to today's due date."
        )

    else:
        st.warning(
            "No incomplete tasks fit within the available time."
        )
