import pandas as pd
import streamlit as st

from ems.db import run_query

QUERIES = {
    "Salary rank within department (window function)": """
SELECT d.dept_name, e.name, e.salary,
       RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS dept_rank
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
ORDER BY d.dept_name, dept_rank""",
    "Earning above department average (CTE)": """
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees GROUP BY dept_id
)
SELECT e.name, d.dept_name, e.salary, ROUND(a.avg_salary, 0) AS dept_avg_salary
FROM employees e
JOIN dept_avg a ON e.dept_id = a.dept_id
JOIN departments d ON e.dept_id = d.dept_id
WHERE e.salary > a.avg_salary
ORDER BY e.salary DESC""",
    "Hiring trend by year": """
SELECT YEAR(hire_date) AS hire_year, COUNT(*) AS hires
FROM employees
GROUP BY YEAR(hire_date)
ORDER BY hire_year""",
    "Attendance percentage per employee": """
SELECT e.name,
       COUNT(a.att_id) AS days_recorded,
       ROUND(100 * SUM(a.status = 'Present') / COUNT(a.att_id), 1) AS attendance_pct
FROM employees e
JOIN attendance a ON e.emp_id = a.emp_id
GROUP BY e.emp_id, e.name
ORDER BY attendance_pct DESC""",
    "Salary cost by department": """
SELECT d.dept_name, COUNT(e.emp_id) AS headcount, SUM(e.salary) AS total_salary_cost
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY total_salary_cost DESC""",
}


def render():
    st.header("SQL Analytics")
    st.caption("Ready-made analytical queries. The SQL is shown so you can learn from it.")
    choice = st.selectbox("Choose a report", list(QUERIES.keys()))
    sql = QUERIES[choice].strip()
    st.code(sql, language="sql")
    rows = run_query(sql, fetch=True)
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No data returned. Run sql/seed.sql to load sample data.")
