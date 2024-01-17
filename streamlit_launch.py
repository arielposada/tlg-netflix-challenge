import firebase_admin
from firebase_admin import credentials
import streamlit as st
from netflix_db import initialize

def get_firebase_app():
    # Initialize Firebase
    dic = dict(st.secrets["firebase"])
    cred = credentials.Certificate(dic) 
    firebase_admin.initialize_app(cred)

def main():
    # Initialize Firebase
    get_firebase_app()

    initialize(get_firebase_app(), "movies", "movies.csv")

if __name__ == "__main__":
    main()