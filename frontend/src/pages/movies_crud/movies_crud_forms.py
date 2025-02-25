import streamlit as st
import uuid
from datetime import date
from backend.controller.media_controller import MediaController
from backend.controller.is_a_controller import IS_A_Controller

from backend.view.movie import Movie
from backend.view.media import Media


# Initialize controller
movieController = MediaController()
is_a_relationControlller = IS_A_Controller()

def show_create_movie():
    st.title("🎬 Agregar una Nueva Película")
    st.write("Aquí puedes agregar una nueva película.")

    # ✅ Movie Form Inputs
    title = st.text_input("Título de la película", placeholder="Ejemplo: Inception")
    duration = st.number_input("Duración (horas)", min_value=1.0, max_value=10.0, step=0.5)
    budget = st.number_input("Presupuesto ($)", min_value=0.0, step=1000000.0)
    revenue = st.number_input("Ingresos ($)", min_value=0.0, step=1000000.0)

    # ✅ Dropdown for Genres
    possible_genres = ["Acción", "Aventura", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Documental", "Romance"]
    genres = st.multiselect("Géneros", possible_genres)

    # ✅ Multiselect Dropdown for Nominations
    possible_nominations = ["Oscar", "BAFTA", "Golden Globe", "Cannes", "Emmy", "Goya", "Sundance"]
    nominations = st.multiselect("Nominaciones", possible_nominations)

    # ✅ Age Classification (Single Selection)
    age_classifications = ["G", "PG", "PG-13", "R", "NC-17"]
    age_classification = st.radio("Clasificación de Edad", age_classifications)

    # ✅ Release Date Picker
    release_date = st.date_input("Fecha de Estreno", min_value=date(1900, 1, 1), max_value=date.today())

    # ✅ Form Validation
    if st.button("Agregar Película"):
        if not title:
            st.error("❌ El título de la película no puede estar vacío.")
        elif duration <= 0:
            st.error("❌ La duración debe ser mayor a 0.")
        elif budget < 0 or revenue < 0:
            st.error("❌ Presupuesto e ingresos deben ser valores positivos.")
        elif not age_classification:
            st.error("❌ Debes seleccionar una clasificación de edad.")
        elif not genres:
            st.error("❌ Debes seleccionar al menos un género.")
        elif not release_date:
            st.error("❌ Debes seleccionar una fecha de estreno válida.")
        else:
            # Convert duration to minutes for database
            duration_minutes = int(duration * 60)

            # ✅ Generate unique media_id
            media_id = str(uuid.uuid4())

            # ✅ Create Media object
            media = Media(
                media_id=media_id,
                title=title,
                genres=genres,
                release_date=release_date,  # Now stored as Python date type
                avg_rating=0.0  # Default value for new entries
            )

            # ✅ Create Movie Object
            movie = Movie(
                movie_id=media_id,
                duration=duration_minutes,
                budget=budget,
                revenue=revenue,
                nominations=nominations,
                age_classification=age_classification
            )
            
            # ✅ Store in Database
            movieController.create_media(media=media, media_type="movie", movie=movie)
            is_a_relationControlller.create_movie_relation(media_id=media_id, movie=movie)
            st.write(media_id)
            st.success(f"✅ Película '{title}' agregada con éxito.")
