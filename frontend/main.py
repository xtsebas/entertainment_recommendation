import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.router import navigate_to

st.set_page_config(page_title="Entertainment Recommendation", layout="wide")

# Mostrar sidebar para la navegación
from src.sidebar import show_sidebar
show_sidebar()

# Mostrar la página seleccionada
navigate_to()
