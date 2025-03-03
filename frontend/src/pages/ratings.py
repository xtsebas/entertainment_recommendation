import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.rating_controller import RatingController

def show():
    user_id = st.session_state["user"].get("user_id")
    user = st.session_state["user"]
    st.title("🔢 Gestion de Ratings")
    st.write(f"Visualiza y gestiona las preferencias de los usuarios a {user['name']}.")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠️ No hay usuario autenticado en la sesión.")
        return
    
    if not user_id:
        st.error("⚠️ No se pudo obtener el ID del usuario.")
        return
    
    rating_controller = RatingController()
    rating_user = rating_controller.get_ratings_user(user_id)
    
    if not rating_user:
        st.info("No se encontraron usuarios similares.")
        rating_controller.close()
        return
    
    st.subheader("Ratings Hechos")
    df = pd.DataFrame(rating_user, columns=["rating_id", "Title", "Rating", "Comment", "Date"])
    df = df.rename(columns={
        "rating_id": "Id",
        "Title": "Titulo",
        "Rating": "Rating",
        "Comment": "Comentario",
        "Date": "Date"
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
    st.markdown("---")

    st.subheader("Gestionar Ratings")
    
    # Agregar botones para eliminar relación
    for _, row in df.iterrows():
          col1, col2 = st.columns([4, 1])
          with col1:
               st.text(f"{row['Titulo']} (Rating: {row['Rating']:.2f})")
          with col2:
               if st.button(f"❌ Eliminar", key=row["Titulo"]):
                    rating_controller.delete_rating(row["Id"])
                    st.success(f"Relación con {row['Titulo']} eliminada correctamente.")
                    st.rerun()
    
    rating_controller.close()