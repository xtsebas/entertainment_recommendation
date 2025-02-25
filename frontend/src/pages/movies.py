import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

def show():
    st.title("🎵 Gestión de las peliculas")
    st.write("Aquí puedes ver y administrar las peliculas.")