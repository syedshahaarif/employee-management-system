import mysql.connector
import pandas as pd
import streamlit as st

from ems.db import get_departments, run_query


def render():
    st.header("Departments")
    with st.form("dept_form", clear_on_submit=True):
        name = st.text_input("New Department Name")
        submit = st.form_submit_button("Add Department")
    if submit:
        if not name.strip():
            st.error("Department name is required.")
        else:
            try:
                run_query(
                    "INSERT INTO departments (dept_name) VALUES (%s)", (name.strip(),)
                )
                st.success("Department added.")
            except mysql.connector.IntegrityError:
                st.error("This department already exists.")
            except mysql.connector.Error as e:
                st.error(f"Database error: {e}")
    st.dataframe(pd.DataFrame(get_departments()), use_container_width=True)
