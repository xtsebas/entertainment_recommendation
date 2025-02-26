import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController  # Importamos el controlador de usuarios

def select_user():
    """ Muestra una lista de usuarios en forma de tarjetas y permite seleccionarlos para ingresar. """
    st.title("Selecciona tu Usuario")

    user_controller = UserController()
    users = user_controller.get_users()  # Obtener todos los usuarios
    user_controller.close()

    if not users:
        st.warning("No hay usuarios disponibles.")
        return

    # Inicializar el índice del usuario seleccionado en el session_state
    if "selected_user_index" not in st.session_state:
        st.session_state["selected_user_index"] = 0

    # Obtener el usuario seleccionado actualmente
    selected_index = st.session_state["selected_user_index"]
    selected_user = users[selected_index]

    # Estilos CSS para la tarjeta del usuario
    st.markdown(f"""
    <style>
    .card-client {{
        background: #2cb5a0;
        width: 250px;
        padding: 20px;
        border: 4px solid #7cdacc;
        box-shadow: 0 6px 10px rgba(207, 212, 222, 1);
        border-radius: 10px;
        text-align: center;
        color: #fff;
        font-family: "Poppins", sans-serif;
        transition: all 0.3s ease;
        margin: auto;
    }}
    .card-client:hover {{
        transform: translateY(-10px);
    }}
    .user-picture {{
        width: 100px;
        height: 100px;
        border: 4px solid #7cdacc;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: auto;
        background: white;
    }}
    .name-client {{
        margin-top: 15px;
        font-weight: 600;
        font-size: 18px;
    }}
    .name-client span {{
        display: block;
        font-weight: 200;
        font-size: 16px;
    }}
    </style>

    <div class="card-client">
        <div class="user-picture">
            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="User Picture" style="border-radius: 50%; width: 100%;">
        </div>
        <p class="name-client">{selected_user['name']}<br>
            <span>Edad: {selected_user['age']}</span>
            <span>Generos favoritos: {selected_user['favorite_genres']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botones de navegación (⬅️ y ➡️)
    col1, col2, col3 = st.columns([1, 2, 1])  # Espaciado para centrar los botones

    with col1:
        if st.button("⬅️ Anterior", key="prev_user") and selected_index > 0:
            if selected_index > 0:
                st.session_state["selected_user_index"] -= 1
            st.rerun() 

    with col3:
        if st.button("Siguiente ➡️", key="next_user") and selected_index < len(users) - 1:
            if selected_index < len(users) - 1:
                st.session_state["selected_user_index"] += 1
            st.rerun() 

    # Botón para seleccionar el usuario y entrar en la app
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"Seleccionar {selected_user['name']}", key="select_user"):
        st.session_state["authenticated"] = True
        st.session_state["user"] = selected_user  # Guardar datos del usuario seleccionado
        st.session_state["selected_page"] = "Home"  # Ir a Home
        st.rerun() 