import streamlit as st

def show_sidebar():
    """Sidebar para la navegación entre páginas."""
    with st.sidebar:
        st.title("Navigation")
        
        #to manage nodes (5 total) + 1 media
        st.session_state["selected_page"] = st.radio(
            "Data", ["Home", "Genres", "Users", "Ratings", "Movies", "Series", "Preferences", "Watched"]
        )