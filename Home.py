import streamlit as st
import sqlite3
from passlib.hash import bcrypt
from PIL import Image
import os
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode
from st_aggrid import GridUpdateMode

from pages import *


# Settings


def initiate_sessions():
    # Initiate session states
    if 'main_database' not in st.session_state:
        st.session_state.main_database = os.path.join(os.getcwd(), "db.sqlite")

    # =============================================================================#

    conn = sqlite3.connect(st.session_state.main_database)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS worksorders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projectNumber TEXT UNIQUE NOT NULL,
            customerCompanyName TEXT NOT NULL,
            projectName TEXT NOT NULL,
            projectDirectory TEXT NOT NULL,
            status TEXT
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                birthday TEXT NOT NULL
            )
        ''')

    conn.commit()
    conn.close()


# Function to validate user credentials
def validate_user(username, password):
    conn = sqlite3.connect(st.session_state.main_database)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()

    if row and bcrypt.verify(password, row[0]):
        return True
    return False


# Login page function
def login_page():
    st.subheader("Login Page")

    # Create or get the session state
    if 'username' not in st.session_state:
        st.session_state.username = ""

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if validate_user(username, password):
            st.success(f"Logged in as {username}")
            st.session_state.username = username
            # Add your code to redirect to another page or display content after login
        else:
            st.error("Invalid credentials")


def main():
    st.set_page_config(layout="centered")
    initiate_sessions()
    image_path = os.path.join(os.getcwd(), 'pages', 'images', 'fan_movement.png')
    image = Image.open(image_path)

    # Divide page header into 3 columns to centralise the logo
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.image(image, width=500)

    colA, colB, colC = st.columns([1, 5, 1])
    with colB:
        st.subheader("**FAN DATABASE SYSTEM**")

    st.divider()

    login_page()


if __name__ == '__main__':
    main()
