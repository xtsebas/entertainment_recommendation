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
          col1, col2, col3 = st.columns([5, 1, 1])
          with col1:
               st.text(f"{row['Titulo']} (Rating: {row['Rating']:.2f})")
          with col2:
               if st.button(f"⬆️ Editar", key=row["Titulo"]):
                    rate(media_type="Movie", rating_id=row["Id"], media_title=row["Titulo"])

          with col3:
               if st.button(f"❌ Eliminar", key=f"delete_{row['Id']}"):
                    rating_controller.delete_rating(row["Id"])
                    st.success(f"Relación con {row['Titulo']} eliminada correctamente.")
                    st.rerun()
    
    rating_controller.close()

@st.dialog("Edita tu rating ⭐")
def rate(media_type: str, rating_id: str, media_title=str):
    user = st.session_state["user"]
    st.write(media_title)
    rating_controller = RatingController()


    actual_rating = rating_controller.get_rating(rating_id=rating_id)
    
    st.markdown(f'🎞️ **{media_title} 📺**')

    # Definir valores por defecto si ya existe un rating previo
    default_rating = actual_rating["rating"] if actual_rating else 3
    default_comment = actual_rating["comment"] if actual_rating else ""
    default_feeling = actual_rating["final_feeling"] if actual_rating else "Neutral"
    default_recommend = actual_rating["recommend"] if actual_rating else False

    # Slider para calificación
    rating = st.slider("⭐ Calificación", min_value=1, max_value=5, step=1, value=default_rating)

    # Campo de comentario
    comment = st.text_area("📝 Comentario (opcional)", default_comment)

    # Seleccionar el sentimiento final
    final_feeling = st.selectbox(
        "¿Cómo te sientes acerca de este contenido?",
        ["Very Good", "Good", "Neutral", "Bad", "Very Bad"],
        index=["Very Good", "Good", "Neutral", "Bad", "Very Bad"].index(default_feeling)
    )

    # Checkbox de recomendación
    recommend = st.checkbox("¿Recomendarías este contenido?", value=default_recommend)

    
    if st.button("Guardar"):
        rating_data = {
            "rating_id": rating_id,
            "user_id": user['user_id'],
            "rating": rating,
            "comment": comment,
            "final_feeling": final_feeling,
            "recommend": recommend
        }

        # Si existe un rating, actualizarlo; de lo contrario, crearlo
        if actual_rating:
            rating_controller.update_rating(rating_data)
            st.success("✅ Calificación actualizada correctamente.")

        st.rerun()
