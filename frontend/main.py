import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.auth import login
from src.router import show_page
from src.session_manager import is_authenticated

# Configuración de la página
st.set_page_config(page_title="Sistema de Recomendación", layout="wide")

# Verificar si el usuario ha iniciado sesión
if not is_authenticated():
    login()
else:
    show_page()
