# lib/config.py
import sqlite3
import os

def create_connection(db_file='company.db'):
    """ Create a database connection to the SQLite database specified by db_file. """
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to the database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def close_connection(conn):
    """ Close the database connection. """
    if conn:
        conn.close()
        print("Database connection closed.")

# Create a connection to the database
CONN = create_connection()

# Create a cursor object
CURSOR = CONN.cursor()

# Optionally, you can close the connection when the script ends
import atexit
atexit.register(lambda: close_connection(CONN))
