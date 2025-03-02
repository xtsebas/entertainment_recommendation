import streamlit as st
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.controller.watched_controller import UserWatchedController

watchedController = UserWatchedController()


def show():
    
    user = st.session_state["user"]
    user_id = user["user_id"] 
    watched_movies = watchedController.get_watched_movies_by_user(user_id)
    watched_series  = watchedController.get_watched_series_by_user(user_id)
    
    print(watched_movies)
    print(watched_series)
    # Format data for dropdown
    movie_options = [(m["movie"], "movie") for m in watched_movies] if watched_movies else []
    series_options = [(s["serie"], "serie") for s in watched_series] if watched_series else []
    
    
    st.title("Gestión de mis Vistas 👀")
    st.write("Aquí puedes ver y administrar tus vistas")
    
    #mostradndo peliculas vistas
    st.subheader("🎬 Películas vistas")
    if watched_movies:
        df_movies = pd.DataFrame(watched_movies)
        st.table(df_movies)
    else:
        st.info("No has visto ninguna película aún.")
    
    # Dropdown for movies
    if watched_movies:
        st.subheader("🗑️ Eliminar película de mis vistas")
        selected_movie = st.selectbox(
            "Selecciona una película para eliminar:", 
            options=[m["movie"] for m in watched_movies], 
            key="movie_dropdown"
        )
        
        if st.button("Eliminar Película", key="delete_movie"):
            watchedController.delete_watched_movie_by_user(user_id, selected_movie)
            st.success(f"🎬 '{selected_movie}' ha sido eliminada de tus vistas.")
            st.rerun()  

    st.subheader("📺 Series vistas")

    #mostrando series vistas
    if watched_series:
        df_series = pd.DataFrame(watched_series)
        st.table(df_series)
    else:
        st.info("No has visto ninguna serie aún.")

    # Dropdown for series
    if watched_series:
        st.subheader("🗑️ Eliminar serie de mis vistas")
        selected_series = st.selectbox(
            "Selecciona una serie para eliminar:", 
            options=[s["serie"] for s in watched_series], 
            key="series_dropdown"
        )
        
        if st.button("Eliminar Serie", key="delete_series"):
            watchedController.delete_watched_serie_by_user(user_id, selected_series)
            st.success(f"📺 '{selected_series}' ha sido eliminada de tus vistas.")
            st.rerun()  
    
    
    
    



    
