import streamlit as st
import os
import sys
import pandas as pd
from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController
from backend.controller.genre_controller import GenreController
from backend.controller.likes_relation_controller import LikesRelationController
from backend.controller.similarTo_relation_controller import SimilarToRelationController


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

        selected_user = st.session_state["user"]

        # Mostrar la tarjeta del usuario seleccionado 
        show_user_card(selected_user)

        # CRUD
        st.markdown("## Operaciones CRUD")

        colB, colC, colD = st.columns(3)
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
        st.rerun()

    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.rerun()


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
        st.rerun()


def show_update_form(user_controller: UserController, user: dict):
    genre_controller = GenreController()
    similar_to_controller = SimilarToRelationController()

    genres = genre_controller.get_all_genres()
    genre_controller.close()
    #Muestra un formulario para actualizar un usuario.
    st.subheader("Actualizar Usuario")
    new_name = st.text_input("Nuevo Nombre:", value=user["name"])
    new_age = st.number_input("Nueva Edad:", min_value=0, max_value=120, value=user["age"])

    # Manejo de géneros favoritos
    fav_genres_str = user["favorite_genres"]

    # Convertir a lista si es un string
    if isinstance(fav_genres_str, str):
        fav_genres_list = fav_genres_str.split(",")
    else:
        fav_genres_list = fav_genres_str  # Ya es lista

    fav_genres_list = [genre.strip() for genre in fav_genres_list]
    genre_names = {genre["name"]: genre["id"] for genre in genres}

    # Mostrar multiselect con los nombres de géneros y preseleccionar los favoritos
    new_fav_genres = st.multiselect(
        "Selecciona tus géneros favoritos",
        options=list(genre_names.keys()),
        default=[genre for genre in fav_genres_list if genre in genre_names] 
    )
    new_fav_duration = st.number_input("Nueva Duración Favorita (min):", min_value=1, max_value=500, value=user["favorite_duration"])

    if st.button("Guardar Cambios"):

        updated_data = {
            "user_id": user['user_id'],
            "name": new_name,
            "age": new_age,
            "favorite_genres": ",".join(new_fav_genres),
            "favorite_duration": new_fav_duration
        }

        created_user = user_controller.update_user(user_data=updated_data)
        current_favorite_genres = user["favorite_genres"]
        current_favorite_genres = [genre.strip() for genre in current_favorite_genres.split(",")]


        if created_user:
            neo4j_user_id = user['user_id']  
                
            today = date.today()
            likes_controller = LikesRelationController() 
            for genre_name in current_favorite_genres:
                if genre_name not in new_fav_genres:
                    genre_id = genre_names.get(genre_name)
                    if genre_id:
                        print(f"❌ Eliminando relación LIKES: user_id={neo4j_user_id}, genre_id={genre_id}")
                        likes_controller.delete_likes_relation(neo4j_user_id, genre_id)

            for genre_name in new_fav_genres:
                genre_id = genre_names.get(genre_name)

                if genre_id:  
                    likes_controller.create_likes_relation(
                        user_id=neo4j_user_id,  
                        genre_id=genre_id,  
                        preference_level=5,  
                        aggregation_date=today,  
                        last_engagement=today  
                    )

            likes_controller.close()  
            similar_to_controller.create_similar_to_jaccard(neo4j_user_id)
            
            st.success(f"🎉 Usuario {new_name} creado con éxito! ID Neo4j: {neo4j_user_id}")
            st.session_state["user"] = created_user
            st.session_state["selected_page"] = "Users" 
            st.rerun()
        else:
            st.error("⚠️ Error al actualizar el usuario.")
            st.session_state["crud_action"] = None
            st.rerun()

    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.rerun()


def delete_user(user_controller: UserController, user: dict):
    #Elimina un usuario 
    st.subheader("Eliminar Usuario")
    st.write(f"¿Seguro que quieres eliminar al usuario '{user['name']}'?")
    if st.button("Confirmar"):
        user_controller.delete_user(user["user_id"])
        st.success(f"Usuario '{user['name']}' eliminado correctamente.")
        st.session_state["crud_action"] = None
        st.session_state["authenticated"] = False
        st.session_state["user"] = None
        st.session_state["selected_page"] = "Signup" 
        st.rerun()
    if st.button("Cancelar"):
        st.session_state["crud_action"] = None
        st.rerun()


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
