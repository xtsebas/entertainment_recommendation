import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.auth import login
from src.router import show_page
from src.sidebar import show_sidebar
from src.session_manager import is_authenticated
from src.pages.signup import signup 

# Configuración de la página
st.set_page_config(page_title="Sistema de Recomendación", layout="wide")

# Inicializa el estado de sesión si no existe
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Login"

# Manejo de páginas según la sesión
if st.session_state["selected_page"] == "Signup":
    signup() 
elif not is_authenticated():
    login()
else:
    show_sidebar()
    show_page()
