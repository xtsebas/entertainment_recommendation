import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.user_controller import UserController
from datetime import datetime

def format_date(date_value):
    try:
        print(f"📅 Raw Date: {date_value} | Type: {type(date_value)}")  # Debugging

        if isinstance(date_value, datetime):  
            return date_value.strftime("%d %b %Y")  # Si ya es datetime, formatear directamente

        elif isinstance(date_value, str):  
            clean_date = date_value.split("T")[0]  # Removemos la parte de la hora
            return datetime.strptime(clean_date, "%Y-%m-%d").strftime("%d %b %Y")  # Convertir

        elif hasattr(date_value, "to_native"):  # Si es un objeto `neo4j.time.DateTime`
            return date_value.to_native().strftime("%d %b %Y")  

        else:
            return "Unknown Date"
    
    except Exception as e:
        print(f"⚠️ Error al formatear fecha: {e}")
        return "Unknown Date"
    
def show():
    user = st.session_state["user"]
    user_id = user["user_id"] 
    st.title("🎬 Entertainment Recommendation")
    st.write(f"Bienvenido {user['name']} al sistema de recomendación de entretenimiento.")
    st.markdown("---")

    user_controller = UserController()
    # Obtener contenido desde la BD
    movies = user_controller.get_movies_not_rated_by_user(user_id, 10)
    series = user_controller.get_series_not_rated_by_user(user_id, 10)

    # Inicializar estados de sesión
    if "movie_index" not in st.session_state:
        st.session_state.movie_index = 0

    if "series_index" not in st.session_state:
        st.session_state.series_index = 0

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Películas"

    # Mini navegación entre películas y series
    st.markdown("""
    <style>
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .nav-buttons button {
            background: #4A90E2;
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }
        .nav-buttons button:hover {
            background: #357ABD;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎬 Películas"):
            st.session_state.active_tab = "Películas"
    with col2:
        if st.button("📺 Series"):
            st.session_state.active_tab = "Series"

    # Elegir el contenido según la pestaña activa
    content = movies if st.session_state.active_tab == "Películas" else series
    content_index = st.session_state.movie_index if st.session_state.active_tab == "Películas" else st.session_state.series_index
    if not content:
        st.warning(f"No hay contenido disponible en la sección {st.session_state.active_tab}.")
        return  # Evita que el código siga ejecutándose con una lista vacía.

    content_index = st.session_state.movie_index if st.session_state.active_tab == "Películas" else st.session_state.series_index

    # Asegurar que el índice esté dentro de los límites de la lista
    if content_index >= len(content):
        content_index = 0

    current_media = content[content_index]

    # Estilos CSS para la tarjeta centrada
    st.markdown("""
    <style>
        .center-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .card {
            width: 350px;
            background: #1b233d;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-left: 38%;
        }
        .poster {
            width: 100%;
            border-radius: 10px;
        }
        .title {
            color: white;
            font-size: 22px;
            font-weight: bold;
            margin-top: 15px;
        }
        .info {
            color: #ccc;
            font-size: 14px;
            margin-top: 5px;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        .stButton>button {
            width: 45%;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px;
            margin-left: 30%;              
        }
    </style>
    """, unsafe_allow_html=True)
    release_date = format_date(current_media["release_date"])


    # Tarjeta de la película/serie
    card_content = f"""
        <div class="card">
            <img src="https://www.w3schools.com/howto/img_avatar.png" class="poster">
            <div class="title">{current_media["media_title"]}</div>
            <div class="info">Release Date: {release_date}</div>
    """

    # Solo agregar episodios y temporadas si existen (para series)
    if "total_episodes" in current_media and current_media["total_episodes"] is not None:
        card_content += f'<div class="info">Episodes: {current_media["total_episodes"]} | Seasons: {current_media["total_seasons"]}</div>'


    if "duration" in current_media and current_media["duration"] is not None:
        card_content += f'<div class="info">Duration: {current_media["duration"]} minutes</div>'
        card_content += f'<div class="info">Budget: {current_media["budget"]} Dollars</div>'

    # Solo agregar show runner si existe (para series)
    if "show_runner" in current_media and current_media["show_runner"]:
        card_content += f'<div class="info">Status: {current_media["status"]}</div>'
        card_content += f'<div class="info">Show Runner: {current_media["show_runner"]}</div>'

    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown(card_content, unsafe_allow_html=True)

    # Botones invisibles para manejar la lógica de Streamlit
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("✅ Ya la vi", key="next"):
            if st.session_state.active_tab == "Películas":
                st.session_state.movie_index = (st.session_state.movie_index + 1) % len(movies)
            else:
                st.session_state.series_index = (st.session_state.series_index + 1) % len(series)
    with col1:
        if st.button("❌ No la vi", key="skip"):
            if st.session_state.active_tab == "Películas":
                st.session_state.movie_index = (st.session_state.movie_index + 1) % len(movies)
            else:
                st.session_state.series_index = (st.session_state.series_index + 1) % len(series)

    st.markdown('</div>', unsafe_allow_html=True)
    user_controller.close()

