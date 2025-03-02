import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.pages import home, genres, users, preferences, signup, ratings, movies, series, watched
from src.session_manager import is_authenticated

# Definir rutas disponibles
ROUTES = {
    "Home": home.show,
    "Genres": genres.show,
    "Users": users.show,
    "Preferences": preferences.show,
    "Signup": signup.signup,
    "Ratings" : ratings.show,
    "Movies" : movies.show,
    "Series" : series.show,
    "Watched" : watched.show
}

def show_page():
    # """Maneja la navegación de pantallas basado en la autenticación."""
    # if not is_authenticated():
    #     st.session_state["selected_page"] = "Login"

    page = st.session_state.get("selected_page", "Home")  # Página por defecto: Home
    
    if page in ROUTES:
        ROUTES[page]()  # Llama a la función correspondiente
    else:
        st.error("❌ Página no encontrada")
