import streamlit as st
from datetime import datetime, timedelta, time

# Function to initialize session state
def init_session_state():
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

# Function to add a new task
def add_task(task, due_date, due_time):
    st.session_state.tasks.append({"task": task, "due_date": due_date, "due_time": due_time, "completed": False})

# Function to display the task list
def display_tasks():
    tasks = st.session_state.tasks
    if not tasks:
        st.write("No tasks added yet.")
    else:
        st.write("### Tasks:")
        for idx, task in enumerate(tasks, start=1):
            task_status = "Completed" if task["completed"] else "Not Completed"
            due_time_display = task["due_time"].strftime("%I:%M %p")
            if task["completed"]:
                st.markdown(f"{idx}. <span style='color:green; font-weight: bold;'>✔</span> Task: {task['task']}, Due Date: {task['due_date']}, Due Time: {due_time_display}, Status: {task_status}", unsafe_allow_html=True)
            else:
                st.write(f"{idx}. {task['task']}, Due Date: {task['due_date']}, Due Time: {due_time_display}, Status: {task_status}")

# Main function to handle the app logic
def main():
    st.title("Productivity App")
    init_session_state()

    # Sidebar menu
    st.sidebar.title("Menu")

    st.sidebar.markdown("---")
    st.sidebar.header("Menu Options")

    if st.sidebar.button("Add Task", key="add_task"):
        st.header("Add a New Task")
        task = st.text_input("Task description")
        due_date = st.date_input("Due Date", datetime.now() + timedelta(days=1))

        st.write("Due Time:")
        with st.expander("Custom Time"):
            hour = st.number_input("Hour", 1, 12)
            minute = st.number_input("Minute", 0, 59)
            am_pm = st.radio("AM/PM", ("AM", "PM"))
            due_time = time(hour, minute)
            if am_pm == "PM":
                due_time = due_time.replace(hour=(due_time.hour + 12) % 24)
        
        if st.button("Add Task", key="add_task_button"):
            add_task(task, due_date, due_time)
            st.success("Task added successfully!")

    if st.sidebar.button("View Tasks", key="view_tasks"):
        st.header("View Tasks")
        display_tasks()
        # Get the task numbers for the dropdown, excluding completed tasks
        task_numbers = [i+1 for i, task in enumerate(st.session_state.tasks) if not task["completed"]]
        task_dropdown = st.selectbox("Select Task Number:", task_numbers)
        if st.button("Mark as Completed", key="mark_completed"):
            # Get the selected task index and mark it as completed
            task_idx = task_dropdown - 1
            st.session_state.tasks[task_idx]["completed"] = True
            st.experimental_rerun()  # Trigger a rerun to update the task status

if __name__ == "__main__":
    main()
