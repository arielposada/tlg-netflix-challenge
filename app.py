import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from netflix_db import initialize, get_all_movies, search_movies_by_title, search_movies_by_director, save_document, get_all_directors

columns = ['name', 'genre', 'director', 'company']
collection_name = "movies" 

def get_firebase_app():
    # Intenta detener la aplicación de Firebase si ya está inicializada
    try: 
        firebase_admin.delete_app(st.firebase_app)
    except:
        pass
    # Inicializar base de datos
    cred = credentials.Certificate("certificate.json") 
    firebase_admin.initialize_app(cred)
    # Carga inicial de la base de datos
    initialize(db, collection_name, "movies.csv")

try:
    get_firebase_app()
    print("La base de datos fue inicializada")
except:
    print("La base de datos ya está inicializada")

# Get reference to Firestore database
db = firestore.client()

# Mostrar la interfaz de usuario con Streamlit
st.title("Netflix app")


##########################################################################################
# Mostrar todos los filmes  (checkbox)                                                   #
##########################################################################################
with st.sidebar:
    mostrar_todos_checkbox = st.checkbox("Mostrar todos los filmes", value=True)



##########################################################################################
# Buscar por título (textbox)                                                            #
########################################################################################## 
with st.sidebar:
    titulo_filme = st.text_input("Título del filme", key="title")
    buscar_titulo_button = st.button("Buscar filmes")

# Filtrar por título si se hace clic en el botón
if buscar_titulo_button:
    st.subheader("Resultados de la búsqueda por título")
    titulo_results_df = search_movies_by_title(db, collection_name, titulo_filme)
    st.dataframe(titulo_results_df)


##########################################################################################
# Buscar por director (combo)                                                            #
########################################################################################## 
# Obtener la lista de directores para el combo
directores_list = get_all_directors(db, collection_name)

with st.sidebar:
    # Mostrar combo para seleccionar director
    selected_director = st.selectbox("Seleccionar director", ["Todos"] + directores_list,key="director")
    filtrar_director_button = st.button("Filtrar director")

# Considerar la opción "Todos" para el filtro
if filtrar_director_button:
    st.subheader("Resultados de la búsqueda por director")
    if selected_director == "Todos":
        # Mostrar todos si se eligió "Todos"
        all_movies_df = get_all_movies(db, collection_name)
        st.dataframe(all_movies_df)
    else:
        # De lo contrario filtrar por director
        director_results_df = search_movies_by_director(db, collection_name, selected_director)
        st.dataframe(director_results_df)





##########################################################################################
# Mostrar todos                                                                          #
########################################################################################## 
if mostrar_todos_checkbox:
    st.subheader("Todos los filmes")
    all_movies_df = get_all_movies(db, collection_name)
    st.dataframe(all_movies_df)