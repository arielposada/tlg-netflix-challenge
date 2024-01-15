import pandas as pd
import firebase_admin
from firebase_admin import firestore

# Método para limpiar previamente la colección
def clean_collection(db_collection):
    collection = db_collection.stream()
    for doc in collection:
        doc.reference.delete()

def initialize(db, collection_name, csv_file_path):
    # Limpiar la colección
    try:
        # Elimina los datos de la colección, previo a la carga, para evitar duplicados y quitar datos de prueba
        clean_collection(db.collection(collection_name))
        print(f"Documentos en la colección '{collection_name}' eliminados con éxito.")
    except Exception as e:
        # Si no pudo es probable que sea la primera vez que se realiza
        print(f"No se limpió la colección: {e}")

    # Cargar los datos del archivo CSV 
    df = pd.read_csv(csv_file_path)
    data_dict = df.to_dict(orient='records')

    # Sube los datos a la colección 'movies' en Firestore
    for doc_data in data_dict:
        # Se agrega la columna adicional
        doc_data['name_lowercase'] = doc_data['name'].lower()
        db.collection(collection_name).add(doc_data)
   
# Método para convertir el resultado en dataframe
def results_to_dataframe(results):
    dataset = [{doc.id: doc.to_dict()} for doc in results]
    df = pd.DataFrame.from_dict({item: data for sublist in dataset for item, data in sublist.items()}, orient='index')

    # Columnas requeridas
    columns = ['name', 'company', 'director', 'genre']
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df

# Método para obtenre todas las películas
def get_all_movies(db, collection_name):
    all_movies_results = db.collection(collection_name).get()

    all_movies_df = results_to_dataframe(all_movies_results)
    return all_movies_df[['name', 'company', 'director', 'genre']]

def search_movies_by_title(db, collection_name, title_query):
    # Búsqueda por título, ignorando mayúsculas
    title_query = title_query.lower()

    # Realiza la consulta en Firestore
    title_results = (
        db.collection(collection_name)
        .where('name_lowercase', '>=', title_query)
        .where('name_lowercase', '<=', title_query + '\uf8ff')
        .get()
    )

    title_df = results_to_dataframe(title_results)

    return title_df[['name', 'company', 'director']]

def search_movies_by_director(db, collection_name, director_query):
    # Realiza la búsqueda por director usando igualdad exacta
    director_results = (
        db.collection(collection_name)
        .where('director', '==', director_query)
        .get()
    )
    
    director_results_df = results_to_dataframe(director_results)

    return director_results_df[['name', 'company', 'director', 'genre']]

# Método para hacer el guardado
def save_document(db, collection_name, name, company, director, genre):
    name_lowercase = name.lower()

    # Estructura
    movie = {
        'name': name,
        'company': company,
        'director': director,
        'genre': genre,
        'name_lowercase': name_lowercase,
    }

    # Guardado
    db.collection(collection_name).add(movie)

# Método para la consulta de los directores
def get_all_directors(db, collection_name):
    
    directors_query = db.collection(collection_name).select(['director']).get()
    directors_list = list(set(doc.get('director') for doc in directors_query))

    return sorted(directors_list)

