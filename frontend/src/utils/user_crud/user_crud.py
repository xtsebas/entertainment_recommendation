import streamlit as st
import uuid
import os
import sys
from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController
from backend.controller.genre_controller import GenreController
from backend.controller.likes_relation_controller import LikesRelationController
from backend.controller.similarTo_relation_controller import SimilarToRelationController
from backend.view.user import User

def show_create_user():
    """Formulario para crear un nuevo usuario en la base de datos."""
    
    st.title("🆕 Crear Nuevo Usuario")

    user_controller = UserController()
    genre_controller = GenreController()
    similar_to_controller = SimilarToRelationController()

    # Obtener géneros disponibles desde la base de datos
    genres = genre_controller.get_all_genres()
    genre_controller.close()

    # Validar si hay géneros disponibles
    if not genres:
        st.warning("⚠️ No hay géneros disponibles en la base de datos.")
        return

    # Campos del formulario
    name = st.text_input("Nombre de usuario")
    age = st.number_input("Edad", min_value=18, max_value=100, step=1)

    # Mostrar los géneros disponibles como opciones seleccionables
    genre_names = {genre["name"]: genre["id"] for genre in genres}  # Mapeo de nombre a ID
    favorite_genres = st.multiselect("Selecciona tus géneros favoritos", list(genre_names.keys()))

    favorite_duration = st.number_input("Duración favorita (minutos)", min_value=30, max_value=300, step=10)
    
    # Botón para crear el usuario
    if st.button("✅ Crear Usuario"):
        if not name or not favorite_genres:
            st.error("⚠️ El nombre y los géneros favoritos son obligatorios.")
        else:
            user = User(
                name=name,
                age=age,
                favorite_genres=",".join(favorite_genres),  # Guardar géneros como string separado por comas
                favorite_duration=favorite_duration
            )
            
            userCreate = user_controller.create_user(user)

            if userCreate:  
                neo4j_user_id = userCreate['user_id']  # Usamos el ID asignado por Neo4j
                
                today = date.today()
                likes_controller = LikesRelationController() 
                for genre_name in favorite_genres:
                    genre_id = genre_names.get(genre_name)

                    if genre_id:  
                        likes_controller.create_likes_relation(
                            user_id=neo4j_user_id,  
                            genre_id=genre_id,  
                            preference_level=5,  
                            aggregation_date=today,  
                            last_engagement=today  
                        )
                        print(f"✅ Creando relación LIKES con: user_id={neo4j_user_id}, genre_id={genre_id}")
                    else:
                        print(f"⚠️ No se encontró el ID para el género '{genre_name}', no se creará la relación.")
                
                likes_controller.close()  
                similar_to_controller.create_similar_to_jaccard(neo4j_user_id)

                
                st.success(f"🎉 Usuario {name} creado con éxito! ID Neo4j: {neo4j_user_id}")
                st.session_state["authenticated"] = True
                st.session_state["user"] = userCreate  # Guardar el usuario en la sesión con el ID correcto
                st.session_state["selected_page"] = "Home"
                st.rerun()
            else:
                st.error("⚠️ Error al crear el usuario.")

    user_controller.close()

def show_read_user():
    pass 

def show_update_user():
    pass 

def show_delete_user():
    pass 


