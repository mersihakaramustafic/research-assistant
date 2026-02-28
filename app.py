import streamlit as st
import os
from agent.planner import generate_plan
from agent.executor import execute_plan, synthesize_report
from storage.persistence import save_plan, load_plan, plan_exists
from infrastructure.logging_config import setup_logging

from dotenv import load_dotenv
load_dotenv()

setup_logging()

st.set_page_config(page_title="Market Research Agent", layout="wide")

st.title("AI Market Research Agent")

# --- Sidebar ---
st.sidebar.header("Session Control")

if plan_exists():
    if st.sidebar.button("Resume Existing Plan"):
        st.session_state.plan = load_plan()
        st.success("Loaded existing plan.")

if st.sidebar.button("Reset Plan"):
    if os.path.exists("data/plan.json"):
        os.remove("data/plan.json")
    st.session_state.plan = None
    st.success("Plan reset.")

# --- Goal Input ---
goal = st.text_input("Enter your research goal:")

if st.button("Generate Plan"):
    if goal:
        plan = generate_plan(goal)
        save_plan(plan)
        st.session_state.plan = plan
        st.success("Plan generated and saved.")
    else:
        st.warning("Please enter a goal.")

# --- Display Plan ---
if "plan" in st.session_state and st.session_state.plan:

    plan = st.session_state.plan

    st.subheader("Tasks")

    for task in plan.tasks:
        status_color = "🟢" if task.status == "completed" else "🟡"
        st.markdown(f"{status_color} **Task {task.id}**: {task.description}")
        if task.result:
            with st.expander("View Result"):
                st.write(task.result)

    if st.button("Execute Remaining Tasks"):
        plan = execute_plan(plan)
        save_plan(plan)
        st.session_state.plan = plan
        st.success("Execution completed.")

    if all(t.status == "completed" for t in plan.tasks):
        if st.button("Generate Final Report"):
            report = synthesize_report(plan)
            st.subheader("Final Report")
            st.write(report)