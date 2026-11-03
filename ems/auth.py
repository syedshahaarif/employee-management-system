import hmac

import streamlit as st

from ems.config import APP_PASSWORD


def require_login() -> bool:
    """Show a login box if APP_PASSWORD is set. Returns True when access is allowed."""
    if not APP_PASSWORD:
        return True
    if st.session_state.get("authed"):
        return True
    st.title("Employee Management System")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if hmac.compare_digest(pw, APP_PASSWORD):
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    return False
