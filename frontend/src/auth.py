import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController  # Importamos el controlador de usuarios

def login():
    """Muestra la pantalla de login y maneja la autenticación directamente con el controlador."""
    st.title("Iniciar Sesión")
    
    name = st.text_input("Nombre de usuario", key="username")
    password = st.text_input("Contraseña", type="password", key="password")

    if st.button("Iniciar Sesión"):
        if name and password:
            user_controller = UserController()  # Creamos instancia del controlador
            
            user_data = user_controller.get_user_by_credentials(name, password)  # Llamamos directamente la función
            
            if user_data:
                st.session_state["authenticated"] = True
                st.session_state["user"] = user_data
                st.success(f"Bienvenido {user_data['name']} 🎉")
                st.experimental_rerun()
            else:
                st.error("❌ Credenciales incorrectas. Intenta de nuevo.")
            
            user_controller.close()  # Cerramos la conexión con Neo4j
        else:
            st.warning("⚠️ Por favor, ingresa tus credenciales.")

def logout():
    """Cierra sesión del usuario."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.experimental_rerun()
