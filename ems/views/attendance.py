from datetime import date

import pandas as pd
import streamlit as st

from ems.db import get_employees, run_query


def render():
    st.header("Attendance")
    rows = get_employees()
    if not rows:
        st.info("No employees found.")
        return
    options = {f"{r['emp_id']} - {r['name']}": r["emp_id"] for r in rows}
    tab1, tab2 = st.tabs(["Mark Attendance", "Attendance Report"])
    with tab1:
        choice = st.selectbox("Employee", list(options.keys()))
        att_date = st.date_input("Date", value=date.today())
        status = st.radio("Status", ["Present", "Absent", "Leave"], horizontal=True)
        if st.button("Save Attendance"):
            run_query(
                """INSERT INTO attendance (emp_id, att_date, status)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE status = VALUES(status)""",
                (options[choice], att_date, status),
            )
            st.success("Attendance saved.")
    with tab2:
        report = run_query(
            """SELECT e.name,
                      COALESCE(SUM(a.status = 'Present'), 0) AS present_days,
                      COALESCE(SUM(a.status = 'Absent'), 0) AS absent_days,
                      COALESCE(SUM(a.status = 'Leave'), 0) AS leave_days
               FROM employees e
               LEFT JOIN attendance a ON e.emp_id = a.emp_id
               GROUP BY e.emp_id, e.name""",
            fetch=True,
        )
        st.dataframe(pd.DataFrame(report), use_container_width=True)
