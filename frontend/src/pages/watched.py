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
    
    st.title("Gestión de mis Vistas 👀")
    st.write("Aquí puedes ver y administrar tus vistas")
    
    st.subheader("🎬 Películas vistas")
    watched_movies = watchedController.get_watched_movies_by_user(user_id)

    if watched_movies:
        df_movies = pd.DataFrame(watched_movies)
        st.table(df_movies)
    else:
        st.info("No has visto ninguna película aún.")

    st.subheader("📺 Series vistas")
    # TODO: Implement get_watched_series_by_user() when available


    
