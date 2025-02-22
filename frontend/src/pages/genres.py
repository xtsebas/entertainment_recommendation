import streamlit as st

def show():
    st.title("🎵 Gestión de Géneros")
    st.write("Aquí puedes ver y administrar los géneros de entretenimiento.")

    # Ejemplo de tabla
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
    st.table({"Géneros Disponibles": genres})
