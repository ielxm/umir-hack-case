from pydantic_models import *

import sqlite3
import json

DATABASE_PATH="database.db"

def initialize_database() -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartment_type TEXT NOT NULL,        
        rooms_to_include TEXT NOT NULL,
        size REAL NOT NULL,
        budget REAL NOT NULL,
        apartment_style TEXT NOT NULL,
        comment TEXT,
        contact_id INTEGER NOT NULL,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)   
    )
    """)

    connection.commit()
    connection.close()

def send_to_database(form: QuizForm) -> None:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    contact = form.contacts
    cursor.execute("""
                   INSERT INTO contacts (phone_number, name, email)
                   VALUES (?, ?, ?)
                   """, (contact.phone_number, 
                         contact.name, 
                         contact.email))
    

    contact_id = cursor.lastrowid

    cursor.execute("""
                   INSERT INTO requests (apartment_type, rooms_to_include, size, budget, apartment_style, comment, contact_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   """, (form.apartment_type, 
                         json.dumps(sorted(form.rooms_to_include), ensure_ascii=False), 
                         form.size, 
                         form.budget, 
                         form.apartment_style,
                         form.comment, 
                         contact_id))
    
    connection.commit()
    connection.close()

def check_if_entry_is_unique(form: QuizForm) -> bool:
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    contact = form.contacts
    cursor.execute("""
                   SELECT 1
                   FROM requests
                   JOIN contacts ON requests.contact_id = contacts.id
                   WHERE contacts.phone_number = ?
                   AND requests.apartment_type = ?
                   AND requests.rooms_to_include = ?
                   AND requests.size = ?
                   AND requests.budget = ?
                   AND requests.apartment_style = ?
                   LIMIT 1
                   """, (contact.phone_number, 
                         form.apartment_type, 
                         json.dumps(sorted(form.rooms_to_include), ensure_ascii=False), 
                         form.size, 
                         form.budget, 
                         form.apartment_style))
    
    result = cursor.fetchone()
    connection.close()

    return result is None