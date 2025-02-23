import streamlit as st
import uuid  
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController
from backend.view.user import User

# Lista de géneros disponibles
GENRES = ["Acción", "Comedia", "Drama", "Terror", "Ciencia Ficción", "Romance", "Aventura", "Documental", "Fantasía"]

def signup():
    """Muestra la pantalla de registro de usuario."""
    st.title("Registro de Nuevo Usuario")

    name = st.text_input("Nombre de usuario", key="signup_username")
    password = st.text_input("Contraseña", type="password", key="signup_password")
    age = st.number_input("Edad", min_value=1, max_value=120, step=1, key="signup_age")
    
    favorite_genres = st.multiselect("Selecciona tus géneros favoritos", GENRES, key="signup_genres")
    favorite_duration = st.number_input("Duración favorita (minutos)", min_value=30, max_value=300, step=10, key="signup_duration")

    if st.button("Registrarse"):
        if name and password and age and favorite_genres:
            user_controller = UserController()
            
            new_user = User(
                user_id=str(uuid.uuid4()),  # Generamos un user_id único
                name=name,
                password= password,
                age=age,
                favorite_genres=favorite_genres,
                favorite_duration=favorite_duration
            )

            response = user_controller.create_user(new_user, password)
            user_controller.close()
            
            if response["message"] == "Usuario creado correctamente":
                st.success("✅ Usuario registrado con éxito. ¡Ahora inicia sesión!")
            else:
                st.error("❌ Error al registrar usuario. Intenta de nuevo.")
        else:
            st.warning("⚠️ Todos los campos son obligatorios excepto la duración.")
    
    # Opción para volver al Login
    st.markdown("---")
    st.markdown("¿Ya tienes una cuenta? [Inicia sesión aquí](#)", unsafe_allow_html=True)
    if st.button("Volver al Login"):
        st.session_state["selected_page"] = "Login"
