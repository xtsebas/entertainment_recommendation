import streamlit as st

def show_sidebar():
    """Sidebar para la navegación entre páginas."""
    with st.sidebar:
        st.title("Navigation")
        st.session_state["selected_page"] = st.radio(
            "Go to", ["Home", "Genres", "Users", "Preferences"]
        )
