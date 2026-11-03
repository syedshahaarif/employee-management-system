import streamlit as st
from mysql.connector import pooling

from ems.config import DB_CONFIG


@st.cache_resource
def _get_pool():
    return pooling.MySQLConnectionPool(pool_name="ems_pool", pool_size=5, **DB_CONFIG)


def run_query(query, params=None, fetch=False):
    """Run a parameterised query. Returns rows (fetch=True) or affected row count."""
    conn = _get_pool().get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(query, params or ())
        if fetch:
            return cur.fetchall()
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()


def get_departments():
    return run_query(
        "SELECT dept_id, dept_name FROM departments ORDER BY dept_name", fetch=True
    )


def get_employees():
    return run_query(
        """SELECT e.emp_id, e.name, e.email, e.phone, e.designation,
                  e.salary, e.hire_date, d.dept_name
           FROM employees e
           LEFT JOIN departments d ON e.dept_id = d.dept_id
           ORDER BY e.emp_id""",
        fetch=True,
    )
