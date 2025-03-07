import streamlit as st
import sys
import os
import pandas as pd
from datetime import date
import uuid
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.genre_controller import GenreController
from backend.controller.likes_relation_controller import LikesRelationController
from backend.controller.dislikes_relation_controller import DislikesRelationController
from backend.view.genre import Genre
from backend.view.relations.dislikes import DislikesRelation


def show():


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
    .st-key-create button { background: linear-gradient(90deg, #4CAF50, #66BB6A); }
    .st-key-read button { background: linear-gradient(90deg, #2196F3, #42A5F5); }
    .st-key-update button { background: linear-gradient(90deg, #FFC107, #FFCA28); }
    .st-key-delete button { background: linear-gradient(90deg, #F44336, #E57373); }
    .stButton>button:hover { 
    filter: brightness(90%); 
    color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    
         
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
    if st.button("Crea un nuevo genero 🌠", key="create"):
        create_genre()

    if st.button("🕵️‍♀️ Insights de los generos 👀", key="update"):
        genre_insights()
        
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
                likes_controller.create_likes_relation_2(user_id, genre["name"])
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

@st.dialog("Sube tu rating ⭐")
def create_genre():
    genresController = GenreController()
    generos_existentes = [genre["name"] for genre in genresController.get_all_genres()]
    
    name = st.text_input("Nombre del género:")
    description = st.text_area("Descripción del género:")
    popular = st.checkbox("¿Es un género popular?")

    # Button to Create Genre
    if st.button("Crear Género"):
        if not name or not description:
            st.warning("Por favor, completa todos los campos.")
            return

        if name in generos_existentes:
            st.warning("El genero ya existe") 
            return
        # Generate random values
        genre_id = str(uuid.uuid4())  # Unique ID
        avg = round(random.uniform(1, 5), 2)  # Random float between 1 and 5

        # Create Genre object
        new_genre = Genre(
            genre_id=genre_id,
            name=name,
            avg=avg,
            description=description,
            popular=popular
        )

        # Call Controller to Insert into DB
        genre_controller = GenreController()
        genre_controller.create_new_genre(new_genre)

        st.success(f"✅ ¡El género '{name}' ha sido creado exitosamente!")
        st.rerun() 
    
@st.dialog("Genre insights")
def genre_insights():
    st.title("Los generos mas gustados por nuestros usarios 🤩")
    
    genre_controller = GenreController()


    total_genres = genre_controller.get_total_genres()
    st.info(f"📢 Actualmente tenemos **{total_genres} géneros** en nuestra plataforma!")

    # Get genre popularity
    popular_genres = genre_controller.get_genre_popularity()

    if not popular_genres:
        st.warning("No hay información disponible sobre los géneros más gustados.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(popular_genres)

    # Display the DataFrame
    st.subheader("📊 Ranking de Géneros por Likes")
    st.dataframe(df)

    # Highlight the most liked genre
    most_liked_genre = df.iloc[0]["genre"] if not df.empty else "N/A"
    most_likes = df.iloc[0]["like_count"] if not df.empty else 0

    st.success(f"🏆 ¡El género más gustado es **{most_liked_genre}** con **{most_likes} likes**!")
    
