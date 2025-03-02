import streamlit as st
import uuid
import pandas as pd

from datetime import date
from backend.controller.media_controller import MediaController
from backend.controller.serie_controller import SerieController

from backend.controller.is_a_controller import IS_A_Controller
from backend.view.media import Media
from backend.view.serie import Serie
# Initialize controllers
seriesController = MediaController()
singleSeriesController =SerieController()
is_a_controller = IS_A_Controller()

def show_create_serie():
    st.title("📺 Agregar una Nueva Serie")
    st.write("Aquí puedes agregar una nueva serie.")

    # ✅ Series Form Inputs
    title = st.text_input("Título de la Serie", placeholder="Ejemplo: Breaking Bad")
    total_episodes = st.number_input("Total de Episodios", min_value=1, step=1)
    total_seasons = st.number_input("Total de Temporadas", min_value=1, step=1)
    status = st.selectbox("Estado de la Serie", ["En emisión", "Finalizada", "Cancelada"])
    release_format = st.text_input("Formato de Lanzamiento", placeholder="Ejemplo: TV Show, Streaming, Web Series")
    show_runner = st.text_input("Showrunner", placeholder="Ejemplo: Vince Gilligan")

    # ✅ Dropdown for Genres
    possible_genres = ["Acción", "Aventura", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Documental", "Romance"]
    genres = st.multiselect("Géneros", possible_genres)

    # ✅ Release Date Picker
    release_date = st.date_input("Fecha de Estreno", min_value=date(1900, 1, 1), max_value=date.today())

    # ✅ Form Validation
    if st.button("Agregar Serie"):
        if not title:
            st.error("❌ El título de la serie no puede estar vacío.")
        elif total_episodes <= 0:
            st.error("❌ El número de episodios debe ser mayor a 0.")
        elif total_seasons <= 0:
            st.error("❌ El número de temporadas debe ser mayor a 0.")
        elif not status:
            st.error("❌ Debes seleccionar el estado de la serie.")
        elif not release_format:
            st.error("❌ Debes especificar el formato de lanzamiento.")
        elif not show_runner:
            st.error("❌ Debes ingresar el nombre del Showrunner.")
        elif not genres:
            st.error("❌ Debes seleccionar al menos un género.")
        elif not release_date:
            st.error("❌ Debes seleccionar una fecha de estreno válida.")
        else:
            # Generate unique media_id
            media_id = str(uuid.uuid4())

            # Create Media object
            media = Media(
                media_id=media_id,
                title=title,
                genres=genres,
                release_date=release_date,
                avg_rating=0.0  # Default value for new series
            )

            # Create Serie Object
            serie = Serie(
                total_episodes=total_episodes,
                total_seasons=total_seasons,
                status=status,
                release_format=release_format,
                show_runner=show_runner
            )
            
            # Step 1: Store Media and Series Nodes in Database
            seriesController.create_media(media=media, media_type="serie", serie=serie)

            # Create the IS_A Relationship
            is_a_controller.create_serie_relation(media_id=media_id, serie=serie)

            st.success(f"✅ Serie '{title}' agregada con éxito.")


def show_read_serie():
    st.title("📺 Lista de Series")

    # Fetch total series count (assuming database has 1979 series)
    total_series = 1979  # Hardcoded, replace with actual DB query if needed
    st.write(f"📊 Total de series disponibles: **{total_series}**")

    # User input to modify the limit
    limit = st.number_input("Cantidad de series a mostrar:", min_value=1, max_value=total_series, value=25, step=1)

    # Fetch series based on limit
    series = singleSeriesController.get_all_series_sorted_by_creation(limit=limit)

    # Convert to DataFrame and display
    if series:
        df_series = pd.DataFrame(series)
        st.table(df_series)
    else:
        st.info("No hay series disponibles.")    


def show_update_serie():
    pass 

def show_delete_serie():
    pass 