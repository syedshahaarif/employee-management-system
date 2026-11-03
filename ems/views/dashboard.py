import pandas as pd
import streamlit as st

from ems.db import run_query


def render():
    st.header("Dashboard")
    total = run_query("SELECT COUNT(*) AS c FROM employees", fetch=True)[0]["c"]
    depts = run_query("SELECT COUNT(*) AS c FROM departments", fetch=True)[0]["c"]
    payroll = run_query(
        "SELECT IFNULL(SUM(salary), 0) AS s FROM employees", fetch=True
    )[0]["s"]
    avg_sal = run_query(
        "SELECT IFNULL(AVG(salary), 0) AS a FROM employees", fetch=True
    )[0]["a"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", total)
    c2.metric("Departments", depts)
    c3.metric("Avg Salary", f"{float(avg_sal):,.0f}")
    c4.metric("Monthly Payroll", f"{float(payroll):,.0f}")

    rows = run_query(
        """SELECT d.dept_name, COUNT(e.emp_id) AS employees,
                  IFNULL(AVG(e.salary), 0) AS avg_salary
           FROM departments d
           LEFT JOIN employees e ON d.dept_id = e.dept_id
           GROUP BY d.dept_name""",
        fetch=True,
    )
    if rows:
        df = pd.DataFrame(rows)
        df["avg_salary"] = df["avg_salary"].astype(float)
        left, right = st.columns(2)
        with left:
            st.subheader("Headcount by Department")
            st.bar_chart(df.set_index("dept_name")["employees"])
        with right:
            st.subheader("Average Salary by Department")
            st.bar_chart(df.set_index("dept_name")["avg_salary"])
        st.dataframe(df, use_container_width=True)
