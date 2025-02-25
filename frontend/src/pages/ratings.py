import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from frontend.src.pages.ratings_crud.rating_crud_forms import show_create_rating

def show():
    st.title("🎵 Gestión de los Ratings")
    st.write("Aquí puedes ver y administrar los Ratings.")

    # Inicializar la acción CRUD si no existe
    if "crud_action" not in st.session_state:
        st.session_state["crud_action"] = None

    # Inyectar estilos CSS para los botones de Streamlit
    st.markdown("""
    <style>
    /* Aplica a los botones generados con st.button */
    .stButton>button {
         width: 100%;
         height: 60px;
         font-size: 20px;
         font-weight: bold;
         border-radius: 8px;
         margin: 10px 0;
         transition: 0.3s;
         color: white;
         border: none;
    }
    /* Estilos individuales para cada botón */
    .stButton>button:focus { outline: none; }
    .create-button { background: linear-gradient(90deg, #4CAF50, #66BB6A); }
    .read-button   { background: linear-gradient(90deg, #2196F3, #42A5F5); }
    .update-button { background: linear-gradient(90deg, #FFC107, #FFCA28); }
    .delete-button { background: linear-gradient(90deg, #F44336, #E57373); }
    .stButton>button:hover { filter: brightness(90%); }
    </style>
    """, unsafe_allow_html=True)

    # Se usan st.button para actualizar el estado de sesión y refrescar la app
    if st.button("📝 Create", key="create"):
         st.session_state["crud_action"] = "create"
    if st.button("🔍 Read", key="read"):
         st.session_state["crud_action"] = "read"
    if st.button("✏️ Update", key="update"):
         st.session_state["crud_action"] = "update"
    if st.button("🗑️ Delete", key="delete"):
         st.session_state["crud_action"] = "delete"

    # Mostrar contenido basado en la acción seleccionada
    accion = st.session_state.get("crud_action")
    if accion == "create":
         st.subheader("Crear Rating")
         st.write("Aquí va el formulario para crear un nuevo rating.")
         show_create_rating()
    elif accion == "read":
         st.subheader("Leer Ratings")
         st.write("Aquí se muestran los ratings existentes.")
         # Agregar la lógica de lectura de ratings
    elif accion == "update":
         st.subheader("Actualizar Rating")
         st.write("Aquí puedes actualizar un rating existente.")
         # Agregar la lógica de actualización
    elif accion == "delete":
         st.subheader("Eliminar Rating")
         st.write("Aquí puedes eliminar un rating.")
         # Agregar la lógica de eliminación        

    # Botón para volver al menú principal (resetear la acción)
    if st.button("Volver al menú", key="menu"):
        st.session_state["crud_action"] = None