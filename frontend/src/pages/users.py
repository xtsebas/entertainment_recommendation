import streamlit as st

def show():
    """Muestra la información del usuario autenticado."""
    
    st.title("👤 Gestión de Usuarios")
    st.write("Información del usuario autenticado y sus preferencias.")

    # Verificar si hay un usuario autenticado en la sesión
    if "user" in st.session_state and st.session_state["user"]:
        user = st.session_state["user"]  # Obtener usuario autenticado
        
        # Manejo de géneros favoritos para asegurar formato correcto
        favorite_genres = user["favorite_genres"]
        if isinstance(favorite_genres, str):
            favorite_genres = [genre.strip() for genre in favorite_genres.strip("[]").split(",")]

        # Mostrar los detalles del usuario
        st.subheader(f"Bienvenido, {user['name']} 👋")
        st.write(f"**Edad:** {user['age']}")
        st.write("**Géneros favoritos:**")
        for genre in favorite_genres:
            st.write(f"- {genre}")  # Mostrar cada género en una nueva línea
        st.write(f"**Duración favorita:** {user['favorite_duration']} minutos")

        st.write("Aquí puedes ver y administrar tu usuario.")

        # Inicializar la acción CRUD si no existe
        if "crud_action" not in st.session_state:
            st.session_state["crud_action"] = None

        # Inyectar estilos CSS para los botones de Streamlit
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

        # Se usan st.button para actualizar el estado de sesión y refrescar la app
        if st.button("🔍 Read", key="read"):
            st.session_state["crud_action"] = "read"
        if st.button("✏️ Update", key="update"):
            st.session_state["crud_action"] = "update"
        if st.button("🗑️ Delete", key="delete"):
            st.session_state["crud_action"] = "delete"

        # Mostrar contenido basado en la acción seleccionada
        accion = st.session_state.get("crud_action")

        if accion == "read":
            st.subheader("Leer Ratings")
            st.write("Aquí se muestran los ratings existentes.")
            # Agregar la lógica de lectura de ratings
        elif accion == "update":
            st.subheader("Actualizar Rating")
            st.write("Aquí puedes actualizar un rating existente.")
            # Agregar la lógica de actualización
        elif accion == "delete":
            st.subheader("Eliminar Rating")
            st.write("Aquí puedes eliminar un rating.")
            # Agregar la lógica de eliminación        

        # Botón para volver al menú principal (resetear la acción)
        if st.button("Volver al menú", key="menu"):
            st.session_state["crud_action"] = None
            st.rerun()

    else:
        st.warning("⚠️ No hay usuario autenticado. Por favor, selecciona un usuario para continuar.")
