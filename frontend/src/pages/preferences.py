import streamlit as st
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.similarTo_relation_controller import SimilarToRelationController

def show():
    user_id = st.session_state["user"].get("user_id")
    user = st.session_state["user"]
    st.title("⭐ Preferencias y Relaciones")
    st.write(f"Visualiza y gestiona las preferencias de los usuarios a {user['name']}.")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠️ No hay usuario autenticado en la sesión.")
        return
    
    if not user_id:
        st.error("⚠️ No se pudo obtener el ID del usuario.")
        return
    
    # Slider para seleccionar el umbral de similitud
    min_score = st.slider("Selecciona el umbral de similitud", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
    
    similar_to_controller = SimilarToRelationController()
    similar_users = similar_to_controller.get_similar_users(user_id, min_score)
    
    if not similar_users:
        st.info("No se encontraron usuarios similares.")
        similar_to_controller.close()
        return
    
    st.subheader("Usuarios Similares")
    df = pd.DataFrame(similar_users, columns=["similar_user_id", "similar_user_name", "score", "shared_genres"])
    df = df.rename(columns={
        "similar_user_name": "Nombre del Usuario",
        "score": "Similitud",
        "shared_genres": "Géneros Favoritos"
    })
    
    # Ajustar el ancho de la tabla al 100%
    st.markdown(
        """
        <style>
            .dataframe-container {
                width: 100%;
                overflow-x: auto;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Agregar botones para eliminar relación
    for _, row in df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.text(f"{row['Nombre del Usuario']} (Similitud: {row['Similitud']:.2f})")
        with col2:
            if st.button(f"❌ Eliminar", key=row["similar_user_id"]):
                similar_to_controller.delete_similar_to_relation(user_id, row["similar_user_id"])
                st.success(f"Relación con {row['Nombre del Usuario']} eliminada correctamente.")
                st.rerun()
    
    similar_to_controller.close()