import streamlit as st

def show():
    user = st.session_state["user"]
    st.title("🎬 Entertainment Recommendation")
    st.write(f"Bienvenido {user['name']} al sistema de recomendación de entretenimiento.")
    st.image("https://wallpapers.com/images/featured/film-pictures-vbq45si2ir8k7fw3.jpg")
