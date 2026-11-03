from datetime import date

import mysql.connector
import pandas as pd
import streamlit as st

from ems.db import get_departments, get_employees, run_query
from ems.utils import validate_employee


def render_add():
    st.header("Add Employee")
    depts = get_departments()
    if not depts:
        st.warning("Please add a department first.")
        return
    dept_map = {d["dept_name"]: d["dept_id"] for d in depts}
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (10 digits)")
        designation = st.text_input("Designation")
        salary = st.number_input("Salary", min_value=0.0, step=1000.0)
        hire_date = st.date_input("Hire Date", value=date.today())
        dept = st.selectbox("Department", list(dept_map.keys()))
        submit = st.form_submit_button("Add Employee")
    if submit:
        errors = validate_employee(name, email, phone, salary)
        if errors:
            for e in errors:
                st.error(e)
            return
        try:
            run_query(
                """INSERT INTO employees
                   (name, email, phone, designation, salary, hire_date, dept_id)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (name.strip(), email.strip(), phone.strip(), designation.strip(),
                 salary, hire_date, dept_map[dept]),
            )
            st.success("Employee added successfully.")
        except mysql.connector.IntegrityError:
            st.error("An employee with this email already exists.")
        except mysql.connector.Error as e:
            st.error(f"Database error: {e}")


def render_view():
    st.header("View / Search Employees")
    df = pd.DataFrame(get_employees())
    if df.empty:
        st.info("No employees found.")
        return
    c1, c2 = st.columns([2, 1])
    search = c1.text_input("Search by name, email or designation")
    dept_filter = c2.selectbox(
        "Department", ["All"] + sorted(df["dept_name"].dropna().unique().tolist())
    )
    if search:
        s = search.lower()
        mask = (
            df["name"].str.lower().str.contains(s, regex=False)
            | df["email"].str.lower().str.contains(s, regex=False)
            | df["designation"].fillna("").str.lower().str.contains(s, regex=False)
        )
        df = df[mask]
    if dept_filter != "All":
        df = df[df["dept_name"] == dept_filter]
    st.dataframe(df, use_container_width=True)
    st.caption(f"{len(df)} record(s) shown")
    st.download_button(
        "Download CSV", df.to_csv(index=False), "employees.csv", "text/csv"
    )


def render_update():
    st.header("Update Employee")
    rows = get_employees()
    depts = get_departments()
    if not rows or not depts:
        st.info("Add at least one department and one employee first.")
        return
    options = {f"{r['emp_id']} - {r['name']}": r for r in rows}
    choice = st.selectbox("Select Employee", list(options.keys()))
    emp = options[choice]
    eid = emp["emp_id"]
    dept_map = {d["dept_name"]: d["dept_id"] for d in depts}
    dept_names = list(dept_map.keys())
    idx = dept_names.index(emp["dept_name"]) if emp["dept_name"] in dept_names else 0

    with st.form("update_form"):
        name = st.text_input("Full Name", emp["name"], key=f"n{eid}")
        email = st.text_input("Email", emp["email"], key=f"e{eid}")
        phone = st.text_input("Phone", emp["phone"] or "", key=f"p{eid}")
        designation = st.text_input(
            "Designation", emp["designation"] or "", key=f"d{eid}"
        )
        salary = st.number_input(
            "Salary", min_value=0.0, value=float(emp["salary"]),
            step=1000.0, key=f"s{eid}",
        )
        dept = st.selectbox("Department", dept_names, index=idx, key=f"dp{eid}")
        submit = st.form_submit_button("Update")
    if submit:
        errors = validate_employee(name, email, phone, salary)
        if errors:
            for e in errors:
                st.error(e)
            return
        try:
            run_query(
                """UPDATE employees
                   SET name=%s, email=%s, phone=%s, designation=%s,
                       salary=%s, dept_id=%s
                   WHERE emp_id=%s""",
                (name.strip(), email.strip(), phone.strip(), designation.strip(),
                 salary, dept_map[dept], eid),
            )
            st.success("Employee updated successfully.")
        except mysql.connector.IntegrityError:
            st.error("Another employee already uses this email.")
        except mysql.connector.Error as e:
            st.error(f"Database error: {e}")


def render_delete():
    st.header("Delete Employee")
    rows = get_employees()
    if not rows:
        st.info("No employees to delete.")
        return
    options = {f"{r['emp_id']} - {r['name']}": r for r in rows}
    choice = st.selectbox("Select Employee", list(options.keys()))
    emp = options[choice]
    st.warning(f"You are about to delete {emp['name']}. This cannot be undone.")
    confirm = st.checkbox("I confirm I want to delete this employee")
    if st.button("Delete Employee", disabled=not confirm):
        run_query("DELETE FROM employees WHERE emp_id = %s", (emp["emp_id"],))
        st.success("Employee deleted. Reselect from the list to refresh.")
