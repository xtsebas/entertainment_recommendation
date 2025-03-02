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
    # Crear DataFrames para likes y dislikes
    df_likes = pd.DataFrame(likes_data)
    df_dislikes = pd.DataFrame(dislikes_data)
    # Ajustar nombres de columnas para visualización
    if not df_likes.empty:
        df_likes.rename(columns={
            "genre_id": "ID Género",
            "genre_name": "Nombre",
            "preference_level": "Preferencia",
            "aggregation_date": "Fecha Agregado",
            "last_engagement": "Última Interacción"
        }, inplace=True)

    if not df_dislikes.empty:
        df_dislikes.rename(columns={
            "genre_id": "ID Género",
            "genre_name": "Nombre",
            "rejection_level": "Rechazo",
            "aggregation_date": "Fecha Agregado",
            "last_engagement": "Última Interacción"
        }, inplace=True)

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
        st.write("### Eliminar 'LIKE'")
        for idx, row in df_likes.iterrows():
            col1, col2 = st.columns([4,1])
            with col1:
                st.text(f"{row['Nombre']} (Preferencia: {row['Preferencia']}, Fecha: {row['Fecha Agregado']})")
            with col2:
                if st.button("❌", key=f"like_{row['ID Género']}"):
                    likes_controller.delete_likes_relation(user_id, row["ID Género"])
                    st.success(f"Se ha eliminado el 'LIKE' del género {row['Nombre']}")
                    st.experimental_rerun()

    st.write("---")

    # Mostrar dislike en otra sección
    st.subheader("Géneros que NO te gustan")
    if df_dislikes.empty:
        st.info("Aún no has marcado ningún género como no favorito.")
    else:
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.dataframe(df_dislikes, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Botones para eliminar "DISLIKE"
        st.write("### Eliminar 'DISLIKE'")
        for idx, row in df_dislikes.iterrows():
            col1, col2 = st.columns([4,1])
            with col1:
                st.text(f"{row['Nombre']} (Rechazo: {row['Rechazo']}, Fecha: {row['Fecha Agregado']})")
            with col2:
                if st.button("❌", key=f"dislike_{row['ID Género']}"):
                    dislikes_controller.delete_dislikes_relation(user_id, row["ID Género"])
                    st.success(f"Se ha eliminado el 'DISLIKE' del género {row['Nombre']}")
                    st.experimental_rerun()

    st.write("---")

    # Agregar un nuevo DISLIKE
    st.subheader("Agregar Género a 'No me gusta'")

    # Conjuntos para filtrar géneros disponibles
    liked_ids = set(df_likes["ID Género"]) if not df_likes.empty else set()
    disliked_ids = set(df_dislikes["ID Género"]) if not df_dislikes.empty else set()

    # Filtrar los géneros que no están en like ni en dislike
    available_for_dislike = [
        g for g in all_genres
        if g["id"] not in liked_ids and g["id"] not in disliked_ids
    ]

    if available_for_dislike:
        # Mapear {nombre: dict_de_género} para el selectbox
        genre_map = {g["name"]: g for g in available_for_dislike}
        selected_name = st.selectbox("Selecciona un género:", list(genre_map.keys()))
        selected_genre = genre_map[selected_name]

        # Campos para la relación DISLIKES
        rejection_level = st.number_input("Nivel de rechazo:", min_value=1, max_value=10, value=5)
        aggregation_date_val = st.date_input("Fecha Agregado:", value=date.today())
        last_engagement_val = st.date_input("Última Interacción:", value=date.today())

        if st.button("Agregar a 'No me gusta'"):
            # Crear un nodo dummy para el usuario
            user_node = type("DummyUser", (), {"node_id": user_id})
            # Crear nodo Genre
            genre_node = Genre(
                genre_id=selected_genre["id"],
                name=selected_genre["name"],
                avg=selected_genre.get("avg", 0),
                description=selected_genre.get("description", ""),
                popular=selected_genre.get("popular", False)
            )
            # Crear la relación
            relation = DislikesRelation(
                start_node=user_node,
                end_node=genre_node,
                rejection_level=rejection_level,
                aggregation_date=aggregation_date_val.isoformat(),
                last_engagement=last_engagement_val.isoformat()
            )
            # Guardar 
            dislikes_controller.create_dislikes_relation(relation)
            st.success(f"Se agregó el género '{selected_name}' a tu lista de 'No me gusta'.")
            st.experimental_rerun()
    else:
        st.info("No hay géneros disponibles para marcar como no te gustan.")

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
