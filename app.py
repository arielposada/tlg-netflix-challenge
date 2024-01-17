import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from netflix_db import initialize, get_all_movies, search_movies_by_title, search_movies_by_director, save_document, get_all_directors


columns = ['name', 'genre', 'director', 'company']
collection_name = "movies" 

def get_firebase_app():
    # Inicializar base de datos
    dic = dict(st.secrets["firebase"])
    cred = credentials.Certificate(dic) 
    firebase_admin.initialize_app(cred)


get_firebase_app()

try:
    get_firebase_app()
    print("La base de datos fue inicializada")
except:
    print("La base de datos ya está inicializada")



# Get reference to Firestore database
db = firestore.client()


# Obtiene la lista de todas las películas para minimizar numero de lecturas
all_movies_df = get_all_movies(db, collection_name)
if all_movies_df.empty:
    # Carga inicial de la base de datos, si, solo si, está vacía
    initialize(db, collection_name, "movies.csv")
    all_movies_df = get_all_movies(db, collection_name)

# Mostrar la interfaz de usuario con Streamlit
st.title("Netflix app")


##########################################################################################
# Mostrar todos los filmes  (checkbox)                                                   #
##########################################################################################
with st.sidebar:
    # Oculto por defecto
    mostrar_todos_checkbox = st.checkbox("Mostrar todos los filmes", value=False, key="mostrar_todos")



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
# Dejó de usarse la versión previa para minimizar el número de lecturas
# directores_list = get_all_directors(db, collection_name)
directors_list = sorted(all_movies_df['director'].unique())
companies_list = sorted(all_movies_df['company'].unique())
genres_list = sorted(all_movies_df['genre'].unique())

with st.sidebar:
    # Mostrar combo para seleccionar director
    selected_director = st.selectbox("Seleccionar director", ["Todos"] + directors_list,key="director")
    filtrar_director_button = st.button("Filtrar director")

# Considerar la opción "Todos" para el filtro
if filtrar_director_button:
    st.subheader("Resultados de la búsqueda por director")
    if selected_director == "Todos":
        # Mostrar todos si se eligió "Todos"
        # all_movies_df = get_all_movies(db, collection_name)
        st.dataframe(all_movies_df)
    else:
        # De lo contrario filtrar por director
        director_results_df = search_movies_by_director(db, collection_name, selected_director)
        st.dataframe(director_results_df)


##########################################################################################
# Formulario nuevo filme                                                                 #
########################################################################################## 
        
with st.sidebar:
    
    st.sidebar.title("Nuevo filme")
    film_name = st.sidebar.text_input("Nombre", key="film_name")
    film_director = st.sidebar.selectbox("Director", directors_list, key="film_director")
    film_company = st.sidebar.selectbox("Director", companies_list, key="film_company")
    film_genre = st.sidebar.selectbox("Género", genres_list, key="film_genre")

    # Botón para crear nuevo filme con atributo key
    crear_filme_button = st.sidebar.button("Crear nuevo filme", key="crear_filme")

# Lógica para guardar el nuevo filme si se presiona el botón
if crear_filme_button:
    # Verifica que los campos no estén vacíos
    if film_name and film_company and film_director and film_genre:
        # Llama a la función para guardar el nuevo filme
        save_document(db, collection_name, film_name, film_company, film_director, film_genre)
        st.sidebar.success("Registro creado exitosamente")

        # Actualiza la lista de filmes
        all_movies_df = get_all_movies(db, collection_name)

        # Activa botón de mostrar todos los filmes
        mostrar_todos_checkbox = True
    else:
        st.sidebar.error("Datos incompletos")

##########################################################################################
# Mostrar todos                                                                          #
########################################################################################## 
if mostrar_todos_checkbox:
    st.subheader("Todos los filmes")
    st.dataframe(all_movies_df)
