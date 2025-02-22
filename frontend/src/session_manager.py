import streamlit as st

def is_authenticated():
    """Verifica si el usuario ha iniciado sesión."""
    return st.session_state.get("authenticated", False)

def get_current_user():
    """Obtiene los datos del usuario autenticado."""
    return st.session_state.get("user", None)
