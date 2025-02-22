import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.pages import home, genres, users, preferences

# Definir un diccionario con las rutas disponibles
ROUTES = {
    "Home": home.show,
    "Genres": genres.show,
    "Users": users.show,
    "Preferences": preferences.show
}

def navigate_to():
    """Determina qué pantalla mostrar según la selección en el sidebar."""
    page = st.session_state.get("selected_page", "Home")  # Por defecto, muestra 'Home'
    
    if page in ROUTES:
        ROUTES[page]()  # Llama a la función correspondiente
    else:
        st.error("Página no encontrada")
