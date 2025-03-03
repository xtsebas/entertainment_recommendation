import streamlit as st
import sys
import os
import pandas as pd
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.genre_controller import GenreController
from backend.controller.likes_relation_controller import LikesRelationController
from backend.controller.dislikes_relation_controller import DislikesRelationController
from backend.view.genre import Genre
from backend.view.relations.dislikes import DislikesRelation


def show():
    # Verificar si hay un usuario autenticado en la sesión
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠️ No hay usuario autenticado en la sesión.")
        return

    user = st.session_state["user"]
    user_id = user.get("user_id")
    if not user_id:
        st.error("⚠️ No se pudo obtener el ID del usuario.")
        return

    st.title("⭐ Gestión de Géneros")
    st.write(f"Visualiza y gestiona los géneros que te gustan o no te gustan, {user['name']}.")

    # Instanciar controladores
    genre_controller = GenreController()
    likes_controller = LikesRelationController()
    dislikes_controller = DislikesRelationController()

    # Obtener géneros que el usuario ha marcado como LIKE
    likes_data = likes_controller.get_likes_by_user(user_id) or []
    # Obtener géneros que el usuario ha marcado como DISLIKE
    dislikes_data = dislikes_controller.get_dislikes_by_user(user_id) or []
    # Todos los géneros
    all_genres = genre_controller.get_all_genres() or []
    
    unrated_genres = likes_controller.get_unrated_genres(user_id=user_id) or []
    # Crear DataFrames para likes y dislikes
    df_likes = pd.DataFrame(likes_data)
    df_dislikes = pd.DataFrame(dislikes_data)
    # Ajustar nombres de columnas para visualización
    
    print("likes data :)")
    print(df_likes)

    

    # Mostrar likes en una sección
    st.subheader("Géneros que te gustan")
    if df_likes.empty:
        st.info("Aún no has marcado ningún género como favorito.")
    else:
        # Para mostrar la tabla 
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df_likes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Botones para eliminar "LIKE"
        st.write("### Eliminar de mis generos ❌")
        for idx, row in df_likes.iterrows():
            col1, col2 = st.columns([4,1])
            with col1:
                st.text(f"{row['genre_name']} (preference_level: {row['preference_level']}, Fecha: {row['aggregation_date']})")
            with col2:
                if st.button("❌", key=f"like_{row['genre_name']}"):
                    likes_controller.delete_likes_relation(user_id, row["genre_id"])
                    st.success(f"Se ha eliminado el 'LIKE' del género {row['genre_name']}")
                    st.rerun()
    st.subheader('Agregar generos a mis gustos')
    
    if not all_genres:
        st.info('No hay generos para agregar')
    
    for genre in all_genres:
        col1, col2 = st.columns([3, 1])  # Create two columns (Genre Name | Add Button)
        
        with col1:
            st.write(f"🤖 {genre["name"]}")

        with col2:
            if st.button(f"Agregar", key=genre["name"]):
                print("I will add genre with genre_name -> ", genre["name"])
                likes_controller.create_likes_relation(user_id, genre["name"])
                st.success(f"¡'{genre}' ha sido agregado a tus gustos!")
                st.rerun()  
    

    st.write("---")

    # Mostrar dislike en otra sección
    st.subheader("Géneros que NO te gustan")
    if df_dislikes.empty:
        st.info("Aún no has marcado ningún género como no favorito.")
    else:
        st.dataframe(df_dislikes, use_container_width=True)

        # # Botones para eliminar "DISLIKE"
        # st.write("### Eliminar 'DISLIKE'")
        # for idx, row in df_dislikes.iterrows():
        #     col1, col2 = st.columns([4,1])
        #     with col1:
        #         st.text(f"{row['Nombre']} (Rechazo: {row['Rechazo']}, Fecha: {row['Fecha Agregado']})")
        #     with col2:
        #         if st.button("❌", key=f"dislike_{row['ID Género']}"):
        #             dislikes_controller.delete_dislikes_relation(user_id, row["ID Género"])
        #             st.success(f"Se ha eliminado el 'DISLIKE' del género {row['Nombre']}")
        #             st.experimental_rerun()

    st.write("---")

    # Agregar un nuevo DISLIKE
    st.subheader("👎 Agregar géneros que NO me gustan")
    print(all_genres)

    if not all_genres:
        st.info("No hay géneros disponibles.")
        return

    # Display genres with "Dislike" buttons
    for genre in all_genres:
        col1, col2 = st.columns([3, 1])  # Two columns: Genre Name | Dislike Button

        with col1:
            st.write(f"🎵 {genre['name']}")

        with col2:
            if st.button("Dislike", key=genre['id']):
                print("I will dislike genre_id -> ", genre["id"])
                dislikes_controller.dislike_genre_by_user(user_id=user_id, genre_id=genre["id"])
                st.success(f"¡'{genre['name']}' ha sido marcado como 'Disliked'!")
                st.rerun()  


    

    # Inyectar estilos 
    st.markdown("""
    <style>
    .dataframe-container {
        width: 100%;
        overflow-x: auto;
        margin-bottom: 20px;
    }
    .stDataFrame table {
        width: 100%;
    }
    .stButton>button {
        font-size: 16px;
        padding: 6px 12px;
        border-radius: 8px;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
