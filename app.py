import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from netflix_db import initialize, get_all_movies, search_movies_by_title, search_movies_by_director, save_document


# Configure access to database
cred = credentials.Certificate("certificate.json") 
firebase_admin.initialize_app(cred)

# Get reference to Firestore database
collection_name = "movies" 
db = firestore.client()

initialize(db, collection_name, "movies.csv")

# Obtener todas las películas
movies_df = get_all_movies(db, collection_name)

# Mostrar la interfaz de usuario con Streamlit
st.title("Películas en Firestore")

# Mostrar el DataFrame
st.dataframe(movies_df[['name', 'genre', 'director', 'company']])

