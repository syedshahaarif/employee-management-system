import mysql.connector
import streamlit as st

from ems.auth import require_login
from ems.views import analytics, attendance, dashboard, departments, employees

st.set_page_config(page_title="Employee Management System", layout="wide")

PAGES = {
    "Dashboard": dashboard.render,
    "Add Employee": employees.render_add,
    "View Employees": employees.render_view,
    "Update Employee": employees.render_update,
    "Delete Employee": employees.render_delete,
    "Attendance": attendance.render,
    "Departments": departments.render,
    "SQL Analytics": analytics.render,
}


def main():
    if not require_login():
        return
    st.title("Employee Management System")
    page = st.sidebar.radio("Menu", list(PAGES.keys()))
    try:
        PAGES[page]()
    except mysql.connector.Error as e:
        st.error(
            f"Database error: {e}. Check your .env settings and that MySQL is running."
        )


main()
