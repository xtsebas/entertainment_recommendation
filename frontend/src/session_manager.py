import streamlit as st

def is_authenticated():
    """Verifica si hay un usuario autenticado en la sesión."""
    return st.session_state.get("authenticated", False)
