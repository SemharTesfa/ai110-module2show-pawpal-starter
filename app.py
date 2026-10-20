import streamlit as st
from pawpal_system import Owner, Pet, Task, PawPalSystem



st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", 60)

st.write("Current owner:", st.session_state.owner.name)
st.write("Available time:", st.session_state.owner.available_minutes, "minutes")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input(
    "Owner name",
    value=st.session_state.owner.name
)

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    new_pet = Pet(pet_name, species, pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added successfully!")

st.subheader("My Pets")

if st.session_state.owner.pets:
    for pet in st.session_state.owner.pets:
        st.write(f"🐾 {pet.name} - {pet.species}, {pet.age} years old")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")

st.markdown("### Tasks")
st.caption("Add care tasks for your pets.")

if st.session_state.owner.pets:
    selected_pet_index = st.selectbox(
        "Select pet",
        range(len(st.session_state.owner.pets)),
        format_func=lambda i: st.session_state.owner.pets[i].name
    )

    selected_pet = st.session_state.owner.pets[selected_pet_index]

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input("Task title", value="Morning walk")

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

    if st.button("Add task"):
        new_task = Task(
            task_title,
            int(duration),
            priority,
            selected_pet
        )

        selected_pet.add_task(new_task)
        st.success(f"{task_title} added for {selected_pet.name}!")

    st.markdown("#### Current Tasks")

    all_tasks = st.session_state.owner.get_all_tasks()

    if all_tasks:
        st.table([
            {
                "Pet": task.pet.name,
                "Task": task.title,
                "Duration": task.duration,
                "Priority": task.priority
            }
            for task in all_tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")

else:
    st.info("Please add a pet before adding tasks.")


st.divider()

st.subheader("Build Schedule")

st.caption("Generate a daily care plan based on priority and available time.")

if st.button("Generate schedule"):
    system = PawPalSystem(st.session_state.owner)
    schedule = system.generate_plan()

    if schedule:
        st.success("Daily schedule generated!")

        for task in schedule:
            st.write(
                f"🐾 {task.pet.name}: {task.title} "
                f"- {task.duration} minutes "
                f"({task.priority} priority)"
            )

        total_time = sum(task.duration for task in schedule)

        st.write(f"Total scheduled tasks: {len(schedule)}")
        st.write(f"Total scheduled time: {total_time} minutes")

    else:
        st.warning("No tasks available within the time limit.")

    
