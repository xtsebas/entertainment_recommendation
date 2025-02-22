import streamlit as st

def show():
    st.title("👤 Gestión de Usuarios")
    st.write("Lista de usuarios y sus preferencias de entretenimiento.")

    users = ["John Doe", "Jane Smith", "Mike Johnson"]
    st.table({"Usuarios": users})
