import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from netflix_db import initialize, get_all_movies, search_movies_by_title, search_movies_by_director, save_document, get_all_directors


# Configure access to database
cred = credentials.Certificate("certificate.json") 
firebase_admin.initialize_app(cred)

# Get reference to Firestore database
collection_name = "movies" 
db = firestore.client()

columns = ['name', 'genre', 'director', 'company']

# Inicializar la base de datos
#initialize(db, collection_name, "movies.csv")

# Obtener todas las películas
movies_df = get_all_movies(db, collection_name)

# Mostrar la interfaz de usuario con Streamlit
st.title("Netflix app")

# Mostrar el DataFrame
st.dataframe(movies_df[columns])

##########################################################################################
# Mostrar todos los filmes  (checkbox)                                                   #
##########################################################################################
mostrar_todos_checkbox = st.checkbox("Mostrar todos los filmes")

if mostrar_todos_checkbox:
    all_movies_df = get_all_movies(db, collection_name)
    st.dataframe(all_movies_df)


##########################################################################################
# Buscar por título (textbox)                                                            #
########################################################################################## 
titulo_filme = st.text_input("Título del filme")
buscar_titulo_button = st.button("Buscar filmes")

# Filtrar por título si se hace clic en el botón
if buscar_titulo_button:
    titulo_results_df = search_movies_by_title(db, collection_name, titulo_filme)
    st.dataframe(titulo_results_df)


##########################################################################################
# Buscar por director (combo)                                                            #
########################################################################################## 
# Obtener la lista de directores para el combo
directores_list = get_all_directors(db, collection_name)

# Mostrar combo para seleccionar director
selected_director = st.selectbox("Seleccionar director", ["Todos"] + directores_list)
filtrar_director_button = st.button("Filtrar director")

# Considerar la opción "Todos" para el filtro
if filtrar_director_button:
    if selected_director == "Todos":
        # Mostrar todos si se eligió "Todos"
        all_movies_df = get_all_movies(db, collection_name)
        st.dataframe(all_movies_df)
    else:
        # De lo contrario filtrar por director
        director_results_df = search_movies_by_director(db, collection_name, selected_director)
        st.dataframe(director_results_df)