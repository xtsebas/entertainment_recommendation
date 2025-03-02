import streamlit as st
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.controller.user_controller import UserController

def show():
    st.title("👤 Gestión de Usuarios")

    # Verificar si ya tenemos un controlador en la sesión o crearlo
    if "user_controller" not in st.session_state:
        st.session_state["user_controller"] = UserController()

    user_controller = st.session_state["user_controller"]

    # Cargar la lista de usuarios 
    users = user_controller.get_users()
    if not users:
        st.warning("No hay usuarios disponibles en la base de datos.")
        # Crear un nuevo usuario si la lista está vacía
        if st.button("Crear un nuevo usuario"):
            st.session_state["crud_action"] = "create"
        else:
            return
    else:
        if "selected_user_index" not in st.session_state:
            st.session_state["selected_user_index"] = 0

        selected_index = st.session_state["selected_user_index"]
        # Indice no se salga de rango si se eliminan usuarios
        if selected_index >= len(users):
            st.session_state["selected_user_index"] = 0
            selected_index = 0

        selected_user = users[selected_index]

        # Mostrar la tarjeta del usuario seleccionado 
        show_user_card(selected_user)

        # Botones de navegación (anterior/siguiente)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Anterior", key="prev_user") and selected_index > 0:
                st.session_state["selected_user_index"] -= 1
                st.experimental_rerun()
        with col3:
            if st.button("Siguiente ➡️", key="next_user") and selected_index < len(users) - 1:
                st.session_state["selected_user_index"] += 1
                st.experimental_rerun()

        st.markdown("---")
        # Botón para seleccionar el usuario e iniciar sesión 
        if st.button(f"Seleccionar {selected_user['name']}", key="select_user"):
            st.session_state["authenticated"] = True
            st.session_state["user"] = selected_user  # Guardar el usuario en la sesión
            st.success(f"Has seleccionado a {selected_user['name']}")
            st.session_state["selected_page"] = "Home"
            st.experimental_rerun()

        # CRUD
        st.markdown("## Operaciones CRUD")

        colA, colB, colC, colD = st.columns(4)
        with colA:
            if st.button("🆕 Crear", key="create"):
                st.session_state["crud_action"] = "create"
        with colB:
            if st.button("🔍 Leer", key="read"):
                st.session_state["crud_action"] = "read"
        with colC:
            if st.button("✏️ Actualizar", key="update"):
                st.session_state["crud_action"] = "update"
        with colD:
            if st.button("🗑️ Eliminar", key="delete"):
                st.session_state["crud_action"] = "delete"

    accion = st.session_state.get("crud_action")
    if accion == "create":
        show_create_form(user_controller)
    elif accion == "read":
        show_read(users)
    elif accion == "update":
        if users:
            show_update_form(user_controller, selected_user)
    elif accion == "delete":
        if users:
            delete_user(user_controller, selected_user)

    # Estilos CSS
    inject_css()


def show_user_card(user):
    #Muestra la tarjeta de un usuario con estilo.
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
        margin-bottom: 10px;
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
        <p class="name-client">{user['name']}<br>
            <span>Edad: {user['age']}</span>
            <span>Géneros favoritos: {user['favorite_genres']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def show_create_form(user_controller: UserController):
    #Muestra un formulario para crear un nuevo usuario.
    st.subheader("Crear Usuario")
    name = st.text_input("Nombre:")
    age = st.number_input("Edad:", min_value=0, max_value=120, value=25)
    favorite_genres = st.text_input("Géneros favoritos (separa con comas):", value="Acción, Comedia")
    favorite_duration = st.number_input("Duración favorita (min):", min_value=1, max_value=500, value=90)

    if st.button("Guardar"):
        genres_str = favorite_genres.strip()
        new_user_data = {
            "name": name,
            "age": age,
            "favorite_genres": genres_str,
            "favorite_duration": favorite_duration
        }
        created_user = user_controller.create_user_object(new_user_data)
        if created_user:
            st.success(f"Usuario '{name}' creado exitosamente.")
        else:
            st.error("Error al crear el usuario en Neo4j.")
        st.session_state["crud_action"] = None
        st.experimental_rerun()

    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.experimental_rerun()


def show_read(users: list):
    #Muestra todos los usuarios en una tabla
    st.subheader("Lista de Usuarios")
    if not users:
        st.info("No hay usuarios en la BD.")
        return

    df = pd.DataFrame(users)
    st.dataframe(df)
    if st.button("Cerrar"):
        st.session_state["crud_action"] = None
        st.experimental_rerun()


def show_update_form(user_controller: UserController, user: dict):
    #Muestra un formulario para actualizar un usuario.
    st.subheader("Actualizar Usuario")
    new_name = st.text_input("Nuevo Nombre:", value=user["name"])
    new_age = st.number_input("Nueva Edad:", min_value=0, max_value=120, value=user["age"])
    # Manejo de géneros favoritos
    fav_genres_str = user["favorite_genres"]
    if isinstance(fav_genres_str, list):
        fav_genres_str = ", ".join(fav_genres_str)

    new_fav_genres = st.text_input("Nuevos Géneros (separa con comas):", value=fav_genres_str)
    new_fav_duration = st.number_input("Nueva Duración Favorita (min):", min_value=1, max_value=500, value=user["favorite_duration"])

    if st.button("Guardar Cambios"):
        # Update con (delete + create)
        user_controller.delete_user(user["user_id"])
        updated_data = {
            "name": new_name,
            "age": new_age,
            "favorite_genres": new_fav_genres,
            "favorite_duration": new_fav_duration
        }
        created_user = user_controller.create_user_object(updated_data)
        if created_user:
            st.success("Usuario actualizado correctamente.")
            st.session_state["user"] = created_user
        else:
            st.error("Error al actualizar el usuario.")
        st.session_state["crud_action"] = None
        st.experimental_rerun()

    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.experimental_rerun()


def delete_user(user_controller: UserController, user: dict):
    #Elimina un usuario 
    st.subheader("Eliminar Usuario")
    st.write(f"¿Seguro que quieres eliminar al usuario '{user['name']}'?")
    if st.button("Confirmar"):
        user_controller.delete_user(user["user_id"])
        st.success(f"Usuario '{user['name']}' eliminado correctamente.")
        st.session_state["crud_action"] = None
        st.experimental_rerun()
    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.experimental_rerun()


def inject_css():
    # CSS para tablas y botones
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 45px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        margin: 5px 0;
        transition: 0.3s;
        color: white;
        border: none;
    }
    .stButton>button:focus { outline: none; }
    .stButton>button:hover { 
        filter: brightness(90%); 
        color: black;
    }
    .stDataFrame { font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)
