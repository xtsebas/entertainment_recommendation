import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.auth import select_user
from src.router import show_page
from src.session_manager import is_authenticated
from src.sidebar import show_sidebar

# Configuración de la página
st.set_page_config(page_title="Sistema de Recomendación", layout="wide")

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Login"

# Si no hay usuario autenticado, mostrar selección de usuario
if not is_authenticated():
    select_user()
else:
    show_sidebar()
    show_page()